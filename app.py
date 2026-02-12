"""
GTF Command Center v16
Drag tasks between calendar days
"""

import streamlit as st
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from streamlit_sortables import sort_items

st.set_page_config(
    page_title="GTF Command Center",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"departments": [], "department_labels": {}, "tasks": []}

def save_tasks(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, default=str))

data = load_tasks()
tasks = data.get("tasks", [])
dept_labels = data.get("department_labels", {})
today = date.today()
today_str = today.isoformat()

# Department colors
dept_colors = {
    "customers": "#8B5CF6",
    "customs_shipping": "#0891B2",
    "brand_outreach": "#059669",
    "brand_followups": "#10B981",
    "content": "#EC4899",
    "legal": "#6366F1",
    "product": "#3B82F6",
    "business": "#F59E0B",
    "fundraising": "#EF4444",
    "hiring": "#8B5CF6",
    "finance": "#14B8A6",
    "quick": "#6B7280"
}

if "show_calendar" not in st.session_state:
    st.session_state.show_calendar = False
if "expanded_day" not in st.session_state:
    st.session_state.expanded_day = None

# Styling
st.markdown("""
<style>
    :root {
        --cream: #FAFAF8;
        --white: #FFFFFF;
        --charcoal: #1a1a1a;
        --gray: #6b6b6b;
        --light-gray: #e5e5e5;
        --red: #EF4444;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
        background-color: var(--cream) !important;
    }
    
    .main .block-container {
        background-color: var(--cream) !important;
        padding: 1.5rem 2rem !important;
        max-width: 100% !important;
    }
    
    section[data-testid="stSidebar"] { display: none !important; }
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    
    .stats-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-box {
        background: var(--white);
        border: 1px solid var(--light-gray);
        padding: 1rem 1.5rem;
        text-align: center;
        flex: 1;
    }
    
    .stat-num { font-size: 1.75rem; font-weight: 600; color: var(--charcoal); }
    .stat-num.red { color: var(--red); }
    .stat-label { font-size: 0.65rem; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; }
    
    .day-column {
        background: var(--white);
        border: 1px solid var(--light-gray);
        border-radius: 8px;
        padding: 0.75rem;
        min-height: 200px;
    }
    
    .day-header {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--charcoal);
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--light-gray);
    }
    
    .day-header.today {
        color: var(--red);
    }
    
    .day-date {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .task-chip {
        padding: 6px 10px;
        border-radius: 4px;
        margin-bottom: 4px;
        font-size: 0.75rem;
        color: white;
        cursor: grab;
    }
    
    .section-head {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .task-card {
        background: var(--white);
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.4rem;
        border-left: 3px solid #ccc;
    }
    
    .expand-btn {
        font-size: 0.7rem;
        color: var(--gray);
        cursor: pointer;
        padding: 4px 8px;
        background: var(--light-gray);
        border-radius: 4px;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Stats
open_tasks = [t for t in tasks if not t.get("done")]
done_tasks = [t for t in tasks if t.get("done")]
today_tasks = [t for t in open_tasks if t.get("due_date") == today_str]
overdue = [t for t in open_tasks if t.get("due_date") and t.get("due_date") < today_str]

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("## GTF Command Center")
with col2:
    if st.button("📅 Calendar View" if not st.session_state.show_calendar else "📋 List View", use_container_width=True):
        st.session_state.show_calendar = not st.session_state.show_calendar
        st.rerun()

# Stats
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box"><div class="stat-num">{len(open_tasks)}</div><div class="stat-label">Open</div></div>
    <div class="stat-box"><div class="stat-num">{len(today_tasks)}</div><div class="stat-label">Today</div></div>
    <div class="stat-box"><div class="stat-num {'red' if overdue else ''}">{len(overdue)}</div><div class="stat-label">Overdue</div></div>
    <div class="stat-box"><div class="stat-num">{len(done_tasks)}</div><div class="stat-label">Done</div></div>
</div>
""", unsafe_allow_html=True)

