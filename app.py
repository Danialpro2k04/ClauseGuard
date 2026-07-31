"""
ClauseGuard — Human-in-the-Loop Review Dashboard
--------------------------------------------------
Standalone Streamlit app for legal reviewers to triage, comment on, and
resolve contract-clause risk findings produced by the ClauseGuard backend
pipeline. Reads from and writes back to `pending_reviews.json` in the same
directory as this script.

Source schema (as produced by the pipeline) — only these 5 fields are
required on each record:
    contract_name, clause_text, risk_level, justification, status

The dashboard itself derives/adds everything else it needs (a stable
review_id, a timestamp, and the human_decision/human_notes/reviewed_by/
reviewed_at audit fields) — the pipeline does not need to supply them.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

DATA_FILE = Path(__file__).parent / "pending_reviews.json"

RISK_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

RISK_STYLE = {
    "HIGH": {"color": "#DC2626", "bg": "#FEF2F2", "border": "#FCA5A5", "icon": "🔴"},
    "MEDIUM": {"color": "#D97706", "bg": "#FFFBEB", "border": "#FCD34D", "icon": "🟠"},
    "LOW": {"color": "#65A30D", "bg": "#F7FEE7", "border": "#BEF264", "icon": "🟡"},
}

STATUS_STYLE = {
    "PENDING": {"color": "#4B5563", "bg": "#F3F4F6"},
    "RESOLVED": {"color": "#1D4ED8", "bg": "#EFF6FF"},
}

DECISION_STYLE = {
    "APPROVED": {"color": "#15803D", "bg": "#F0FDF4", "icon": "✅"},
    "REJECTED": {"color": "#B91C1C", "bg": "#FEF2F2", "icon": "❌"},
    "RESOLVED": {"color": "#1D4ED8", "bg": "#EFF6FF", "icon": "🗂️"},
}

# Only these come from the pipeline. Everything else (review_id, timestamp,
# human_decision, human_notes, reviewed_by, reviewed_at) is derived/added by
# this dashboard on load or on first decision.
REQUIRED_FIELDS = [
    "contract_name",
    "clause_text",
    "risk_level",
    "justification",
    "status",
]


# --------------------------------------------------------------------------
# Data layer
# --------------------------------------------------------------------------


@dataclass
class LoadResult:
    records: list[dict[str, Any]]
    error: str | None = None


def _make_review_id(record: dict[str, Any]) -> str:
    """Derive a stable ID from clause content rather than requiring the pipeline
    to supply one. Hashing (contract_name, clause_text) means the *same* clause
    re-flagged in a later pipeline run maps to the same ID (so a decision made
    on it persists / dedupes across pipeline reruns), while two genuinely
    different clauses always get different IDs."""
    basis = f"{record.get('contract_name', '')}||{record.get('clause_text', '')}"
    digest = hashlib.sha256(basis.encode("utf-8")).hexdigest()[:12]
    return f"rev_{digest}"


def _normalize_record(record: dict[str, Any], file_mtime: str) -> dict[str, Any]:
    """Fill in every field the UI needs that the pipeline doesn't supply.
    Never overwrites a field that's already present (so once a human decision
    has been saved back to disk, reloading won't clobber it)."""
    record.setdefault("review_id", _make_review_id(record))
    # The pipeline doesn't timestamp individual findings, so fall back to the
    # file's last-modified time as a "flagged around this time" signal.
    record.setdefault("timestamp", file_mtime)
    record.setdefault("human_decision", None)
    record.setdefault("human_notes", "")
    record.setdefault("reviewed_by", None)
    record.setdefault("reviewed_at", None)
    record.setdefault("status", "PENDING")
    # Normalize risk_level/status casing defensively — pipeline output is
    # free-text from an LLM and could drift ("High" vs "HIGH").
    record["risk_level"] = str(record.get("risk_level", "")).strip().upper()
    record["status"] = str(record.get("status", "PENDING")).strip().upper()
    return record


