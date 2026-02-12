"""
GTF Command Center v7
Color tags, no emojis
"""

import streamlit as st
import json
from datetime import datetime, date
from pathlib import Path

st.set_page_config(
    page_title="GTF Command Center",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"departments": [], "department_labels": {}, "tasks": []}

data = load_tasks()
tasks = data.get("tasks", [])
dept_labels = data.get("department_labels", {})
today_str = date.today().isoformat()

# Department colors
dept_colors = {
    "customers": "#8B5CF6",      # Purple
    "customs_shipping": "#0891B2", # Teal
    "brand_outreach": "#059669",  # Green
    "brand_followups": "#10B981", # Emerald
    "content": "#EC4899",         # Pink
    "legal": "#6366F1",           # Indigo
    "product": "#3B82F6",         # Blue
    "business": "#F59E0B",        # Amber
    "fundraising": "#EF4444",     # Red
    "hiring": "#8B5CF6",          # Purple
    "finance": "#14B8A6",         # Teal
    "quick": "#9CA3AF"            # Gray
}

# Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@400;500;600&display=swap');
    
    :root {
        --cream: #FAFAF8;
        --white: #FFFFFF;
        --charcoal: #1a1a1a;
        --gray: #6b6b6b;
        --light-gray: #e5e5e5;
        --gold: #c9a87c;
        --red: #c45c5c;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
        background-color: var(--cream) !important;
    }
    
    .main .block-container {
        background-color: var(--cream) !important;
        padding: 2rem 3rem !important;
        max-width: 1000px !important;
    }
    
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: var(--white) !important;
        border-right: 1px solid var(--light-gray) !important;
    }
    
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
    }
    
    p, span, div, label, li {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Stats */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0 2rem 0;
    }
    
    .stat-box {
        background: var(--white);
        border: 1px solid var(--light-gray);
        padding: 1.25rem;
        text-align: center;
    }
    
    .stat-num {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 500;
        color: var(--charcoal);
    }
    
    .stat-num.red { color: var(--red); }
    
    .stat-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.4rem;
    }
    
    /* Progress */
    .progress-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        color: var(--gray);
        margin-bottom: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .progress-track {
        height: 2px;
        background: var(--light-gray);
        margin-bottom: 1.5rem;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--gold);
    }
    
    /* Section */
    .section-head {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--light-gray);
    }
    
    /* Task */
    .task-card {
        background: var(--white);
        border: 1px solid var(--light-gray);
        padding: 1rem 1.25rem;
        margin-bottom: 0.5rem;
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
    }
    
    .task-priority {
        width: 3px;
        min-height: 32px;
        flex-shrink: 0;
    }
    
    .priority-high { background: #c45c5c; }
    .priority-medium { background: #c9a87c; }
    .priority-low { background: #d1d5db; }
    
    .task-body { flex: 1; }
    
    .task-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--charcoal);
        line-height: 1.4;
        margin-bottom: 0.3rem;
    }
    
    .task-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .task-due {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        color: var(--gray);
    }
    
    .task-due.overdue {
        color: var(--red);
        font-weight: 500;
    }
    
    .dept-tag {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.6rem;
        font-weight: 500;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tabs */
    .stRadio > div {
        flex-direction: row !important;
        gap: 0 !important;
        background: transparent !important;
    }
    
    .stRadio > div > label {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        padding: 0.6rem 1.25rem !important;
        border: 1px solid var(--light-gray) !important;
        border-right: none !important;
        border-radius: 0 !important;
        background: var(--white) !important;
        color: var(--gray) !important;
        margin: 0 !important;
    }
    
    .stRadio > div > label:last-child {
        border-right: 1px solid var(--light-gray) !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: var(--charcoal) !important;
        color: var(--white) !important;
        border-color: var(--charcoal) !important;
    }
    
    /* Expander */
    .stExpander {
        border: 1px solid var(--light-gray) !important;
        border-radius: 0 !important;
        background: var(--white) !important;
        margin-bottom: 0.4rem !important;
    }
    
    /* Sidebar */
    .sb-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.6rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1.5rem 0 0.6rem 0;
    }
    
    .sb-row {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: var(--charcoal);
        padding: 0.25rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sb-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
</style>
""", unsafe_allow_html=True)

# Stats
open_tasks = [t for t in tasks if not t.get("done")]
done_tasks = [t for t in tasks if t.get("done")]
today_tasks = [t for t in open_tasks if t.get("due_date") == today_str]
overdue = [t for t in open_tasks if t.get("due_date") and t.get("due_date") < today_str]
high_p = [t for t in open_tasks if t.get("priority") == "high"]
progress = (len(done_tasks) / len(tasks) * 100) if tasks else 0

# Sidebar
with st.sidebar:
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=140)
    
    st.markdown('<div class="sb-title">Overview</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-row">Open: <strong>{len(open_tasks)}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-row">Today: <strong>{len(today_tasks)}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sb-row">Overdue: <strong>{len(overdue)}</strong></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-title">Departments</div>', unsafe_allow_html=True)
    for dk, dn in dept_labels.items():
        c = len([t for t in open_tasks if t.get("department") == dk])
        if c > 0:
            color = dept_colors.get(dk, "#9CA3AF")
            st.markdown(f'<div class="sb-row"><span class="sb-dot" style="background:{color}"></span>{dn}: <strong>{c}</strong></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Text Zoya to manage tasks")

# Main
st.markdown("## Command Center")
st.caption(datetime.now().strftime("%A, %B %d, %Y"))

# Progress
st.markdown(f"""
<div class="progress-row">
    <span>Progress</span>
    <span>{len(done_tasks)} / {len(tasks)}</span>
</div>
<div class="progress-track">
    <div class="progress-fill" style="width:{progress}%"></div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-box">
        <div class="stat-num">{len(open_tasks)}</div>
        <div class="stat-label">Open</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">{len(today_tasks)}</div>
        <div class="stat-label">Today</div>
    </div>
    <div class="stat-box">
        <div class="stat-num {'red' if overdue else ''}">{len(overdue)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">{len(high_p)}</div>
        <div class="stat-label">Priority</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
view = st.radio("", ["Today", "All", "Department", "Done"], horizontal=True, label_visibility="collapsed")

def show_task(task, show_dept=True):
    p = task.get("priority", "medium")
    due = task.get("due_date")
    dk = task.get("department", "quick")
    dept = dept_labels.get(dk, "Quick")
    color = dept_colors.get(dk, "#9CA3AF")
    
    due_html = ""
    if due:
        if due < today_str:
            due_html = '<span class="task-due overdue">Overdue</span>'
        elif due == today_str:
            due_html = '<span class="task-due">Today</span>'
        else:
            due_html = f'<span class="task-due">{due}</span>'
    
    dept_html = f'<span class="dept-tag" style="background:{color}">{dept}</span>' if show_dept else ''
    
    st.markdown(f"""
    <div class="task-card">
        <div class="task-priority priority-{p}"></div>
        <div class="task-body">
            <div class="task-title">{task['title']}</div>
            <div class="task-info">
                {due_html}
                {dept_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Views
if view == "Today":
    if overdue:
        st.markdown('<div class="section-head">Overdue</div>', unsafe_allow_html=True)
        for t in sorted(overdue, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    if today_tasks:
        st.markdown('<div class="section-head">Due Today</div>', unsafe_allow_html=True)
        for t in sorted(today_tasks, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    upcoming = [t for t in open_tasks if t.get("due_date") and t.get("due_date") > today_str][:5]
    if upcoming:
        st.markdown('<div class="section-head">Coming Up</div>', unsafe_allow_html=True)
        for t in sorted(upcoming, key=lambda x: x.get("due_date")):
            show_task(t)
    
    if not overdue and not today_tasks:
        st.info("Nothing due today")

elif view == "All":
    st.markdown('<div class="section-head">All Tasks</div>', unsafe_allow_html=True)
    for t in sorted(open_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
        show_task(t)

elif view == "Department":
    st.markdown('<div class="section-head">By Department</div>', unsafe_allow_html=True)
    for dk, dn in dept_labels.items():
        dept_tasks = [t for t in open_tasks if t.get("department") == dk]
        if dept_tasks:
            with st.expander(f"{dn} ({len(dept_tasks)})"):
                for t in sorted(dept_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
                    show_task(t, show_dept=False)

elif view == "Done":
    if done_tasks:
        st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
        for t in sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)[:30]:
            show_task(t)
    else:
        st.info("No completed tasks yet")