if st.session_state.show_calendar:
    # Calendar drag-and-drop view
    st.markdown("**Drag tasks between days to reschedule**")
    
    # Show 7 days starting from today - 2
    start_date = today - timedelta(days=2)
    days = [(start_date + timedelta(days=i)) for i in range(7)]
    
    # Build containers for each day
    day_containers = {}
    task_id_map = {}  # Map display text to task id
    
    for d in days:
        d_str = d.isoformat()
        day_tasks = [t for t in open_tasks if t.get("due_date") == d_str]
        day_tasks = sorted(day_tasks, key=lambda x: x.get("order", 999))
        
        items = []
        for t in day_tasks:
            dk = t.get("department", "quick")
            # Short label for dragging
            label = t["title"][:40] + ("..." if len(t["title"]) > 40 else "")
            items.append(label)
            task_id_map[label] = t["id"]
        
        day_name = d.strftime("%a")
        if d == today:
            day_name = "Today"
        elif d == today - timedelta(days=1):
            day_name = "Yesterday"
        elif d == today + timedelta(days=1):
            day_name = "Tomorrow"
        
        day_containers[f"{day_name} {d.day}"] = items
    
    # Sort with multi-container
    sorted_containers = sort_items(day_containers, multi_containers=True, direction="vertical")
    
    # Check for changes and update due dates
    container_to_date = {}
    for i, d in enumerate(days):
        day_name = d.strftime("%a")
        if d == today:
            day_name = "Today"
        elif d == today - timedelta(days=1):
            day_name = "Yesterday"
        elif d == today + timedelta(days=1):
            day_name = "Tomorrow"
        container_to_date[f"{day_name} {d.day}"] = d.isoformat()
    
    # Detect if any task moved
    changes_made = False
    for container_name, item_list in sorted_containers.items():
        new_date = container_to_date.get(container_name)
        if new_date:
            for item in item_list:
                task_id = task_id_map.get(item)
                if task_id:
                    # Find current task date
                    for t in data["tasks"]:
                        if t["id"] == task_id and t.get("due_date") != new_date:
                            t["due_date"] = new_date
                            changes_made = True
    
    if changes_made:
        save_tasks(data)
        st.rerun()
    
    # Also show overdue tasks
    if overdue:
        st.markdown("---")
        st.markdown("**⚠️ Overdue (drag to a day above to reschedule)**")
        
        overdue_items = [t["title"][:40] + ("..." if len(t["title"]) > 40 else "") for t in overdue]
        for t in overdue:
            label = t["title"][:40] + ("..." if len(t["title"]) > 40 else "")
            task_id_map[label] = t["id"]
        
        # Show as sortable too
        sorted_overdue = sort_items(overdue_items, direction="vertical")

else:
    # List view
    view = st.radio("", ["Today", "All", "Done"], horizontal=True, label_visibility="collapsed")
    
    def render_task(task):
        dk = task.get("department", "quick")
        dept = dept_labels.get(dk, "Quick")
        color = dept_colors.get(dk, "#6B7280")
        due = task.get("due_date")
        priority = task.get("priority", "medium")
        
        due_text = ""
        if due:
            if due < today_str:
                due_text = "⚠️ OVERDUE"
            elif due == today_str:
                due_text = "Today"
            else:
                due_text = due
        
        col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
        
        with col1:
            done = st.checkbox("", value=task.get("done", False), key=f"done_{task['id']}")
            if done != task.get("done", False):
                for t in data["tasks"]:
                    if t["id"] == task["id"]:
                        t["done"] = done
                        if done:
                            t["completed_date"] = today_str
                save_tasks(data)
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="task-card" style="border-left-color: {color};">
                <strong>{task['title']}</strong><br>
                <small style="color: #888;">{dept} · {due_text} · {priority}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            with st.popover("Edit"):
                new_due = st.date_input("Due", 
                    value=date.fromisoformat(task["due_date"]) if task.get("due_date") else None, 
                    key=f"due_{task['id']}")
                new_priority = st.selectbox("Priority", ["high", "medium", "low"], 
                    index=["high", "medium", "low"].index(task.get("priority", "medium")),
                    key=f"pri_{task['id']}")
                new_notes = st.text_area("Notes", value=task.get("notes", ""), 
                    key=f"notes_{task['id']}", height=60)
                
                if st.button("Save", key=f"save_{task['id']}"):
                    for t in data["tasks"]:
                        if t["id"] == task["id"]:
                            t["due_date"] = new_due.isoformat() if new_due else None
                            t["priority"] = new_priority
                            t["notes"] = new_notes
                    save_tasks(data)
                    st.rerun()
    
    if view == "Today":
        all_today = overdue + today_tasks
        all_today = sorted(all_today, key=lambda x: (x.get("order", 999), x.get("priority") != "high"))
        
        if all_today:
            st.markdown('<div class="section-head">Today</div>', unsafe_allow_html=True)
            for task in all_today:
                render_task(task)
        else:
            st.info("Nothing due today")
    
    elif view == "All":
        sorted_tasks = sorted(open_tasks, key=lambda x: (x.get("due_date") or "9999", x.get("priority") != "high"))
        
        if sorted_tasks:
            st.markdown('<div class="section-head">All Tasks</div>', unsafe_allow_html=True)
            for task in sorted_tasks:
                render_task(task)
    
    elif view == "Done":
        if done_tasks:
            st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
            for task in done_tasks[:30]:
                st.markdown(f"~~{task['title']}~~")
        else:
            st.info("No completed tasks")