def load_reviews() -> LoadResult:
    """Load and validate pending_reviews.json. Never raises — returns errors instead,
    since a malformed file shouldn't crash a reviewer's dashboard mid-session."""
    if not DATA_FILE.exists():
        return LoadResult(records=[], error=f"No file found at `{DATA_FILE}`.")

    try:
        raw_text = DATA_FILE.read_text(encoding="utf-8")
        file_mtime = datetime.fromtimestamp(DATA_FILE.stat().st_mtime).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    except OSError as e:
        return LoadResult(records=[], error=f"Could not read file: {e}")

    if not raw_text.strip():
        return LoadResult(records=[], error="File is empty.")

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        return LoadResult(records=[], error=f"Invalid JSON — {e}")

    if not isinstance(data, list):
        return LoadResult(records=[], error="Expected a JSON array at the top level.")

    validated: list[dict[str, Any]] = []
    skipped = 0
    for item in data:
        if not isinstance(item, dict):
            skipped += 1
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in item]
        if missing:
            skipped += 1
            continue
        validated.append(_normalize_record(item, file_mtime))

    # Two records that hash to the same review_id are the *same* clause
    # finding (e.g. the pipeline flagged it again on a later run). Collapse
    # them to one card rather than rendering duplicate widgets with the same
    # key — reviewing the finding once should cover every occurrence of it.
    # If any duplicate is already RESOLVED, prefer that copy so a past
    # decision isn't hidden behind a fresh PENDING duplicate.
    deduped: dict[str, dict[str, Any]] = {}
    duplicate_count = 0
    for record in validated:
        rid = record["review_id"]
        if rid not in deduped:
            deduped[rid] = record
            continue
        duplicate_count += 1
        existing = deduped[rid]
        if existing["status"] == "PENDING" and record["status"] != "PENDING":
            deduped[rid] = record

    error_parts = []
    if skipped:
        error_parts.append(f"skipped {skipped} malformed record(s) missing required fields")
    if duplicate_count:
        error_parts.append(
            f"merged {duplicate_count} duplicate finding(s) for clauses flagged more than once"
        )
    error = ("Note: " + "; ".join(error_parts) + ".") if error_parts else None

    return LoadResult(records=list(deduped.values()), error=error)


def save_reviews(records: list[dict[str, Any]]) -> None:
    """Atomically write records back to DATA_FILE.

    Writes to a temp file in the same directory then renames over the target,
    so a crash or concurrent read mid-write can never leave a half-written /
    corrupt pending_reviews.json on disk.
    """
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=DATA_FILE.parent, prefix=".pending_reviews_", suffix=".tmp"
    )
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, DATA_FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def apply_decision(
    records: list[dict[str, Any]],
    review_id: str,
    decision: str,
    notes: str,
    reviewer: str,
) -> list[dict[str, Any]]:
    """Return a new list with the given review updated. Pure function — makes the
    call site (a button handler) trivial to reason about and test."""
    updated = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for r in records:
        if r["review_id"] == review_id:
            r = {**r}
            r["human_decision"] = decision
            r["human_notes"] = notes.strip()
            r["status"] = "RESOLVED"
            r["reviewed_by"] = reviewer.strip() or "Anonymous Reviewer"
            r["reviewed_at"] = now
        updated.append(r)
    return updated


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------


def init_state() -> None:
    if "records" not in st.session_state:
        result = load_reviews()
        st.session_state.records = result.records
        st.session_state.load_error = result.error
    if "reviewer_name" not in st.session_state:
        st.session_state.reviewer_name = ""
    if "flash" not in st.session_state:
        st.session_state.flash = None  # (kind, message) shown once, then cleared


def reload_from_disk() -> None:
    result = load_reviews()
    st.session_state.records = result.records
    st.session_state.load_error = result.error


# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
    .block-container { padding-top: 2rem; max-width: 1100px; }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 0.9rem 1rem 0.6rem 1rem;
    }

    /* Risk / status pill badges */
    .pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-right: 6px;
        white-space: nowrap;
    }

    .clause-box {
        background: #FAFAFA;
        border-left: 3px solid #D1D5DB;
        border-radius: 6px;
        padding: 0.85rem 1rem;
        font-size: 0.95rem;
        line-height: 1.55;
        color: #1F2937;
        margin: 0.4rem 0 0.8rem 0;
    }

    .justification-box {
        background: #F5F3FF;
        border-left: 3px solid #A78BFA;
        border-radius: 6px;
        padding: 0.85rem 1rem;
        font-size: 0.9rem;
        line-height: 1.5;
        color: #3730A3;
        margin: 0.4rem 0 0.8rem 0;
    }

    .meta-line {
        color: #6B7280;
        font-size: 0.82rem;
        margin-bottom: 0.3rem;
    }

    .decision-note-box {
        background: #F9FAFB;
        border: 1px dashed #D1D5DB;
        border-radius: 6px;
        padding: 0.7rem 0.9rem;
        font-size: 0.88rem;
        color: #374151;
        margin-top: 0.4rem;
    }

    hr { margin: 0.6rem 0 1.2rem 0; }
