"""
GTF Command Center
Clean. Minimal. Get shit done.
"""

import streamlit as st
import json
from datetime import datetime, date, timedelta
from pathlib import Path

st.set_page_config(
    page_title="GTF Tasks",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"departments": [], "department_labels": {}, "tasks": []}

data = load_tasks()
tasks = data.get("tasks", [])
dept_labels = data.get("department_labels", {})

# Clean minimal CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background: #fafafa; }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1200px;
    }
    
    h1 { 
        font-weight: 600 !important; 
        font-size: 1.8rem !important;
        color: #111 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .subtitle {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    .stat-row {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-box {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        min-width: 120px;
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 600;
        color: #111;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .section-title {
        font-size: 0.85rem;
        font-weight: 500;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #eee;
    }
    
    .task-item {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.15s ease;
    }
    
    .task-item:hover {
        border-color: #ccc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .task-done {
        opacity: 0.5;
        text-decoration: line-through;
    }
    
    .task-title {
        font-size: 0.9rem;
        color: #222;
        font-weight: 400;
    }
    
    .task-meta {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.25rem;
    }
    
    .priority-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
    }
    
    .priority-high { background: #ef4444; }
    .priority-medium { background: #f59e0b; }
    .priority-low { background: #3b82f6; }
    
    .overdue { color: #ef4444 !important; font-weight: 500; }
    
    .dept-badge {
        font-size: 0.7rem;
        background: #f3f4f6;
        color: #666;
        padding: 2px 8px;
        border-radius: 4px;
        margin-left: 8px;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #999;
    }
    
    /* Hide streamlit stuff */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Clean up expanders */
    .streamlit-expanderHeader {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Radio buttons as tabs */
    .stRadio > div {
        display: flex;
        gap: 0.5rem;
    }
    
    .stRadio label {
        background: white !important;
        border: 1px solid #e5e5e5 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
    }
    
    .stRadio label[data-checked="true"] {
        background: #111 !important;
        color: white !important;
        border-color: #111 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
today_str = date.today().isoformat()
st.markdown("# ✨ GTF Command Center")
st.markdown(f'<p class="subtitle">{datetime.now().strftime("%A, %B %d")}</p>', unsafe_allow_html=True)

# Stats
open_tasks = [t for t in tasks if not t.get("done")]
today_tasks = [t for t in open_tasks if t.get("due_date") == today_str]
overdue = [t for t in open_tasks if t.get("due_date") and t.get("due_date") < today_str]
high_p = [t for t in open_tasks if t.get("priority") == "high"]

st.markdown(f"""
<div class="stat-row">
    <div class="stat-box">
        <div class="stat-number">{len(open_tasks)}</div>
        <div class="stat-label">Open</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">{len(today_tasks)}</div>
        <div class="stat-label">Today</div>
    </div>
    <div class="stat-box">
        <div class="stat-number" style="color: {'#ef4444' if overdue else '#111'}">{len(overdue)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">{len(high_p)}</div>
        <div class="stat-label">High Priority</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
view = st.radio("", ["Today", "All Tasks", "By Department", "Completed"], horizontal=True, label_visibility="collapsed")

def render_task(task, show_dept=True):
    priority = task.get("priority", "medium")
    due = task.get("due_date")
    dept = dept_labels.get(task.get("department", "quick"), "Quick")
    
    due_text = ""
    is_overdue = False
    if due:
        if due < today_str:
            due_text = f"Overdue"
            is_overdue = True
        elif due == today_str:
            due_text = "Today"
        else:
            due_text = due
    
    st.markdown(f"""
    <div class="task-item {'task-done' if task.get('done') else ''}">
        <div>
            <span class="priority-dot priority-{priority}"></span>
            <span class="task-title">{task['title']}</span>
            {f'<span class="dept-badge">{dept.split(" ", 1)[-1] if " " in dept else dept}</span>' if show_dept else ''}
            <div class="task-meta {'overdue' if is_overdue else ''}">{due_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Views
if view == "Today":
    if overdue:
        st.markdown('<div class="section-title">⚠️ Overdue</div>', unsafe_allow_html=True)
        for task in sorted(overdue, key=lambda x: x.get("priority") != "high"):
            render_task(task)
    
    if today_tasks:
        st.markdown('<div class="section-title">📍 Due Today</div>', unsafe_allow_html=True)
        for task in sorted(today_tasks, key=lambda x: x.get("priority") != "high"):
            render_task(task)
    
    if not today_tasks and not overdue:
        st.markdown('<div class="empty-state">Nothing due today ✨</div>', unsafe_allow_html=True)

elif view == "All Tasks":
    st.markdown('<div class="section-title">All Open Tasks</div>', unsafe_allow_html=True)
    
    for task in sorted(open_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
        render_task(task)
    
    if not open_tasks:
        st.markdown('<div class="empty-state">No open tasks</div>', unsafe_allow_html=True)

elif view == "By Department":
    cols = st.columns(2)
    
    for i, (dept_key, dept_name) in enumerate(dept_labels.items()):
        dept_tasks = [t for t in open_tasks if t.get("department") == dept_key]
        
        with cols[i % 2]:
            with st.expander(f"{dept_name} ({len(dept_tasks)})", expanded=False):
                if dept_tasks:
                    for task in sorted(dept_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
                        render_task(task, show_dept=False)
                else:
                    st.markdown("*No tasks*")

elif view == "Completed":
    done_tasks = [t for t in tasks if t.get("done")]
    done_tasks = sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)
    
    st.markdown('<div class="section-title">Completed</div>', unsafe_allow_html=True)
    
    if done_tasks:
        for task in done_tasks[:30]:
            render_task(task)
    else:
        st.markdown('<div class="empty-state">Nothing completed yet. Get to work 💪</div>', unsafe_allow_html=True)

# Footer tip
st.markdown("---")
st.markdown("*💬 Text Zoya to add tasks, mark done, or ask \"what's on my plate?\"*")
