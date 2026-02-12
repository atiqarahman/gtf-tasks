"""
GTF Command Center v12
Department colored tasks
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
    "quick": "#6B7280"
}

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
        --red: #c45c5c;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
        background-color: var(--cream) !important;
    }
    
    .main .block-container {
        background-color: var(--cream) !important;
        padding: 2rem 3rem !important;
        max-width: 1100px !important;
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
    
    .task-card {
        background: var(--white);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #ccc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .task-title {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--charcoal);
        margin-bottom: 0.4rem;
    }
    
    .task-meta {
        font-size: 0.75rem;
        color: var(--gray);
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .task-dept {
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
    }
    
    .task-due {
        color: var(--gray);
    }
    
    .task-due.overdue {
        color: #EF4444;
        font-weight: 600;
    }
    
    .task-priority {
        text-transform: uppercase;
        font-size: 0.65rem;
        letter-spacing: 0.5px;
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
            color = dept_colors.get(dk, "#6B7280")
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

def render_task(task):
    dk = task.get("department", "quick")
    dept = dept_labels.get(dk, "Quick")
    color = dept_colors.get(dk, "#6B7280")
    due = task.get("due_date")
    priority = task.get("priority", "medium")
    notes = task.get("notes", "")
    is_done = task.get("done", False)
    
    # Due text
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
    
    # Priority color
    pri_color = {"high": "#EF4444", "medium": "#F59E0B", "low": "#6B7280"}.get(priority, "#6B7280")
    
    col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
    
    with col1:
        done = st.checkbox("", value=is_done, key=f"done_{task['id']}", label_visibility="collapsed")
        if done != is_done:
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
            <div class="task-title">{'<s>' + task['title'] + '</s>' if is_done else task['title']}</div>
            <div class="task-meta">
                <span class="task-dept" style="background: {color}20; color: {color};">{dept}</span>
                <span class="task-due {due_class}">{due_text}</span>
                <span class="task-priority" style="color: {pri_color};">{priority}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if notes:
            st.caption(f"Notes: {notes}")
    
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

# Filter indicator
if st.session_state.selected_dept:
    dept_name = dept_labels.get(st.session_state.selected_dept, "")
    st.info(f"Filtered: {dept_name}")

# Sort tasks by order then priority
def sort_tasks(task_list):
    return sorted(task_list, key=lambda x: (x.get("order", 999), x.get("priority") != "high"))

# Views
if view == "Today":
    all_today = filter_tasks(overdue + today_tasks)
    
    if all_today:
        st.markdown('<div class="section-head">Today\'s Tasks</div>', unsafe_allow_html=True)
        
        for t in sort_tasks(all_today):
            render_task(t)
    else:
        st.info("Nothing due today")

elif view == "All":
    filtered = filter_tasks(open_tasks)
    
    if filtered:
        st.markdown('<div class="section-head">All Tasks</div>', unsafe_allow_html=True)
        
        for t in sort_tasks(filtered):
            render_task(t)

elif view == "Done":
    filtered = filter_tasks(done_tasks)
    
    if filtered:
        st.markdown('<div class="section-head">Completed</div>', unsafe_allow_html=True)
        
        for t in filtered[:30]:
            render_task(t)
    else:
        st.info("No completed tasks")
