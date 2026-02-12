"""
GTF Command Center v6
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

# Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@400;500;600&display=swap');
    
    :root {
        --cream: #FAFAF8;
        --white: #FFFFFF;
        --charcoal: #1a1a1a;
        --gray: #6b6b6b;
        --light-gray: #e0e0e0;
        --gold: #c9a87c;
        --red: #c45c5c;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: var(--cream) !important;
    }
    
    .main .block-container {
        background-color: var(--cream) !important;
        padding: 2rem 3rem !important;
        max-width: 1000px !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: var(--white) !important;
        border-right: 1px solid var(--light-gray) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: var(--white) !important;
    }
    
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
    }
    
    p, span, div, label, li {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Stats cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0 2rem 0;
    }
    
    .stat-card {
        background: var(--white);
        border: 1px solid var(--light-gray);
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-num {
        font-family: 'Playfair Display', serif;
        font-size: 2.25rem;
        font-weight: 500;
        color: var(--charcoal);
    }
    
    .stat-num.red { color: var(--red); }
    
    .stat-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Progress */
    .progress-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: var(--gray);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .progress-track {
        height: 2px;
        background: var(--light-gray);
        margin-bottom: 2rem;
    }
    
    .progress-bar {
        height: 100%;
        background: var(--gold);
    }
    
    /* Section */
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--light-gray);
    }
    
    /* Task */
    .task {
        background: var(--white);
        border: 1px solid var(--light-gray);
        padding: 1rem 1.25rem;
        margin-bottom: 0.6rem;
        display: flex;
        gap: 1rem;
        align-items: flex-start;
    }
    
    .task-bar {
        width: 3px;
        min-height: 35px;
        flex-shrink: 0;
    }
    
    .task-bar.high { background: var(--red); }
    .task-bar.medium { background: var(--gold); }
    .task-bar.low { background: var(--light-gray); }
    
    .task-text {
        flex: 1;
    }
    
    .task-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--charcoal);
        line-height: 1.4;
    }
    
    .task-meta {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        color: var(--gray);
        margin-top: 0.25rem;
    }
    
    .task-meta .overdue {
        color: var(--red);
        font-weight: 500;
    }
    
    /* Tabs */
    .stRadio > div {
        flex-direction: row !important;
        gap: 0 !important;
        background: transparent !important;
    }
    
    .stRadio > div > label {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.75rem !important;
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
        margin-bottom: 0.5rem !important;
    }
    
    .stExpander > details > summary {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar */
    .sidebar-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .sidebar-row {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        color: var(--charcoal);
        padding: 0.3rem 0;
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
        st.image(str(logo_path), width=150)
    
    st.markdown('<div class="sidebar-title">Overview</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-row">Open Tasks: <strong>{len(open_tasks)}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-row">Due Today: <strong>{len(today_tasks)}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-row">Overdue: <strong>{len(overdue)}</strong></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">Departments</div>', unsafe_allow_html=True)
    for dk, dn in dept_labels.items():
        c = len([t for t in open_tasks if t.get("department") == dk])
        if c > 0:
            st.markdown(f'<div class="sidebar-row">{dn}: <strong>{c}</strong></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Text Zoya to manage tasks")

# Main content
st.markdown("## Command Center")
st.caption(datetime.now().strftime("%A, %B %d, %Y"))

# Progress
st.markdown(f"""
<div class="progress-row">
    <span>Progress</span>
    <span>{len(done_tasks)} of {len(tasks)} complete</span>
</div>
<div class="progress-track">
    <div class="progress-bar" style="width:{progress}%"></div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown(f"""
<div class="stats-container">
    <div class="stat-card">
        <div class="stat-num">{len(open_tasks)}</div>
        <div class="stat-label">Open</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">{len(today_tasks)}</div>
        <div class="stat-label">Today</div>
    </div>
    <div class="stat-card">
        <div class="stat-num {'red' if overdue else ''}">{len(overdue)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    <div class="stat-card">
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
    dept = dept_labels.get(task.get("department", "quick"), "Quick")
    
    due_text = ""
    if due:
        if due < today_str:
            due_text = '<span class="overdue">Overdue</span>'
        elif due == today_str:
            due_text = "Today"
        else:
            due_text = due
    
    meta = " · ".join([x for x in [due_text, dept if show_dept else None] if x])
    
    st.markdown(f"""
    <div class="task">
        <div class="task-bar {p}"></div>
        <div class="task-text">
            <div class="task-title">{task['title']}</div>
            <div class="task-meta">{meta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Views
if view == "Today":
    if overdue:
        st.markdown('<div class="section-header">Overdue</div>', unsafe_allow_html=True)
        for t in sorted(overdue, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    if today_tasks:
        st.markdown('<div class="section-header">Due Today</div>', unsafe_allow_html=True)
        for t in sorted(today_tasks, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    upcoming = [t for t in open_tasks if t.get("due_date") and t.get("due_date") > today_str][:5]
    if upcoming:
        st.markdown('<div class="section-header">Coming Up</div>', unsafe_allow_html=True)
        for t in sorted(upcoming, key=lambda x: x.get("due_date")):
            show_task(t)
    
    if not overdue and not today_tasks:
        st.info("Nothing due today")

elif view == "All":
    st.markdown('<div class="section-header">All Tasks</div>', unsafe_allow_html=True)
    for t in sorted(open_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
        show_task(t)

elif view == "Department":
    st.markdown('<div class="section-header">By Department</div>', unsafe_allow_html=True)
    for dk, dn in dept_labels.items():
        dept_tasks = [t for t in open_tasks if t.get("department") == dk]
        if dept_tasks:
            with st.expander(f"{dn} ({len(dept_tasks)})"):
                for t in sorted(dept_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
                    show_task(t, show_dept=False)

elif view == "Done":
    if done_tasks:
        st.markdown('<div class="section-header">Completed</div>', unsafe_allow_html=True)
        for t in sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)[:30]:
            show_task(t)
    else:
        st.info("No completed tasks yet")
