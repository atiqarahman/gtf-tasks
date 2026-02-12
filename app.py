"""
GTF Command Center v9
System fonts, no rendering issues
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

def save_tasks(data):
    DATA_FILE.write_text(json.dumps(data, indent=2, default=str))

data = load_tasks()
tasks = data.get("tasks", [])
dept_labels = data.get("department_labels", {})
today_str = date.today().isoformat()

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
    "quick": "#9CA3AF"
}

if "selected_dept" not in st.session_state:
    st.session_state.selected_dept = None

# Simple styling - system fonts only
st.markdown("""
<style>
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
    
    .stat-num {
        font-size: 2rem;
        font-weight: 600;
        color: var(--charcoal);
    }
    
    .stat-num.red { color: var(--red); }
    
    .stat-label {
        font-size: 0.7rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.4rem;
    }
    
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
    
    .dept-tag {
        font-size: 0.65rem;
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 3px;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Stats
open_tasks = [t for t in tasks if not t.get("done")]
done_tasks = [t for t in tasks if t.get("done")]
today_tasks = [t for t in open_tasks if t.get("due_date") == today_str]
overdue = [t for t in open_tasks if t.get("due_date") and t.get("due_date") < today_str]
high_p = [t for t in open_tasks if t.get("priority") == "high"]

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

# Filters
col1, col2 = st.columns([2, 1])
with col1:
    view = st.radio("View", ["Today", "All", "Done"], horizontal=True, label_visibility="collapsed")
with col2:
    sort_by = st.selectbox("Sort", ["Due Date", "Priority", "Department"], label_visibility="collapsed")

def filter_tasks(task_list):
    if st.session_state.selected_dept:
        return [t for t in task_list if t.get("department") == st.session_state.selected_dept]
    return task_list

def sort_tasks(task_list):
    if sort_by == "Due Date":
        return sorted(task_list, key=lambda x: (x.get("due_date") or "9999"))
    elif sort_by == "Priority":
        p_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(task_list, key=lambda x: p_order.get(x.get("priority", "medium"), 1))
    else:
        return sorted(task_list, key=lambda x: x.get("department", "quick"))

def render_task(task):
    dk = task.get("department", "quick")
    dept = dept_labels.get(dk, "Quick")
    color = dept_colors.get(dk, "#9CA3AF")
    due = task.get("due_date")
    priority = task.get("priority", "medium")
    notes = task.get("notes", "")
    is_done = task.get("done", False)
    
    # Due date text
    due_text = ""
    if due:
        if due < today_str:
            due_text = f"OVERDUE ({due})"
        elif due == today_str:
            due_text = "Today"
        else:
            due_text = due
    
    col1, col2 = st.columns([0.05, 0.95])
    
    with col1:
        done = st.checkbox("Done", value=is_done, key=f"done_{task['id']}", label_visibility="collapsed")
        if done != is_done:
            for t in data["tasks"]:
                if t["id"] == task["id"]:
                    t["done"] = done
                    if done:
                        t["completed_date"] = today_str
            save_tasks(data)
            st.rerun()
    
    with col2:
        title_style = "~~" if is_done else ""
        st.markdown(f"**{title_style}{task['title']}{title_style}**")
        
        tag_html = f'<span class="dept-tag" style="background:{color}">{dept}</span>'
        st.markdown(f"{tag_html} | {due_text} | {priority.upper()}", unsafe_allow_html=True)
        
        if notes:
            st.caption(f"Notes: {notes}")
        
        # Edit section using columns instead of expander
        with st.popover("Edit"):
            new_due = st.date_input("Due", value=date.fromisoformat(due) if due else None, key=f"due_{task['id']}")
            new_priority = st.selectbox("Priority", ["high", "medium", "low"], 
                                        index=["high", "medium", "low"].index(priority),
                                        key=f"pri_{task['id']}")
            new_notes = st.text_area("Notes", value=notes, key=f"notes_{task['id']}", height=80)
            
            if st.button("Save", key=f"save_{task['id']}"):
                for t in data["tasks"]:
                    if t["id"] == task["id"]:
                        t["due_date"] = new_due.isoformat() if new_due else None
                        t["priority"] = new_priority
                        t["notes"] = new_notes
                save_tasks(data)
                st.success("Saved!")
                st.rerun()
    
    st.divider()

# Show filter
if st.session_state.selected_dept:
    dept_name = dept_labels.get(st.session_state.selected_dept, "")
    st.info(f"Filtered: {dept_name}")

# Views
if view == "Today":
    filtered_overdue = filter_tasks(overdue)
    filtered_today = filter_tasks(today_tasks)
    
    if filtered_overdue:
        st.markdown('<div class="section-head">Overdue</div>', unsafe_allow_html=True)
        for t in sort_tasks(filtered_overdue):
            render_task(t)
    
    if filtered_today:
        st.markdown('<div class="section-head">Due Today</div>', unsafe_allow_html=True)
        for t in sort_tasks(filtered_today):
            render_task(t)
    
    if not filtered_overdue and not filtered_today:
        st.info("Nothing due today")

elif view == "All":
    filtered = filter_tasks(open_tasks)
    st.markdown('<div class="section-head">All Tasks</div>', unsafe_allow_html=True)
    for t in sort_tasks(filtered):
        render_task(t)

elif view == "Done":
    filtered = filter_tasks(done_tasks)
    if filtered:
        st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
        for t in sort_tasks(filtered)[:30]:
            render_task(t)
    else:
        st.info("No completed tasks")
