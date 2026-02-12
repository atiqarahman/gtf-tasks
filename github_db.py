"""
GitHub-backed database for GTF Tasks
Uses GitHub API to read/write tasks.json directly to the repo
"""

import json
import base64
import requests
import streamlit as st
from datetime import datetime

# Config
REPO_OWNER = "atiqarahman"
REPO_NAME = "gtf-tasks"
FILE_PATH = "tasks.json"
BRANCH = "main"

def get_github_token():
    """Get GitHub token from Streamlit secrets"""
    try:
        return st.secrets["GITHUB_TOKEN"]
    except:
        return None

def get_file_from_github():
    """Fetch tasks.json from GitHub"""
    token = get_github_token()
    if not token:
        return None, None
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        resp = requests.get(url, headers=headers, params={"ref": BRANCH})
        if resp.status_code == 200:
            data = resp.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return json.loads(content), data["sha"]
        return None, None
    except Exception as e:
        st.error(f"GitHub read error: {e}")
        return None, None

def save_file_to_github(data, sha=None, message="Update tasks"):
    """Save tasks.json to GitHub"""
    token = get_github_token()
    if not token:
        return False
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    content = json.dumps(data, indent=2, default=str)
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": message,
        "content": encoded_content,
        "branch": BRANCH
    }
    
    if sha:
        payload["sha"] = sha
    
    try:
        resp = requests.put(url, headers=headers, json=payload)
        return resp.status_code in [200, 201]
    except Exception as e:
        st.error(f"GitHub save error: {e}")
        return False

def load_tasks_from_github():
    """Load tasks from GitHub, with caching"""
    data, sha = get_file_from_github()
    if data:
        # Store SHA in session for later updates
        st.session_state["github_sha"] = sha
        return data
    return None

def save_tasks_to_github(data, message="Dashboard update"):
    """Save tasks to GitHub"""
    sha = st.session_state.get("github_sha")
    success = save_file_to_github(data, sha, message)
    if success:
        # Refresh SHA after save
        _, new_sha = get_file_from_github()
        st.session_state["github_sha"] = new_sha
    return success
