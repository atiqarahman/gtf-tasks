"""
GTF Command Center v3
Inspired by Linear, Notion, Asana
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

# Modern SaaS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fc;
        --bg-hover: #f3f4f8;
        --border: #e6e8eb;
        --text-primary: #1a1a2e;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --accent: #6366f1;
        --accent-light: #eef2ff;
        --danger: #ef4444;
        --warning: #f59e0b;
        --success: #10b981;
    }
    
    * { font-family: 'Inter', -apple-system, sans-serif !important; }
    
    .main { background: var(--bg-secondary) !important; }
    
    .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1400px !important;
    }
    
    /* Hide default streamlit */
    #MainMenu, footer, .stDeployButton, header { visibility: hidden; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--bg-primary) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1rem !important;
    }
    
    /* Header */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .header-date {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        border-color: var(--accent);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    
    .stat-value.danger { color: var(--danger); }
    .stat-value.warning { color: var(--warning); }
    .stat-value.success { color: var(--success); }
    
    .stat-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    /* Section */
    .section {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin-bottom: 1rem;
        overflow: hidden;
    }
    
    .section-header {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .section-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-count {
        background: var(--bg-secondary);
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 500;
        padding: 0.125rem 0.5rem;
        border-radius: 10px;
    }
    
    /* Task row */
    .task-row {
        display: flex;
        align-items: center;
        padding: 0.875rem 1.25rem;
        border-bottom: 1px solid var(--border);
        transition: background 0.15s ease;
        cursor: pointer;
    }
    
    .task-row:last-child { border-bottom: none; }
    .task-row:hover { background: var(--bg-hover); }
    
    .task-checkbox {
        width: 18px;
        height: 18px;
        border: 2px solid var(--border);
        border-radius: 4px;
        margin-right: 0.875rem;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.15s ease;
    }
    
    .task-checkbox:hover {
        border-color: var(--accent);
        background: var(--accent-light);
    }
    
    .task-checkbox.checked {
        background: var(--success);
        border-color: var(--success);
    }
    
    .task-content { flex: 1; min-width: 0; }
    
    .task-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 0.125rem;
    }
    
    .task-title.done {
        color: var(--text-muted);
        text-decoration: line-through;
    }
    
    .task-meta {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.75rem;
        color: var(--text-muted);
    }
    
    .task-due { 
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .task-due.overdue { color: var(--danger); font-weight: 500; }
    .task-due.today { color: var(--accent); font-weight: 500; }
    
    /* Priority indicator */
    .priority-bar {
        width: 3px;
        height: 24px;
        border-radius: 2px;
        margin-right: 0.875rem;
        flex-shrink: 0;
    }
    
    .priority-high { background: var(--danger); }
    .priority-medium { background: var(--warning); }
    .priority-low { background: #3b82f6; }
    
    /* Department badge */
    .dept-badge {
        font-size: 0.7rem;
        font-weight: 500;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        background: var(--bg-secondary);
        color: var(--text-secondary);
    }
    
    /* Progress bar */
    .progress-container {
        margin-bottom: 2rem;
    }
    
    .progress-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .progress-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    .progress-bar {
        height: 6px;
        background: var(--bg-secondary);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--accent), #818cf8);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    /* Empty state */
    .empty-state {
        padding: 3rem;
        text-align: center;
        color: var(--text-muted);
    }
    
    .empty-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* View tabs */
    .view-tabs {
        display: flex;
        gap: 0.25rem;
        background: var(--bg-secondary);
        padding: 0.25rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        width: fit-content;
    }
    
    .view-tab {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--text-secondary);
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    
    .view-tab:hover { color: var(--text-primary); }
    .view-tab.active {
        background: var(--bg-primary);
        color: var(--text-primary);
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    /* Streamlit overrides */
    .stRadio > div {
        gap: 0.25rem !important;
        background: var(--bg-secondary) !important;
        padding: 0.25rem !important;
        border-radius: 8px !important;
        width: fit-content !important;
    }
    
    .stRadio label {
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        border: none !important;
        background: transparent !important;
    }
    
    .stRadio label[data-checked="true"] {
        background: var(--bg-primary) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }
    
    div[data-baseweb="select"] { font-size: 0.85rem !important; }
    
    .stExpander {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        margin-bottom: 0.75rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Calculate stats
open_tasks = [t for t in tasks if not t.get("done")]
done_tasks = [t for t in tasks if t.get("done")]
today_tasks = [t for t in open_tasks if t.get("due_date") == today_str]
overdue = [t for t in open_tasks if t.get("due_date") and t.get("due_date") < today_str]
high_p = [t for t in open_tasks if t.get("priority") == "high"]

total_tasks = len(tasks)
done_count = len(done_tasks)
progress = (done_count / total_tasks * 100) if total_tasks > 0 else 0

# Sidebar
with st.sidebar:
    st.markdown("### ✨ GTF")
    st.markdown(f"*{datetime.now().strftime('%a, %b %d')}*")
    
    st.markdown("---")
    
    st.markdown("**Quick Stats**")
    st.metric("Open Tasks", len(open_tasks))
    st.metric("Due Today", len(today_tasks))
    st.metric("Overdue", len(overdue))
    
    st.markdown("---")
    
    st.markdown("**Departments**")
    for dept_key, dept_name in dept_labels.items():
        count = len([t for t in open_tasks if t.get("department") == dept_key])
        if count > 0:
            st.markdown(f"<small>{dept_name}: **{count}**</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<small>💬 *Text Zoya to manage tasks*</small>", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="header-container">
    <div>
        <div class="header-title">Command Center</div>
        <div class="header-date">{datetime.now().strftime('%A, %B %d, %Y')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Progress bar
st.markdown(f"""
<div class="progress-container">
    <div class="progress-header">
        <span class="progress-label">Overall Progress</span>
        <span class="progress-label">{done_count}/{total_tasks} tasks ({progress:.0f}%)</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats cards
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-value">{len(open_tasks)}</div>
        <div class="stat-label">Open Tasks</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{len(today_tasks)}</div>
        <div class="stat-label">Due Today</div>
    </div>
    <div class="stat-card">
        <div class="stat-value {'danger' if overdue else ''}">{len(overdue)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{len(high_p)}</div>
        <div class="stat-label">High Priority</div>
    </div>
</div>
""", unsafe_allow_html=True)

# View selector
view = st.radio("View", ["Today", "All Tasks", "By Department", "Completed"], horizontal=True, label_visibility="collapsed")

def render_task_row(task, show_dept=True):
    priority = task.get("priority", "medium")
    due = task.get("due_date")
    dept = dept_labels.get(task.get("department", "quick"), "Quick")
    is_done = task.get("done", False)
    
    due_class = ""
    due_text = ""
    if due:
        if due < today_str:
            due_text = "⚠️ Overdue"
            due_class = "overdue"
        elif due == today_str:
            due_text = "📍 Today"
            due_class = "today"
        else:
            due_text = f"📅 {due}"
    
    dept_clean = dept.split(" ", 1)[-1] if " " in dept else dept
    
    st.markdown(f"""
    <div class="task-row">
        <div class="priority-bar priority-{priority}"></div>
        <div class="task-checkbox {'checked' if is_done else ''}">
            {'✓' if is_done else ''}
        </div>
        <div class="task-content">
            <div class="task-title {'done' if is_done else ''}">{task['title']}</div>
            <div class="task-meta">
                {f'<span class="task-due {due_class}">{due_text}</span>' if due_text else ''}
                {f'<span class="dept-badge">{dept_clean}</span>' if show_dept else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_section(title, task_list, show_dept=True, icon=""):
    if not task_list:
        return
        
    st.markdown(f"""
    <div class="section">
        <div class="section-header">
            <div class="section-title">{icon} {title} <span class="section-count">{len(task_list)}</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    for task in task_list:
        render_task_row(task, show_dept)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Render views
if view == "Today":
    if overdue:
        render_section("Overdue", sorted(overdue, key=lambda x: x.get("priority") != "high"), icon="⚠️")
    
    if today_tasks:
        render_section("Due Today", sorted(today_tasks, key=lambda x: x.get("priority") != "high"), icon="📍")
    
    upcoming = [t for t in open_tasks if t.get("due_date") and t.get("due_date") > today_str][:5]
    if upcoming:
        render_section("Coming Up", sorted(upcoming, key=lambda x: x.get("due_date")), icon="📅")
    
    if not overdue and not today_tasks:
        st.markdown("""
        <div class="section">
            <div class="empty-state">
                <div class="empty-icon">✨</div>
                <div>Nothing due today. You're all caught up!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif view == "All Tasks":
    render_section("All Open Tasks", sorted(open_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")), icon="📋")

elif view == "By Department":
    for dept_key, dept_name in dept_labels.items():
        dept_tasks = [t for t in open_tasks if t.get("department") == dept_key]
        if dept_tasks:
            with st.expander(f"{dept_name} ({len(dept_tasks)})", expanded=False):
                for task in sorted(dept_tasks, key=lambda x: (x.get("priority") != "high", x.get("due_date") or "9999")):
                    render_task_row(task, show_dept=False)

elif view == "Completed":
    if done_tasks:
        render_section("Completed", sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)[:30], icon="✅")
    else:
        st.markdown("""
        <div class="section">
            <div class="empty-state">
                <div class="empty-icon">💪</div>
                <div>No completed tasks yet. Get to work!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
