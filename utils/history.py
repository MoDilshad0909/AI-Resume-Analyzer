"""
Resume History Module

This module handles saving and loading previous versions of resumes
and AI-generated content to maintain a version history for the user.
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any

HISTORY_DIR = "data/history"

def _ensure_dir():
    """Ensures the history directory exists."""
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)

def save_resume_version(session_id: str, data: Dict[str, Any]) -> str:
    """
    Saves a snapshot of the current resume and generated content.
    
    Args:
        session_id (str): A unique identifier for the user or session (e.g., email or name).
        data (Dict[str, Any]): The content to save.
        
    Returns:
        str: The path to the saved JSON file.
    """
    _ensure_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean the session ID for valid filenames
    clean_id = "".join(c for c in session_id if c.isalnum() or c in (' ', '_')).replace(" ", "_")
    if not clean_id:
        clean_id = "anonymous"
        
    filename = f"{clean_id}_v_{timestamp}.json"
    filepath = os.path.join(HISTORY_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    return filepath

def load_resume_history(session_id: str = None) -> List[Dict[str, Any]]:
    """
    Loads all saved versions. If session_id is provided, filters by it.
    
    Args:
        session_id (str, optional): The identifier to filter by.
        
    Returns:
        List[Dict[str, Any]]: A list of historical saved sessions, sorted by newest first.
    """
    _ensure_dir()
    history = []
    
    clean_id = None
    if session_id:
        clean_id = "".join(c for c in session_id if c.isalnum() or c in (' ', '_')).replace(" ", "_")
    
    for filename in os.listdir(HISTORY_DIR):
        if not filename.endswith(".json"):
            continue
            
        if clean_id and not filename.startswith(clean_id):
            continue
            
        filepath = os.path.join(HISTORY_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                data['filename'] = filename
                data['timestamp_str'] = filename.split('_v_')[-1].replace('.json', '')
                history.append(data)
            except json.JSONDecodeError:
                pass
                
    # Sort by timestamp descending
    history.sort(key=lambda x: x.get('filename', ''), reverse=True)
    return history
