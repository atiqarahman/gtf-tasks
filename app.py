"""
GTF Command Center v19
With GitHub-backed persistence
"""

import streamlit as st
import json
import requests
import base64
from datetime import datetime, date, timedelta
from pathlib import Path
from streamlit_sortables import sort_items

# Cricket live scores - placeholder for now
def get_live_cricket():
    # Hardcoded sample data - replace with live API later
    return [
        {
            "match": "IND vs NAM",
            "score1": "IND: 209/9 (20 ov)",
            "score2": "NAM: 142/10 (18.3 ov)",
            "status": "India won by 67 runs"
        }
    ]

st.set_page_config(
    page_title="GTF Command Center",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).parent / "tasks.json"

# GitHub backend config
GITHUB_REPO = "atiqarahman/gtf-tasks"
GITHUB_FILE = "tasks.json"

def get_github_token():
    """Get GitHub token from Streamlit secrets"""
    try:
        return st.secrets["GITHUB_TOKEN"]
    except:
        return None

def load_from_github():
    """Load tasks.json from GitHub"""
    token = get_github_token()
    if not token:
        return None, None
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return json.loads(content), data["sha"]
    except:
        pass
    return None, None

def save_to_github(data, message="Dashboard update"):
    """Save tasks.json to GitHub"""
    token = get_github_token()
    if not token:
        return False
    
    sha = st.session_state.get("github_sha")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    content = json.dumps(data, indent=2, default=str)
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    payload = {"message": message, "content": encoded, "branch": "main"}
    if sha:
        payload["sha"] = sha
    
    try:
        resp = requests.put(url, headers=headers, json=payload, timeout=10)
        if resp.status_code in [200, 201]:
            # Update SHA for next save
            st.session_state["github_sha"] = resp.json().get("content", {}).get("sha")
            return True
    except:
        pass
    return False

def load_tasks():
    """Load tasks - GitHub first, then local file"""
    # Try GitHub first (for cloud deployment)
    github_data, sha = load_from_github()
    if github_data:
        st.session_state["github_sha"] = sha
        st.session_state["using_github"] = True
        return github_data
    
    # Fall back to local file
    st.session_state["using_github"] = False
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"departments": [], "department_labels": {}, "tasks": []}

