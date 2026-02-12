"""
GTF Command Center v4
Clean, functional, works.
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

# Clean styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, sans-serif !important; }
    
    .main { background: #f8f9fc !important; }
    .block-container { padding: 2rem 2.5rem !important; max-width: 1200px !important; }
    
    #MainMenu, footer, .stDeployButton, header { visibility: hidden; }
    
    [data-testid="stSidebar"] { background: #fff !important; border-right: 1px solid #e5e7eb !important; }
    
    .stat-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-box {
        flex: 1;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.25rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #111;
    }
    
    .stat-number.red { color: #ef4444; }
    
    .stat-label {
        font-size: 0.7rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }
    
    .section-header {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .task-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #e5e7eb;
    }
    
    .task-card.high { border-left-color: #ef4444; }
    .task-card.medium { border-left-color: #f59e0b; }
    .task-card.low { border-left-color: #3b82f6; }
    
    .task-title {
        font-size: 0.9rem;
        font-weight: 500;
        color: #111;
        margin-bottom: 0.25rem;
    }
    
    .task-meta {
        font-size: 0.75rem;
        color: #9ca3af;
    }
    
    .task-meta .overdue { color: #ef4444; font-weight: 500; }
    .task-meta .today { color: #6366f1; font-weight: 500; }
    
    .task-done .task-title {
        text-decoration: line-through;
        color: #9ca3af;
    }
    
    .progress-bar-bg {
        height: 6px;
        background: #e5e7eb;
        border-radius: 3px;
        margin-bottom: 2rem;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366f1, #818cf8);
        border-radius: 3px;
    }
    
    .stRadio > div { flex-direction: row !important; gap: 0.5rem !important; }
    .stRadio label { 
        background: white !important; 
        border: 1px solid #e5e7eb !important; 
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        font-size: 0.85rem !important;
    }
    .stRadio label[data-checked="true"] { 
        background: #111 !important; 
        color: white !important;
        border-color: #111 !important;
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
    # Logo
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=150)
    else:
        st.markdown("### ✨ GTF")
    st.caption(datetime.now().strftime("%A, %b %d"))
    st.markdown("---")
    
    st.markdown("**Overview**")
    st.markdown(f"Open: **{len(open_tasks)}**")
    st.markdown(f"Due Today: **{len(today_tasks)}**")
    st.markdown(f"Overdue: **{len(overdue)}**")
    
    st.markdown("---")
    st.markdown("**Departments**")
    for dk, dn in dept_labels.items():
        c = len([t for t in open_tasks if t.get("department") == dk])
        if c > 0:
            st.markdown(f"{dn.split()[0]} {dn.split(' ', 1)[-1] if ' ' in dn else dn}: **{c}**", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("💬 Text Zoya to manage tasks")

# Header
st.markdown("## Command Center")
st.caption(f"{datetime.now().strftime('%A, %B %d, %Y')} · {len(done_tasks)}/{len(tasks)} tasks done ({progress:.0f}%)")

# Progress bar
st.markdown(f"""
<div class="progress-bar-bg">
    <div class="progress-bar-fill" style="width: {progress}%"></div>
</div>
""", unsafe_allow_html=True)

# Stats row
st.markdown(f"""
<div class="stat-container">
    <div class="stat-box">
        <div class="stat-number">{len(open_tasks)}</div>
        <div class="stat-label">Open Tasks</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">{len(today_tasks)}</div>
        <div class="stat-label">Due Today</div>
    </div>
    <div class="stat-box">
        <div class="stat-number {'red' if overdue else ''}">{len(overdue)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">{len(high_p)}</div>
        <div class="stat-label">High Priority</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
view = st.radio("View", ["Today", "All Tasks", "By Department", "Completed"], horizontal=True, label_visibility="collapsed")

def show_task(task, show_dept=True):
    p = task.get("priority", "medium")
    due = task.get("due_date")
    dept = dept_labels.get(task.get("department", "quick"), "Quick")
    done = task.get("done", False)
    
    due_html = ""
    if due:
        if due < today_str:
            due_html = f'<span class="overdue">⚠️ Overdue</span>'
        elif due == today_str:
            due_html = f'<span class="today">📍 Today</span>'
        else:
            due_html = f'📅 {due}'
    
    dept_short = dept.split(' ', 1)[-1] if ' ' in dept else dept
    
    st.markdown(f"""
    <div class="task-card {p} {'task-done' if done else ''}">
        <div class="task-title">{task['title']}</div>
        <div class="task-meta">{due_html} {'· ' + dept_short if show_dept else ''}</div>
    </div>
    """, unsafe_allow_html=True)

# Views
if view == "Today":
    if overdue:
        st.markdown('<div class="section-header">⚠️ Overdue</div>', unsafe_allow_html=True)
        for t in sorted(overdue, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    if today_tasks:
        st.markdown('<div class="section-header">📍 Due Today</div>', unsafe_allow_html=True)
        for t in sorted(today_tasks, key=lambda x: x.get("priority") != "high"):
            show_task(t)
    
    upcoming = [t for t in open_tasks if t.get("due_date") and t.get("due_date") > today_str][:5]
    if upcoming:
        st.markdown('<div class="section-header">📅 Coming Up</div>', unsafe_allow_html=True)
        for t in sorted(upcoming, key=lambda x: x.get("due_date")):
            show_task(t)
    
    if not overdue and not today_tasks:
        st.info("✨ Nothing due today!")

elif view == "All Tasks":
    st.markdown('<div class="section-header">📋 All Open Tasks</div>', unsafe_allow_html=True)
    for t in sorted(open_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
        show_task(t)

elif view == "By Department":
    for dk, dn in dept_labels.items():
        dept_tasks = [t for t in open_tasks if t.get("department") == dk]
        if dept_tasks:
            with st.expander(f"{dn} ({len(dept_tasks)})", expanded=False):
                for t in sorted(dept_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
                    show_task(t, show_dept=False)

elif view == "Completed":
    if done_tasks:
        st.markdown('<div class="section-header">✅ Completed</div>', unsafe_allow_html=True)
        for t in sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)[:30]:
            show_task(t)
    else:
        st.info("💪 No completed tasks yet")