</style>
"""


def pill(text: str, color: str, bg: str) -> str:
    return f'<span class="pill" style="color:{color};background:{bg};">{text}</span>'


# --------------------------------------------------------------------------
# UI — sidebar
# --------------------------------------------------------------------------


def render_sidebar(records: list[dict[str, Any]]) -> dict[str, Any]:
    st.sidebar.markdown("### ⚖️ ClauseGuard")
    st.sidebar.caption("Human-in-the-Loop compliance review")

    st.session_state.reviewer_name = st.sidebar.text_input(
        "Your name",
        value=st.session_state.reviewer_name,
        placeholder="e.g. J. Alvarez",
        help="Attached to any decision you make below, for the audit trail.",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Filters**")

    status_filter = st.sidebar.radio(
        "Status",
        options=["Pending only", "Resolved only", "All"],
        index=0,
    )

    risk_filter = st.sidebar.multiselect(
        "Risk level",
        options=["HIGH", "MEDIUM", "LOW"],
        default=["HIGH", "MEDIUM", "LOW"],
    )

    contracts = sorted({r["contract_name"] for r in records})
    contract_filter = st.sidebar.multiselect(
        "Contract",
        options=contracts,
        default=[],
        placeholder="All contracts",
    )

    search = st.sidebar.text_input(
        "Search clause text", placeholder="e.g. encryption, indemnification…"
    )

    sort_by = st.sidebar.selectbox(
        "Sort by",
        options=["Risk (High → Low)", "Contract name"],
        index=0,
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reload from disk", use_container_width=True):
        reload_from_disk()
        st.rerun()

    st.sidebar.caption(f"Source: `{DATA_FILE.name}`")

    return {
        "status_filter": status_filter,
        "risk_filter": risk_filter,
        "contract_filter": contract_filter,
        "search": search.strip().lower(),
        "sort_by": sort_by,
    }


# --------------------------------------------------------------------------
# UI — summary metrics
# --------------------------------------------------------------------------


def render_summary(records: list[dict[str, Any]]) -> None:
    pending = [r for r in records if r["status"] == "PENDING"]
    high = sum(1 for r in pending if r["risk_level"] == "HIGH")
    medium = sum(1 for r in pending if r["risk_level"] == "MEDIUM")
    low = sum(1 for r in pending if r["risk_level"] == "LOW")
    resolved = sum(1 for r in records if r["status"] != "PENDING")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Pending review", len(pending))
    c2.metric("🔴 High risk", high)
    c3.metric("🟠 Medium risk", medium)
    c4.metric("🟡 Low risk", low)
    c5.metric("Resolved", resolved)


# --------------------------------------------------------------------------
# UI — filtering & sorting
# --------------------------------------------------------------------------


def filter_and_sort(
    records: list[dict[str, Any]], filters: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = list(records)

    if filters["status_filter"] == "Pending only":
        rows = [r for r in rows if r["status"] == "PENDING"]
    elif filters["status_filter"] == "Resolved only":
        rows = [r for r in rows if r["status"] != "PENDING"]

    if filters["risk_filter"]:
        rows = [r for r in rows if r["risk_level"] in filters["risk_filter"]]

    if filters["contract_filter"]:
        rows = [r for r in rows if r["contract_name"] in filters["contract_filter"]]

    if filters["search"]:
        q = filters["search"]
        rows = [
            r
            for r in rows
            if q in r["clause_text"].lower() or q in r["justification"].lower()
        ]

    if filters["sort_by"] == "Risk (High → Low)":
        rows.sort(
            key=lambda r: (RISK_ORDER.get(r["risk_level"], 99), r["contract_name"])
        )
    else:  # Contract name
        rows.sort(key=lambda r: (r["contract_name"], RISK_ORDER.get(r["risk_level"], 99)))

    return rows


# --------------------------------------------------------------------------
# UI — a single review card
# --------------------------------------------------------------------------


def render_card(record: dict[str, Any]) -> None:
    rid = record["review_id"]
    risk = record.get("risk_level", "LOW")
    risk_s = RISK_STYLE.get(risk, RISK_STYLE["LOW"])
    status = record.get("status", "PENDING")
    status_s = STATUS_STYLE.get(status, STATUS_STYLE["PENDING"])
    is_pending = status == "PENDING"

    with st.container(border=True):
        header_l, header_r = st.columns([5, 2])

        with header_l:
            st.markdown(
                pill(f"{risk_s['icon']} {risk}", risk_s["color"], risk_s["bg"])
                + pill(status, status_s["color"], status_s["bg"]),
                unsafe_allow_html=True,
            )
            st.markdown(f"**{record['contract_name']}**")
            st.markdown(
                f'<div class="meta-line">ID: {rid} &nbsp;•&nbsp; Flagged around: {record["timestamp"]}</div>',
                unsafe_allow_html=True,
            )

        with header_r:
            if not is_pending and record.get("human_decision"):
                d = record["human_decision"]
                d_s = DECISION_STYLE.get(d, DECISION_STYLE["RESOLVED"])
                decision_pill = pill(f"{d_s['icon']} {d}", d_s["color"], d_s["bg"])
                st.markdown(
                    f'<div style="text-align:right;">{decision_pill}</div>',
                    unsafe_allow_html=True,
                )
                if record.get("reviewed_by"):
                    st.markdown(
                        f'<div class="meta-line" style="text-align:right;">by {record["reviewed_by"]} on {record.get("reviewed_at", "")}</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("**Clause**")
        st.markdown(
            f'<div class="clause-box">{record["clause_text"]}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Why it was flagged**")
        st.markdown(
            f'<div class="justification-box">{record["justification"]}</div>',
            unsafe_allow_html=True,
        )

        if not is_pending:
            if record.get("human_notes"):
                st.markdown("**Reviewer notes**")
                st.markdown(
                    f'<div class="decision-note-box">{record["human_notes"]}</div>',
                    unsafe_allow_html=True,
                )
            return  # no action controls on already-resolved items

        # --- Action area for PENDING items ---
        st.markdown("**Your decision**")
        notes_key = f"notes__{rid}"
        notes = st.text_area(
            "Notes (optional, but recommended — visible in the audit trail)",
            key=notes_key,
            placeholder="e.g. Confirmed with vendor legal this is a placeholder clause; escalating.",
            height=80,
            label_visibility="collapsed",
        )

        b1, b2, b3 = st.columns(3)
        reviewer = st.session_state.reviewer_name

        if b1.button("✅ Approve", key=f"approve__{rid}", use_container_width=True):
            commit_decision(rid, "APPROVED", notes, reviewer)

        if b2.button("❌ Reject", key=f"reject__{rid}", use_container_width=True):
            commit_decision(rid, "REJECTED", notes, reviewer)

        if b3.button(
            "🗂️ Mark Resolved", key=f"resolve__{rid}", use_container_width=True
        ):
            commit_decision(rid, "RESOLVED", notes, reviewer)


def commit_decision(review_id: str, decision: str, notes: str, reviewer: str) -> None:
    if not reviewer.strip():
        st.session_state.flash = (
            "warning",
            "Enter your name in the sidebar before recording a decision — it's part of the audit trail.",
        )
        st.rerun()
        return

    st.session_state.records = apply_decision(
        st.session_state.records, review_id, decision, notes, reviewer
    )
    try:
        save_reviews(st.session_state.records)
        st.session_state.flash = (
            "success",
            f"Recorded **{decision}** for `{review_id}` and saved to {DATA_FILE.name}.",
        )
    except OSError as e:
        st.session_state.flash = ("error", f"Decision recorded in-app, but saving to disk failed: {e}")
    st.rerun()


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="ClauseGuard — Compliance Review",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_state()

    st.title("⚖️ ClauseGuard Review Dashboard")
    st.caption(
        "Inspect contract clauses flagged by the compliance pipeline, then approve, reject, or resolve."
    )

    if st.session_state.load_error:
        st.warning(st.session_state.load_error)

    if not DATA_FILE.exists() and not st.session_state.records:
        st.info(
            f"Waiting for `{DATA_FILE.name}` to appear in this directory. "
            "The dashboard will pick it up automatically — use **Reload from disk** in the sidebar once it's there."
        )
        return

    if st.session_state.flash:
        kind, message = st.session_state.flash
        getattr(st, kind)(message)
        st.session_state.flash = None

    filters = render_sidebar(st.session_state.records)

    render_summary(st.session_state.records)
    st.markdown("---")

    visible = filter_and_sort(st.session_state.records, filters)

    if not visible:
        st.info("No reviews match the current filters.")
        return

    st.caption(f"Showing {len(visible)} of {len(st.session_state.records)} reviews.")

    for record in visible:
        render_card(record)


if __name__ == "__main__":
    main()