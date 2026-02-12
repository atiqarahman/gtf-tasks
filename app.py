"""
GTF Command Center v15
Calendar view with expand/collapse
"""

import streamlit as st
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from calendar import monthcalendar, month_name

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
today_str = date.today().isoformat()
today = date.today()

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

if "selected_dept" not in st.session_state:
    st.session_state.selected_dept = None
if "show_calendar" not in st.session_state:
    st.session_state.show_calendar = False

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
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: var(--white) !important;
    }
    
    #MainMenu, footer, header, .stDeployButton { display: none !important; }
    
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
    
    .stat-num { font-size: 2rem; font-weight: 600; color: var(--charcoal); }
    .stat-num.red { color: var(--red); }
    .stat-label { font-size: 0.7rem; color: var(--gray); text-transform: uppercase; letter-spacing: 1px; margin-top: 0.4rem; }
    
    .section-head {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--light-gray);
    }
    
    .task-card {
        background: var(--white);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #ccc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .task-title { font-size: 0.95rem; font-weight: 500; color: var(--charcoal); margin-bottom: 0.4rem; }
    .task-meta { font-size: 0.75rem; color: var(--gray); display: flex; gap: 1rem; align-items: center; }
    .task-dept { font-weight: 600; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }
    .task-due.overdue { color: var(--red); font-weight: 600; }
    
    /* Calendar styles */
    .calendar-container {
        background: var(--white);
        border: 1px solid var(--light-gray);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .calendar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .calendar-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--charcoal);
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 2px;
    }
    
    .calendar-day-header {
        text-align: center;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--gray);
        text-transform: uppercase;
        padding: 0.5rem;
    }
    
    .calendar-day {
        min-height: 100px;
        background: var(--cream);
        border: 1px solid var(--light-gray);
        padding: 0.5rem;
        vertical-align: top;
    }
    
    .calendar-day.today {
        background: #FEF3C7;
    }
    
    .calendar-day.other-month {
        background: #f5f5f5;
        opacity: 0.5;
    }
    
    .calendar-date {
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--charcoal);
        margin-bottom: 0.5rem;
    }
    
    .calendar-date.today {
        background: var(--red);
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .calendar-task {
        font-size: 0.7rem;
        padding: 3px 6px;
        border-radius: 4px;
        margin-bottom: 3px;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        cursor: pointer;
    }
    
    .calendar-task:hover {
        opacity: 0.8;
    }
    
    .calendar-more {
        font-size: 0.65rem;
        color: var(--gray);
        cursor: pointer;
    }
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
    
    if st.button("All", use_container_width=True):
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

# Main
st.title("Command Center")
st.caption(datetime.now().strftime("%A, %B %d, %Y"))

# Stats row
st.markdown(f"""
<div class="stats-grid">
    <div class="stat-box"><div class="stat-num">{len(open_tasks)}</div><div class="stat-label">Open</div></div>
    <div class="stat-box"><div class="stat-num">{len(today_tasks)}</div><div class="stat-label">Today</div></div>
    <div class="stat-box"><div class="stat-num {'red' if overdue else ''}">{len(overdue)}</div><div class="stat-label">Overdue</div></div>
    <div class="stat-box"><div class="stat-num">{len(high_p)}</div><div class="stat-label">Priority</div></div>
</div>
""", unsafe_allow_html=True)

# Calendar toggle button
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("📅 Expand Calendar View" if not st.session_state.show_calendar else "📅 Collapse Calendar", use_container_width=True):
        st.session_state.show_calendar = not st.session_state.show_calendar
        st.rerun()

# Calendar View
if st.session_state.show_calendar:
    st.markdown("---")
    
    # Get tasks organized by date
    tasks_by_date = {}
    for t in open_tasks:
        due = t.get("due_date")
        if due:
            if due not in tasks_by_date:
                tasks_by_date[due] = []
            tasks_by_date[due].append(t)
    
    # Calendar navigation
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = today.month
    if "cal_year" not in st.session_state:
        st.session_state.cal_year = today.year
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("< Prev"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1
            st.rerun()
    with col2:
        st.markdown(f"### {month_name[st.session_state.cal_month]} {st.session_state.cal_year}")
    with col3:
        if st.button("Next >"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1
            st.rerun()
    
    # Build calendar HTML
    cal = monthcalendar(st.session_state.cal_year, st.session_state.cal_month)
    
    calendar_html = '<div class="calendar-container"><div class="calendar-grid">'
    
    # Day headers
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        calendar_html += f'<div class="calendar-day-header">{day}</div>'
    
    # Days
    for week in cal:
        for day in week:
            if day == 0:
                calendar_html += '<div class="calendar-day other-month"></div>'
            else:
                day_date = date(st.session_state.cal_year, st.session_state.cal_month, day)
                day_str = day_date.isoformat()
                is_today = day_date == today
                
                day_class = "calendar-day"
                if is_today:
                    day_class += " today"
                
                date_class = "calendar-date"
                if is_today:
                    date_class += " today"
                
                calendar_html += f'<div class="{day_class}">'
                calendar_html += f'<div class="{date_class}">{day}</div>'
                
                # Tasks for this day
                day_tasks = tasks_by_date.get(day_str, [])
                shown = 0
                for t in day_tasks[:3]:
                    dk = t.get("department", "quick")
                    color = dept_colors.get(dk, "#6B7280")
                    calendar_html += f'<div class="calendar-task" style="background: {color};" title="{t["title"]}">{t["title"]}</div>'
                    shown += 1
                
                if len(day_tasks) > 3:
                    calendar_html += f'<div class="calendar-more">+{len(day_tasks) - 3} more</div>'
                
                calendar_html += '</div>'
    
    calendar_html += '</div></div>'
    
    st.markdown(calendar_html, unsafe_allow_html=True)
    
    # Quick task moving
    st.markdown("**Quick Move Task**")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        task_options = {f"{t['title']}": t['id'] for t in open_tasks}
        selected_task = st.selectbox("Select task", options=list(task_options.keys()), label_visibility="collapsed")
    with col2:
        new_date = st.date_input("New date", value=today, label_visibility="collapsed")
    with col3:
        if st.button("Move"):
            task_id = task_options.get(selected_task)
            if task_id:
                for t in data["tasks"]:
                    if t["id"] == task_id:
                        t["due_date"] = new_date.isoformat()
                save_tasks(data)
                st.success(f"Moved!")
                st.rerun()
    
    st.markdown("---")

# Regular view tabs
view = st.radio("View", ["Today", "All", "Done"], horizontal=True, label_visibility="collapsed")

if st.session_state.selected_dept:
    dept_name = dept_labels.get(st.session_state.selected_dept, "")
    st.info(f"Filtered: {dept_name}")

def render_task_card(task):
    dk = task.get("department", "quick")
    dept = dept_labels.get(dk, "Quick")
    color = dept_colors.get(dk, "#6B7280")
    due = task.get("due_date")
    priority = task.get("priority", "medium")
    
    due_class = ""
    due_text = ""
    if due:
        if due < today_str:
            due_text = "OVERDUE"
            due_class = "overdue"
        elif due == today_str:
            due_text = "Today"
        else:
            due_text = due
    
    pri_color = {"high": "#EF4444", "medium": "#F59E0B", "low": "#6B7280"}.get(priority, "#6B7280")
    
    return f"""
    <div class="task-card" style="border-left-color: {color};">
        <div class="task-title">{task['title']}</div>
        <div class="task-meta">
            <span class="task-dept" style="background: {color}22; color: {color};">{dept}</span>
            <span class="task-due {due_class}">{due_text}</span>
            <span style="color: {pri_color}; text-transform: uppercase; font-size: 0.65rem;">{priority}</span>
        </div>
    </div>
    """

# Views
if view == "Today":
    all_today = filter_tasks(overdue + today_tasks)
    all_today_sorted = sorted(all_today, key=lambda x: (x.get("order", 999), x.get("priority") != "high"))
    
    if all_today_sorted:
        st.markdown('<div class="section-head">Today\'s Tasks</div>', unsafe_allow_html=True)
        
        for task in all_today_sorted:
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
                st.markdown(render_task_card(task), unsafe_allow_html=True)
                if task.get("notes"):
                    st.caption(f"Notes: {task['notes']}")
            
            with col3:
                with st.popover("Edit"):
                    new_due = st.date_input("Due", 
                        value=date.fromisoformat(task["due_date"]) if task.get("due_date") else None, 
                        key=f"due_{task['id']}")
                    new_priority = st.selectbox("Priority", ["high", "medium", "low"], 
                        index=["high", "medium", "low"].index(task.get("priority", "medium")),
                        key=f"pri_{task['id']}")
                    new_notes = st.text_area("Notes", value=task.get("notes", ""), 
                        key=f"notes_{task['id']}", height=80)
                    
                    if st.button("Save", key=f"save_{task['id']}"):
                        for t in data["tasks"]:
                            if t["id"] == task["id"]:
                                t["due_date"] = new_due.isoformat() if new_due else None
                                t["priority"] = new_priority
                                t["notes"] = new_notes
                        save_tasks(data)
                        st.rerun()
    else:
        st.info("Nothing due today")

elif view == "All":
    filtered = filter_tasks(open_tasks)
    filtered_sorted = sorted(filtered, key=lambda x: (x.get("order", 999), x.get("due_date") or "9999"))
    
    if filtered_sorted:
        st.markdown('<div class="section-head">All Tasks</div>', unsafe_allow_html=True)
        
        for task in filtered_sorted:
            col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
            
            with col1:
                done = st.checkbox("", value=False, key=f"done_{task['id']}")
                if done:
                    for t in data["tasks"]:
                        if t["id"] == task["id"]:
                            t["done"] = True
                            t["completed_date"] = today_str
                    save_tasks(data)
                    st.rerun()
            
            with col2:
                st.markdown(render_task_card(task), unsafe_allow_html=True)
            
            with col3:
                with st.popover("Edit"):
                    new_due = st.date_input("Due", 
                        value=date.fromisoformat(task["due_date"]) if task.get("due_date") else None,
                        key=f"due_{task['id']}")
                    new_priority = st.selectbox("Priority", ["high", "medium", "low"],
                        index=["high", "medium", "low"].index(task.get("priority", "medium")),
                        key=f"pri_{task['id']}")
                    new_notes = st.text_area("Notes", value=task.get("notes", ""),
                        key=f"notes_{task['id']}", height=80)
                    if st.button("Save", key=f"save_{task['id']}"):
                        for t in data["tasks"]:
                            if t["id"] == task["id"]:
                                t["due_date"] = new_due.isoformat() if new_due else None
                                t["priority"] = new_priority
                                t["notes"] = new_notes
                        save_tasks(data)
                        st.rerun()

elif view == "Done":
    filtered = filter_tasks(done_tasks)
    
    if filtered:
        st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
        for task in filtered[:30]:
            st.markdown(f"~~{task['title']}~~")
    else:
        st.info("No completed tasks")
