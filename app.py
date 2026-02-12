"""
GTF Command Center v17
Fixed multi-container format + sidebar restored
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
    initial_sidebar_state="expanded"
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
if "selected_dept" not in st.session_state:
    st.session_state.selected_dept = None

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
        max-width: 1200px !important;
    }
    
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: var(--white) !important;
    }
    
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
    
    .day-col {
        background: var(--white);
        border: 1px solid var(--light-gray);
        border-radius: 8px;
        padding: 0.75rem;
        min-height: 150px;
    }
    
    .day-title {
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--light-gray);
    }
    
    .day-title.today { color: var(--red); }
</style>
""", unsafe_allow_html=True)

# Stats
open_tasks = [t for t in tasks if not t.get("done")]
done_tasks = [t for t in tasks if t.get("done")]
today_tasks = [t for t in open_tasks if t.get("due_date") == today_str]
overdue = [t for t in open_tasks if t.get("due_date") and t.get("due_date") < today_str]
high_p = [t for t in open_tasks if t.get("priority") == "high"]

def filter_tasks(task_list):
    if st.session_state.selected_dept:
        return [t for t in task_list if t.get("department") == st.session_state.selected_dept]
    return task_list

# Sidebar
with st.sidebar:
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=140)
    
    st.markdown("**Overview**")
    st.write(f"Open: {len(open_tasks)}")
    st.write(f"Today: {len(today_tasks)}")
    st.write(f"Overdue: {len(overdue)}")
    
    st.markdown("---")
    st.markdown("**Departments**")
    
    if st.button("All Departments", use_container_width=True):
        st.session_state.selected_dept = None
        st.rerun()
    
    for dk, dn in dept_labels.items():
        c = len([t for t in open_tasks if t.get("department") == dk])
        if c > 0:
            if st.button(f"{dn} ({c})", key=f"dept_{dk}", use_container_width=True):
                st.session_state.selected_dept = dk
                st.rerun()
    
    st.markdown("---")
    st.caption("Text Zoya to manage tasks")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("## Command Center")
with col2:
    if st.button("📅 Calendar" if not st.session_state.show_calendar else "📋 List", use_container_width=True):
        st.session_state.show_calendar = not st.session_state.show_calendar
        st.rerun()

# Stats
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box"><div class="stat-num">{len(open_tasks)}</div><div class="stat-label">Open</div></div>
    <div class="stat-box"><div class="stat-num">{len(today_tasks)}</div><div class="stat-label">Today</div></div>
    <div class="stat-box"><div class="stat-num {'red' if overdue else ''}">{len(overdue)}</div><div class="stat-label">Overdue</div></div>
    <div class="stat-box"><div class="stat-num">{len(high_p)}</div><div class="stat-label">Priority</div></div>
</div>
""", unsafe_allow_html=True)

if st.session_state.selected_dept:
    st.info(f"Filtered: {dept_labels.get(st.session_state.selected_dept, '')}")

if st.session_state.show_calendar:
    # Calendar view - 7 day columns
    st.markdown("**Drag tasks between days to reschedule**")
    
    # Create 7 day columns
    days = [(today + timedelta(days=i-1)) for i in range(7)]  # Yesterday through 5 days out
    cols = st.columns(7)
    
    task_id_map = {}
    
    for i, d in enumerate(days):
        d_str = d.isoformat()
        day_tasks = [t for t in filter_tasks(open_tasks) if t.get("due_date") == d_str]
        
        day_name = d.strftime("%a")
        if d == today:
            day_name = "TODAY"
        elif d == today - timedelta(days=1):
            day_name = "Yesterday"
        elif d == today + timedelta(days=1):
            day_name = "Tomorrow"
        
        with cols[i]:
            title_class = "day-title today" if d == today else "day-title"
            st.markdown(f'<div class="{title_class}">{day_name}<br><span style="font-size:1.2rem">{d.day}</span></div>', unsafe_allow_html=True)
            
            if day_tasks:
                items = []
                for t in day_tasks:
                    dk = t.get("department", "quick")
                    color = dept_colors.get(dk, "#6B7280")
                    label = t["title"][:25] + "..." if len(t["title"]) > 25 else t["title"]
                    items.append(label)
                    task_id_map[label] = {"id": t["id"], "date": d_str}
                
                sorted_items = sort_items(items, direction="vertical")
            else:
                st.caption("No tasks")
    
    # Quick reschedule tool
    st.markdown("---")
    st.markdown("**Quick Reschedule**")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        task_options = {t["title"]: t["id"] for t in filter_tasks(open_tasks)}
        selected = st.selectbox("Task", list(task_options.keys()), label_visibility="collapsed")
    with col2:
        new_date = st.date_input("To", value=today, label_visibility="collapsed")
    with col3:
        if st.button("Move", use_container_width=True):
            tid = task_options.get(selected)
            if tid:
                for t in data["tasks"]:
                    if t["id"] == tid:
                        t["due_date"] = new_date.isoformat()
                save_tasks(data)
                st.rerun()
    
    # Show overdue
    if overdue:
        st.markdown("---")
        st.markdown("**⚠️ Overdue Tasks** (use Quick Reschedule above)")
        for t in filter_tasks(overdue)[:10]:
            dk = t.get("department", "quick")
            color = dept_colors.get(dk, "#6B7280")
            st.markdown(f'<span style="background:{color}; color:white; padding:4px 8px; border-radius:4px; font-size:0.8rem; margin-right:8px;">{t["title"]}</span>', unsafe_allow_html=True)

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
                due_text = "OVERDUE"
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
        all_today = filter_tasks(overdue + today_tasks)
        all_today = sorted(all_today, key=lambda x: (x.get("order", 999), x.get("priority") != "high"))
        
        if all_today:
            st.markdown('<div class="section-head">Today</div>', unsafe_allow_html=True)
            for task in all_today:
                render_task(task)
        else:
            st.info("Nothing due today")
    
    elif view == "All":
        filtered = filter_tasks(open_tasks)
        sorted_tasks = sorted(filtered, key=lambda x: (x.get("due_date") or "9999", x.get("priority") != "high"))
        
        if sorted_tasks:
            st.markdown('<div class="section-head">All Tasks</div>', unsafe_allow_html=True)
            for task in sorted_tasks:
                render_task(task)
    
    elif view == "Done":
        filtered = filter_tasks(done_tasks)
        if filtered:
            st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
            for task in filtered[:30]:
                st.markdown(f"~~{task['title']}~~")
        else:
            st.info("No completed tasks")