def save_tasks(data):
    """Save tasks - GitHub if available, otherwise local"""
    if st.session_state.get("using_github"):
        if save_to_github(data):
            return True
    # Always save locally as backup
    DATA_FILE.write_text(json.dumps(data, indent=2, default=str))
    return True

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
    
    /* Clean popover trigger buttons */
    [data-testid="stPopover"] > button,
    button[kind="secondary"] {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 6px !important;
        font-size: 0.8rem !important;
        color: #333 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
        transition: all 0.15s ease !important;
    }
    
    [data-testid="stPopover"] > button:hover,
    button[kind="secondary"]:hover {
        border-color: #3B82F6 !important;
        box-shadow: 0 2px 8px rgba(59,130,246,0.15) !important;
        background: #f8fafc !important;
    }
    
    /* Popover content styling */
    [data-testid="stPopoverBody"] {
        padding: 12px !important;
    }
    
    [data-testid="stPopoverBody"] button {
        margin-top: 4px !important;
    }
    
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
    
    # Zoya suggestions section
    st.markdown("---")
    # Keep suggestions visible until: approved & completed, OR denied, OR explicitly completed in chat
    zoya_suggestions = [t for t in open_tasks if t.get("zoya_can_help") and t.get("zoya_status") not in ["completed", "denied"]]
    zoya_in_progress = [t for t in open_tasks if t.get("zoya_status") == "approved"]
    
    if zoya_in_progress:
        st.markdown(f"**🚀 Zoya Working On** ({len(zoya_in_progress)})")
        for zt in zoya_in_progress[:3]:
            st.caption(f"⏳ {zt['title'][:30]}...")
    
    if zoya_suggestions:
        st.markdown(f"**✨ Zoya Can Help** ({len(zoya_suggestions)})")
        for zt in zoya_suggestions[:5]:
            with st.expander(f"📌 {zt['title'][:22]}...", expanded=False):
                st.markdown(f"**{zt['title']}**")
                st.caption(zt.get("zoya_suggestion", "I can help with this task"))
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve", key=f"zoya_approve_{zt['id']}", use_container_width=True):
                        for t in data["tasks"]:
                            if t["id"] == zt["id"]:
                                t["zoya_status"] = "approved"
                                t["zoya_approved_at"] = datetime.now().isoformat()
                        save_tasks(data)
                        st.rerun()
                
                with col2:
                    if st.button("❌ Deny", key=f"zoya_deny_{zt['id']}", use_container_width=True):
                        for t in data["tasks"]:
                            if t["id"] == zt["id"]:
                                t["zoya_can_help"] = False
                                t["zoya_status"] = "denied"
                        save_tasks(data)
                        st.rerun()
                
                # Remind with date picker
                st.markdown("**⏰ Remind me to discuss:**")
                remind_cols = st.columns(3)
                with remind_cols[0]:
                    if st.button("Today (+2h)", key=f"remind_today_{zt['id']}", use_container_width=True):
                        # Remind in 2 hours
                        remind_time = datetime.now() + timedelta(hours=2)
                        new_task = {
                            "id": datetime.now().strftime("%Y%m%d%H%M%S") + zt["id"][:4],
                            "title": f"💬 Chat with Zoya about: {zt['title'][:30]}",
                            "department": zt.get("department", "quick"),
                            "priority": "high",
                            "due_date": today_str,
                            "notes": f"Discuss Zoya's suggestion: {zt.get('zoya_suggestion', '')}",
                            "done": False,
                            "created": datetime.now().isoformat(),
                            "is_zoya_reminder": True,
                            "original_task_id": zt["id"],
                            "remind_at": remind_time.isoformat(),
                            "remind_sent": False
                        }
                        data["tasks"].append(new_task)
                        # Don't change zoya_status - keep it in suggestions
                        for t in data["tasks"]:
                            if t["id"] == zt["id"]:
                                t["reminder_scheduled"] = remind_time.isoformat()
                        save_tasks(data)
                        st.toast(f"⏰ I'll remind you at {remind_time.strftime('%H:%M')}")
                        st.rerun()
                
                with remind_cols[1]:
                    if st.button("Tomorrow 🌅", key=f"remind_tmrw_{zt['id']}", use_container_width=True):
                        # Remind tomorrow at 9am
                        tomorrow_9am = datetime.combine(today + timedelta(days=1), datetime.strptime("09:00", "%H:%M").time())
                        new_task = {
                            "id": datetime.now().strftime("%Y%m%d%H%M%S") + zt["id"][:4],
                            "title": f"💬 Chat with Zoya about: {zt['title'][:30]}",
                            "department": zt.get("department", "quick"),
                            "priority": "high",
                            "due_date": (today + timedelta(days=1)).isoformat(),
                            "notes": f"Discuss Zoya's suggestion: {zt.get('zoya_suggestion', '')}",
                            "done": False,
                            "created": datetime.now().isoformat(),
                            "is_zoya_reminder": True,
                            "original_task_id": zt["id"],
                            "remind_at": tomorrow_9am.isoformat(),
                            "remind_sent": False
                        }
                        data["tasks"].append(new_task)
                        for t in data["tasks"]:
                            if t["id"] == zt["id"]:
                                t["reminder_scheduled"] = tomorrow_9am.isoformat()
                        save_tasks(data)
                        st.toast("⏰ I'll remind you tomorrow morning at 9am")
                        st.rerun()
                
                with remind_cols[2]:
                    remind_date = st.date_input("Pick", value=today, key=f"remind_date_{zt['id']}", label_visibility="collapsed")
                    if st.button("Set", key=f"remind_set_{zt['id']}", use_container_width=True):
                        # Remind at 9am on selected date
                        remind_9am = datetime.combine(remind_date, datetime.strptime("09:00", "%H:%M").time())
                        new_task = {
                            "id": datetime.now().strftime("%Y%m%d%H%M%S") + zt["id"][:4],
                            "title": f"💬 Chat with Zoya about: {zt['title'][:30]}",
                            "department": zt.get("department", "quick"),
                            "priority": "high",
                            "due_date": remind_date.isoformat(),
                            "notes": f"Discuss Zoya's suggestion: {zt.get('zoya_suggestion', '')}",
                            "done": False,
                            "created": datetime.now().isoformat(),
                            "is_zoya_reminder": True,
                            "original_task_id": zt["id"],
                            "remind_at": remind_9am.isoformat(),
                            "remind_sent": False
                        }
                        data["tasks"].append(new_task)
                        for t in data["tasks"]:
                            if t["id"] == zt["id"]:
                                t["reminder_scheduled"] = remind_9am.isoformat()
                        save_tasks(data)
                        st.toast(f"⏰ I'll remind you on {remind_date.strftime('%b %d')} at 9am")
                        st.rerun()
                
                # Chat now button
                if st.button("💬 Let's Chat Now", key=f"zoya_chat_{zt['id']}", use_container_width=True):
                    for t in data["tasks"]:
                        if t["id"] == zt["id"]:
                            t["zoya_status"] = "chat_now"
                            t["zoya_chat_requested_at"] = datetime.now().isoformat()
                    save_tasks(data)
                    st.rerun()
    
    elif not zoya_in_progress:
        st.markdown("**✨ Zoya Can Help**")
        st.caption("No suggestions yet")
    
    st.markdown("---")
    
    # Quick actions - Google Meet
    st.markdown("**Quick Meeting**")
    st.link_button("📹 Start Meet Now", "https://meet.google.com/new", use_container_width=True)
    st.link_button("🔗 Schedule + Get Link", "https://calendar.google.com/calendar/render?action=TEMPLATE&text=GTF+Meeting&details=Created+from+GTF+Command+Center", use_container_width=True)
    
    st.markdown("---")
    
    # Live Cricket Scores
    st.markdown("**🏏 Live Cricket**")
    live_matches = get_live_cricket()
    if live_matches:
        for match in live_matches[:3]:
            st.markdown(f"**{match['match']}**")
            if match['score1']:
                st.caption(match['score1'])
            if match['score2']:
                st.caption(match['score2'])
            st.caption(f"_{match['status']}_")
            st.markdown("")
    else:
        st.caption("No live matches right now")
    
    st.link_button("📺 All Scores", "https://www.espncricinfo.com/live-cricket-score", use_container_width=True)
    
    # Placeholder for sports book
    st.button("📚 Atiqa's Sports Book", use_container_width=True, disabled=True)
    st.caption("Coming soon...")
    
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
    # Calendar view with clickable colored task cards
    days = [(today + timedelta(days=i-1)) for i in range(7)]
    
    # Initialize selected task state
    if "selected_task" not in st.session_state:
        st.session_state.selected_task = None
    
    # If a task is selected, show action bar at top
    if st.session_state.selected_task:
        sel_task = next((t for t in tasks if t["id"] == st.session_state.selected_task), None)
        if sel_task:
            st.markdown(f"**Selected:** {sel_task['title'][:50]}")
            ac1, ac2, ac3, ac4, ac5 = st.columns([1, 1, 1, 2, 1])
            
            with ac1:
                if st.button("✅ Done", use_container_width=True, key="action_done"):
                    for t in data["tasks"]:
                        if t["id"] == st.session_state.selected_task:
                            t["done"] = True
                            t["completed_date"] = today_str
                    save_tasks(data)
                    st.session_state.selected_task = None
                    st.rerun()
            
            with ac2:
                if st.button("→ Tomorrow", use_container_width=True, key="action_tomorrow"):
                    for t in data["tasks"]:
                        if t["id"] == st.session_state.selected_task:
                            t["due_date"] = (today + timedelta(days=1)).isoformat()
                    save_tasks(data)
                    st.session_state.selected_task = None
                    st.rerun()
            
            with ac3:
                if st.button("→ Today", use_container_width=True, key="action_today"):
                    for t in data["tasks"]:
                        if t["id"] == st.session_state.selected_task:
                            t["due_date"] = today_str
                    save_tasks(data)
                    st.session_state.selected_task = None
                    st.rerun()
            
            with ac4:
                move_to = st.date_input("Move to date", value=today, label_visibility="collapsed", key="action_date")
                
            with ac5:
                if st.button("Move", use_container_width=True, key="action_move"):
                    for t in data["tasks"]:
                        if t["id"] == st.session_state.selected_task:
                            t["due_date"] = move_to.isoformat()
                    save_tasks(data)
                    st.session_state.selected_task = None
                    st.rerun()
            
            if st.button("✕ Cancel", key="action_cancel"):
                st.session_state.selected_task = None
                st.rerun()
            
            st.markdown("---")
    
    # Render day columns with clickable task cards
    cols = st.columns(7)
    
    for i, d in enumerate(days):
        d_str = d.isoformat()
        day_tasks = [t for t in filter_tasks(open_tasks) if t.get("due_date") == d_str]
        day_tasks = sorted(day_tasks, key=lambda x: (x.get("order", 999), x.get("priority") != "high"))
        
        day_name = d.strftime("%a")
        if d == today:
            day_name = "📍 TODAY"
        elif d == today - timedelta(days=1):
            day_name = "Yesterday"
        elif d == today + timedelta(days=1):
            day_name = "Tomorrow"
        else:
            day_name = f"{d.strftime('%a')}"
        
        with cols[i]:
            title_class = "day-title today" if d == today else "day-title"
            st.markdown(f'<div class="{title_class}">{day_name}<br><span style="font-size:1.3rem; font-weight:700;">{d.day}</span></div>', unsafe_allow_html=True)
            
            if day_tasks:
                for t in day_tasks:
                    dk = t.get("department", "quick")
                    color = dept_colors.get(dk, "#6B7280")
                    label = t["title"][:18] + "..." if len(t["title"]) > 18 else t["title"]
                    is_selected = st.session_state.selected_task == t["id"]
                    
                    # Use popover for each task
                    with st.popover(f"{'✓ ' if is_selected else ''}{label}", use_container_width=True):
                        st.markdown(f"**{t['title']}**")
                        st.caption(f"Dept: {dept_labels.get(dk, 'Quick')} · Due: {t.get('due_date', 'Not set')}")
                        
                        # Notes section
                        current_notes = t.get("notes", "")
                        if current_notes:
                            st.markdown(f"📝 *{current_notes}*")
                        
                        new_notes = st.text_area("Notes", value=current_notes, key=f"notes_{t['id']}", height=80, placeholder="Add context, details, links...")
                        if new_notes != current_notes:
                            if st.button("💾 Save Notes", key=f"save_notes_{t['id']}", use_container_width=True):
                                for task in data["tasks"]:
                                    if task["id"] == t["id"]:
                                        task["notes"] = new_notes
                                save_tasks(data)
                                st.rerun()
                        
                        st.markdown("---")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("✅ Done", key=f"pop_done_{t['id']}", use_container_width=True):
                                for task in data["tasks"]:
                                    if task["id"] == t["id"]:
                                        task["done"] = True
                                        task["completed_date"] = today_str
                                save_tasks(data)
                                st.rerun()
                        
                        with col_b:
                            if st.button("→ Tomorrow", key=f"pop_tmrw_{t['id']}", use_container_width=True):
                                for task in data["tasks"]:
                                    if task["id"] == t["id"]:
                                        task["due_date"] = (today + timedelta(days=1)).isoformat()
                                save_tasks(data)
                                st.rerun()
                        
                        new_date = st.date_input("Move to", value=d, key=f"pop_date_{t['id']}", label_visibility="collapsed")
                        if st.button("Move to date", key=f"pop_move_{t['id']}", use_container_width=True):
                            for task in data["tasks"]:
                                if task["id"] == t["id"]:
                                    task["due_date"] = new_date.isoformat()
                            save_tasks(data)
                            st.rerun()
            else:
                st.caption("—")
    
    # Color legend
    st.markdown("---")
    legend_html = "<div style='display:flex; flex-wrap:wrap; gap:8px; align-items:center;'><span style='font-size:0.75rem; color:#888;'>Departments:</span>"
    for dk, dn in dept_labels.items():
        color = dept_colors.get(dk, "#6B7280")
        count = len([t for t in open_tasks if t.get("department") == dk])
        if count > 0:
            legend_html += f"<span style='background:{color}; color:white; padding:3px 8px; border-radius:4px; font-size:0.7rem;'>{dn}</span>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)
    
    # Overdue section
    overdue_filtered = filter_tasks(overdue)
    if overdue_filtered:
        st.markdown("---")
        st.markdown("**⚠️ Overdue Tasks**")
        ov_cols = st.columns(4)
        for idx, t in enumerate(overdue_filtered[:12]):
            dk = t.get("department", "quick")
            color = dept_colors.get(dk, "#6B7280")
            label = t["title"][:22] + "..." if len(t["title"]) > 22 else t["title"]
            
            with ov_cols[idx % 4]:
                with st.popover(label, use_container_width=True):
                    st.markdown(f"**{t['title']}**")
                    st.caption(f"Dept: {dept_labels.get(dk, 'Quick')} · Overdue: {t.get('due_date', '')}")
                    
                    # Notes section
                    current_notes = t.get("notes", "")
                    if current_notes:
                        st.markdown(f"📝 *{current_notes}*")
                    
                    new_notes = st.text_area("Notes", value=current_notes, key=f"ov_notes_{t['id']}", height=60, placeholder="Add context...")
                    if new_notes != current_notes:
                        if st.button("💾 Save", key=f"ov_save_{t['id']}", use_container_width=True):
                            for task in data["tasks"]:
                                if task["id"] == t["id"]:
                                    task["notes"] = new_notes
                            save_tasks(data)
                            st.rerun()
                    
                    st.markdown("---")
                    
                    if st.button("✅ Done", key=f"ov_done_{t['id']}", use_container_width=True):
                        for task in data["tasks"]:
                            if task["id"] == t["id"]:
                                task["done"] = True
                                task["completed_date"] = today_str
                        save_tasks(data)
                        st.rerun()
                    
                    if st.button("→ Today", key=f"ov_today_{t['id']}", use_container_width=True):
                        for task in data["tasks"]:
                            if task["id"] == t["id"]:
                                task["due_date"] = today_str
                        save_tasks(data)
                        st.rerun()
                    
                    if st.button("→ Tomorrow", key=f"ov_tmrw_{t['id']}", use_container_width=True):
                        for task in data["tasks"]:
                            if task["id"] == t["id"]:
                                task["due_date"] = (today + timedelta(days=1)).isoformat()
                        save_tasks(data)
                        st.rerun()

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
