"""
GTF Task Command Center
Your brain, but organized.
"""

import streamlit as st
import json
from datetime import datetime, date, timedelta
from pathlib import Path

# Config
st.set_page_config(
    page_title="GTF Tasks",
    page_icon="✨",
    layout="wide"
)

# Data file - use GitHub raw or local
DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"departments": [], "department_labels": {}, "tasks": []}

def save_tasks(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, default=str))

# Load data
data = load_tasks()
tasks = data.get("tasks", [])
dept_labels = data.get("department_labels", {})

# Custom CSS
st.markdown("""
<style>
    .task-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #e91e63;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .task-done {
        border-left-color: #4caf50;
        opacity: 0.6;
    }
    .priority-high { border-left-color: #f44336; }
    .priority-medium { border-left-color: #ff9800; }
    .priority-low { border-left-color: #2196f3; }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    .stat-number { font-size: 36px; font-weight: bold; }
    .stat-label { font-size: 14px; opacity: 0.9; }
    .today-banner {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# ✨ GTF Command Center")
st.markdown(f"*{datetime.now().strftime('%A, %B %d, %Y')}*")

# Today's focus banner
today_str = date.today().isoformat()
today_tasks = [t for t in tasks if not t.get("done") and t.get("due_date") == today_str]
overdue_tasks = [t for t in tasks if not t.get("done") and t.get("due_date") and t.get("due_date") < today_str]

if today_tasks or overdue_tasks:
    st.markdown(f"""
    <div class="today-banner">
        <h2 style="margin:0;">🎯 Today's Focus</h2>
        <p style="margin:5px 0 0 0; font-size: 18px;">
            {len(today_tasks)} task{'s' if len(today_tasks) != 1 else ''} for today
            {f' • {len(overdue_tasks)} overdue!' if overdue_tasks else ''}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Stats row
col1, col2, col3, col4 = st.columns(4)

total_tasks = len([t for t in tasks if not t.get("done")])
done_today = len([t for t in tasks if t.get("done") and t.get("completed_date") == today_str])
high_priority = len([t for t in tasks if not t.get("done") and t.get("priority") == "high"])

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_tasks}</div>
        <div class="stat-label">Open Tasks</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
        <div class="stat-number">{done_today}</div>
        <div class="stat-label">Done Today</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);">
        <div class="stat-number">{high_priority}</div>
        <div class="stat-label">High Priority</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);">
        <div class="stat-number">{len(overdue_tasks)}</div>
        <div class="stat-label">Overdue</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# View selector
view = st.radio("View", ["📅 Today", "🗂️ By Department", "⚡ All Tasks", "✅ Completed"], horizontal=True)

def render_task(task, show_dept=True):
    priority_class = f"priority-{task.get('priority', 'medium')}"
    done_class = "task-done" if task.get("done") else ""
    dept = dept_labels.get(task.get("department", "quick"), "⚡ Quick")
    
    due = ""
    if task.get("due_date"):
        due_date = task["due_date"]
        if due_date < today_str:
            due = f"🔴 Overdue ({due_date})"
        elif due_date == today_str:
            due = "📍 Today"
        else:
            due = f"📅 {due_date}"
    
    priority_emoji = {"high": "🔥", "medium": "➡️", "low": "💤"}.get(task.get("priority", "medium"), "")
    
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown(f"""
        <div class="task-card {priority_class} {done_class}">
            <strong>{task['title']}</strong><br>
            <small>{dept if show_dept else ''} {priority_emoji} {due}</small>
            {f"<br><small style='color:#666'>{task.get('notes', '')}</small>" if task.get('notes') else ''}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if not task.get("done"):
            if st.button("✓", key=f"done_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["done"] = True
                        t["completed_date"] = today_str
                save_tasks(data)
                st.rerun()

# Views
if view == "📅 Today":
    st.markdown("### 🌅 Today's Tasks")
    
    if overdue_tasks:
        st.markdown("#### 🔴 Overdue")
        for task in sorted(overdue_tasks, key=lambda x: x.get("priority", "medium") == "high", reverse=True):
            render_task(task)
    
    if today_tasks:
        st.markdown("#### 📍 Due Today")
        for task in sorted(today_tasks, key=lambda x: x.get("priority", "medium") == "high", reverse=True):
            render_task(task)
    
    if not today_tasks and not overdue_tasks:
        st.info("🎉 Nothing due today! Check 'All Tasks' or add something.")

elif view == "🗂️ By Department":
    # Two columns of departments
    cols = st.columns(2)
    
    for i, (dept_key, dept_name) in enumerate(dept_labels.items()):
        dept_tasks = [t for t in tasks if not t.get("done") and t.get("department") == dept_key]
        
        with cols[i % 2]:
            with st.expander(f"{dept_name} ({len(dept_tasks)})", expanded=len(dept_tasks) > 0):
                if dept_tasks:
                    for task in sorted(dept_tasks, key=lambda x: (x.get("priority", "medium") != "high", x.get("due_date") or "9999")):
                        render_task(task, show_dept=False)
                else:
                    st.markdown("*No tasks*")

elif view == "⚡ All Tasks":
    st.markdown("### All Open Tasks")
    
    open_tasks = [t for t in tasks if not t.get("done")]
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_dept = st.selectbox("Filter by department", ["All"] + list(dept_labels.values()))
    with col2:
        filter_priority = st.selectbox("Filter by priority", ["All", "🔥 High", "➡️ Medium", "💤 Low"])
    
    for task in sorted(open_tasks, key=lambda x: (x.get("priority", "medium") != "high", x.get("due_date") or "9999")):
        dept_match = filter_dept == "All" or dept_labels.get(task.get("department")) == filter_dept
        priority_map = {"🔥 High": "high", "➡️ Medium": "medium", "💤 Low": "low"}
        priority_match = filter_priority == "All" or task.get("priority") == priority_map.get(filter_priority)
        
        if dept_match and priority_match:
            render_task(task)

elif view == "✅ Completed":
    st.markdown("### Completed Tasks")
    
    done_tasks = [t for t in tasks if t.get("done")]
    done_tasks = sorted(done_tasks, key=lambda x: x.get("completed_date", ""), reverse=True)
    
    if done_tasks:
        for task in done_tasks[:50]:  # Show last 50
            render_task(task)
    else:
        st.info("No completed tasks yet. Get to work! 💪")

# Sidebar - Quick Add
st.sidebar.markdown("## ➕ Quick Add")

with st.sidebar.form("add_task"):
    new_title = st.text_input("Task")
    new_dept = st.selectbox("Department", options=list(dept_labels.keys()), format_func=lambda x: dept_labels[x])
    new_priority = st.select_slider("Priority", options=["low", "medium", "high"], value="medium")
    new_due = st.date_input("Due date", value=None)
    new_notes = st.text_area("Notes (optional)", height=68)
    
    if st.form_submit_button("Add Task"):
        if new_title:
            new_task = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "title": new_title,
                "department": new_dept,
                "priority": new_priority,
                "due_date": new_due.isoformat() if new_due else None,
                "notes": new_notes,
                "done": False,
                "created": datetime.now().isoformat()
            }
            data["tasks"].append(new_task)
            save_tasks(data)
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Pro tip")
st.sidebar.markdown("*Just text Zoya to add tasks! Say things like:*")
st.sidebar.markdown("- 'Add task: follow up with X brand'")
st.sidebar.markdown("- 'Done with shipping research'")
st.sidebar.markdown("- 'What's on my plate today?'")
