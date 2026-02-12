"""
GTF Command Center v11
Drag and drop reordering
"""

import streamlit as st
import json
from datetime import datetime, date
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
if "editing_task" not in st.session_state:
    st.session_state.editing_task = None

# Styling
st.markdown("""
<style>
    :root {
        --cream: #FAFAF8;
        --white: #FFFFFF;
        --charcoal: #1a1a1a;
        --gray: #6b6b6b;
        --light-gray: #e5e5e5;
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
        margin-right: 8px;
    }
    
    /* Sortable items styling */
    .sortable-item {
        background: var(--white);
        border: 1px solid var(--light-gray);
        padding: 12px 16px;
        margin: 4px 0;
        border-radius: 4px;
        cursor: grab;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .sortable-item:hover {
        border-color: #c9a87c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .sortable-item:active {
        cursor: grabbing;
    }
    
    .task-priority {
        width: 4px;
        height: 32px;
        border-radius: 2px;
        flex-shrink: 0;
    }
    
    .priority-high { background: #c45c5c; }
    .priority-medium { background: #c9a87c; }
    .priority-low { background: #d1d5db; }
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

# View selector
view = st.radio("View", ["Today", "All", "Done"], horizontal=True, label_visibility="collapsed")

def filter_tasks(task_list):
    if st.session_state.selected_dept:
        return [t for t in task_list if t.get("department") == st.session_state.selected_dept]
    return task_list

def get_task_display(task):
    """Create display string for sortable item"""
    dk = task.get("department", "quick")
    dept = dept_labels.get(dk, "Quick")
    due = task.get("due_date", "")
    priority = task.get("priority", "medium")
    
    due_str = ""
    if due:
        if due < today_str:
            due_str = "OVERDUE"
        elif due == today_str:
            due_str = "Today"
        else:
            due_str = due
    
    return f"{task['title']} | {dept} | {due_str} | {priority}"

def save_new_order(sorted_items, task_list):
    """Save the new order after drag and drop"""
    # Create mapping from display string to task id
    display_to_id = {get_task_display(t): t["id"] for t in task_list}
    
    # Update order values
    for new_order, item in enumerate(sorted_items):
        task_id = display_to_id.get(item)
        if task_id:
            for t in data["tasks"]:
                if t["id"] == task_id:
                    t["order"] = new_order
    
    save_tasks(data)

# Filter indicator
if st.session_state.selected_dept:
    dept_name = dept_labels.get(st.session_state.selected_dept, "")
    st.info(f"Filtered: {dept_name}")

# Views
if view == "Today":
    st.markdown('<div class="section-head">Today\'s Tasks - Drag to Reorder</div>', unsafe_allow_html=True)
    
    all_today = filter_tasks(overdue + today_tasks)
    all_today_sorted = sorted(all_today, key=lambda x: x.get("order", 999))
    
    if all_today_sorted:
        # Create sortable items
        items = [get_task_display(t) for t in all_today_sorted]
        
        sorted_items = sort_items(items, direction="vertical")
        
        # Check if order changed
        if sorted_items != items:
            save_new_order(sorted_items, all_today_sorted)
            st.rerun()
        
        # Show task details below
        st.markdown("---")
        st.markdown("**Task Details** (click to edit)")
        
        for item in sorted_items:
            # Find the task
            task = None
            for t in all_today_sorted:
                if get_task_display(t) == item:
                    task = t
                    break
            
            if task:
                dk = task.get("department", "quick")
                color = dept_colors.get(dk, "#9CA3AF")
                
                col1, col2, col3 = st.columns([0.05, 0.75, 0.2])
                
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
                    st.markdown(f"**{task['title']}**")
                    if task.get("notes"):
                        st.caption(task["notes"])
                
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
                
                st.divider()
    else:
        st.info("Nothing due today")

elif view == "All":
    st.markdown('<div class="section-head">All Tasks - Drag to Reorder</div>', unsafe_allow_html=True)
    
    filtered = filter_tasks(open_tasks)
    filtered_sorted = sorted(filtered, key=lambda x: x.get("order", 999))
    
    if filtered_sorted:
        items = [get_task_display(t) for t in filtered_sorted]
        sorted_items = sort_items(items, direction="vertical")
        
        if sorted_items != items:
            save_new_order(sorted_items, filtered_sorted)
            st.rerun()
        
        st.markdown("---")
        for item in sorted_items:
            task = next((t for t in filtered_sorted if get_task_display(t) == item), None)
            if task:
                col1, col2, col3 = st.columns([0.05, 0.75, 0.2])
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
                    st.markdown(f"**{task['title']}**")
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
                st.divider()

elif view == "Done":
    filtered = filter_tasks(done_tasks)
    if filtered:
        st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
        for t in filtered[:30]:
            st.markdown(f"~~{t['title']}~~")
            st.divider()
    else:
        st.info("No completed tasks")
