"""
GTF Command Center v5
Luxury. Clean. Classy.
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

# Luxury styling - cream, charcoal, gold accents
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Montserrat:wght@300;400;500;600&display=swap');
    
    :root {
        --bg-cream: #FAF9F6;
        --bg-white: #FFFFFF;
        --charcoal: #2C2C2C;
        --charcoal-light: #4A4A4A;
        --warm-gray: #8B8680;
        --border: #E8E6E1;
        --gold: #B8A088;
        --gold-light: #D4C5B5;
        --danger: #C45C5C;
        --success: #6B8E6B;
    }
    
    .main { background: var(--bg-cream) !important; }
    
    .block-container { 
        padding: 2.5rem 3rem !important; 
        max-width: 1100px !important; 
    }
    
    #MainMenu, footer, .stDeployButton, header { visibility: hidden; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { 
        background: var(--bg-white) !important; 
        border-right: 1px solid var(--border) !important; 
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.5rem !important;
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', Georgia, serif !important;
        color: var(--charcoal) !important;
        font-weight: 500 !important;
    }
    
    p, span, div, label {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    /* Header */
    .header-title {
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 2.5rem;
        font-weight: 500;
        color: var(--charcoal);
        letter-spacing: 0.02em;
        margin-bottom: 0.25rem;
    }
    
    .header-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        color: var(--warm-gray);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 400;
    }
    
    /* Stats */
    .stats-row {
        display: flex;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        flex: 1;
        background: var(--bg-white);
        border: 1px solid var(--border);
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Cormorant Garamond', Georgia, serif;
        font-size: 2.5rem;
        font-weight: 500;
        color: var(--charcoal);
        line-height: 1;
    }
    
    .stat-number.alert { color: var(--danger); }
    
    .stat-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.65rem;
        color: var(--warm-gray);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-top: 0.75rem;
    }
    
    /* Progress */
    .progress-container {
        margin: 2rem 0;
    }
    
    .progress-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        color: var(--warm-gray);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
    }
    
    .progress-bar {
        height: 3px;
        background: var(--border);
    }
    
    .progress-fill {
        height: 100%;
        background: var(--gold);
    }
    
    /* Section headers */
    .section-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        color: var(--warm-gray);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin: 2.5rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }
    
    /* Task cards */
    .task-item {
        background: var(--bg-white);
        border: 1px solid var(--border);
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        transition: all 0.2s ease;
    }
    
    .task-item:hover {
        border-color: var(--gold-light);
    }
    
    .task-priority {
        width: 4px;
        height: 40px;
        flex-shrink: 0;
    }
    
    .priority-high { background: var(--danger); }
    .priority-medium { background: var(--gold); }
    .priority-low { background: var(--gold-light); }
    
    .task-content { flex: 1; }
    
    .task-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--charcoal);
        line-height: 1.4;
        margin-bottom: 0.35rem;
    }
    
    .task-meta {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        color: var(--warm-gray);
        letter-spacing: 0.03em;
    }
    
    .task-meta .overdue { 
        color: var(--danger); 
        font-weight: 500;
    }
    
    .task-meta .today { 
        color: var(--charcoal); 
        font-weight: 500;
    }
    
    .task-done .task-title {
        text-decoration: line-through;
        color: var(--warm-gray);
    }
    
    /* Tabs */
    .stRadio > div {
        gap: 0 !important;
        border: 1px solid var(--border) !important;
        background: transparent !important;
        padding: 0 !important;
        display: inline-flex !important;
    }
    
    .stRadio label {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 0.75rem 1.25rem !important;
        border: none !important;
        border-right: 1px solid var(--border) !important;
        border-radius: 0 !important;
        background: var(--bg-white) !important;
        color: var(--warm-gray) !important;
    }
    
    .stRadio label:last-child {
        border-right: none !important;
    }
    
    .stRadio label[data-checked="true"] {
        background: var(--charcoal) !important;
        color: var(--bg-white) !important;
    }
    
    /* Sidebar text */
    .sidebar-section {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.65rem;
        font-weight: 500;
        color: var(--warm-gray);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .sidebar-item {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        color: var(--charcoal-light);
        padding: 0.35rem 0;
    }
    
    .sidebar-item strong {
        color: var(--charcoal);
    }
    
    /* Expanders */
    .stExpander {
        background: var(--bg-white) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0 !important;
    }
    
    .streamlit-expanderHeader {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: var(--warm-gray);
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
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
        st.image(str(logo_path), width=160)
    st.markdown("")
    
    st.markdown('<div class="sidebar-section">Overview</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item">Open Tasks: <strong>{len(open_tasks)}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item">Due Today: <strong>{len(today_tasks)}</strong></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item">Overdue: <strong>{len(overdue)}</strong></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">Departments</div>', unsafe_allow_html=True)
    for dk, dn in dept_labels.items():
        c = len([t for t in open_tasks if t.get("department") == dk])
        if c > 0:
            name = dn.split(' ', 1)[-1] if ' ' in dn else dn
            st.markdown(f'<div class="sidebar-item">{name}: <strong>{c}</strong></div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    st.caption("Text Zoya to manage tasks")

# Header
st.markdown(f"""
<div class="header-title">Command Center</div>
<div class="header-subtitle">{datetime.now().strftime('%A, %B %d, %Y')}</div>
""", unsafe_allow_html=True)

# Progress
st.markdown(f"""
<div class="progress-container">
    <div class="progress-text">
        <span>Progress</span>
        <span>{len(done_tasks)} of {len(tasks)} complete</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown(f"""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-number">{len(open_tasks)}</div>
        <div class="stat-label">Open</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{len(today_tasks)}</div>
        <div class="stat-label">Today</div>
    </div>
    <div class="stat-card">
        <div class="stat-number {'alert' if overdue else ''}">{len(overdue)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{len(high_p)}</div>
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
    done = task.get("done", False)
    
    due_html = ""
    if due:
        if due < today_str:
            due_html = '<span class="overdue">Overdue</span>'
        elif due == today_str:
            due_html = '<span class="today">Today</span>'
        else:
            due_html = due
    
    dept_short = dept.split(' ', 1)[-1] if ' ' in dept else dept
    meta_parts = [x for x in [due_html, dept_short if show_dept else None] if x]
    
    st.markdown(f"""
    <div class="task-item {'task-done' if done else ''}">
        <div class="task-priority priority-{p}"></div>
        <div class="task-content">
            <div class="task-title">{task['title']}</div>
            <div class="task-meta">{' · '.join(meta_parts)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Views
if view == "Today":
    if overdue:
        st.markdown('<div class="section-title">Overdue</div>', unsafe_allow_html=True)
        for t in sorted(overdue, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    if today_tasks:
        st.markdown('<div class="section-title">Due Today</div>', unsafe_allow_html=True)
        for t in sorted(today_tasks, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    upcoming = [t for t in open_tasks if t.get("due_date") and t.get("due_date") > today_str][:5]
    if upcoming:
        st.markdown('<div class="section-title">Upcoming</div>', unsafe_allow_html=True)
        for t in sorted(upcoming, key=lambda x: x.get("due_date")):
            show_task(t)
    
    if not overdue and not today_tasks:
        st.markdown('<div class="empty-state">Nothing due today ✨</div>', unsafe_allow_html=True)

elif view == "All":
    st.markdown('<div class="section-title">All Tasks</div>', unsafe_allow_html=True)
    for t in sorted(open_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
        show_task(t)

elif view == "Department":
    for dk, dn in dept_labels.items():
        dept_tasks = [t for t in open_tasks if t.get("department") == dk]
        if dept_tasks:
            with st.expander(f"{dn} ({len(dept_tasks)})"):
                for t in sorted(dept_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
                    show_task(t, show_dept=False)

elif view == "Done":
    if done_tasks:
        st.markdown('<div class="section-title">Completed</div>', unsafe_allow_html=True)
        for t in sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)[:30]:
            show_task(t)
    else:
        st.markdown('<div class="empty-state">No completed tasks yet</div>', unsafe_allow_html=True)
