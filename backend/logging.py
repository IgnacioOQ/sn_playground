"""
Data Logger

Handles saving session data to JSON files in the data/sessions folder.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from backend.engine.state import RoundResult


# Get the project root (parent of backend/)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "sessions"


def ensure_data_dir() -> Path:
    """Ensure the data/sessions directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def save_session_data(
    session_id: str,
    config: Dict[str, Any],
    history: List[RoundResult],
    agent_score: int,
    human_score: int,
    agent_name: str,
    agent_type: str
) -> str:
    """
    Save session data to a JSON file.
    
    Args:
        session_id: Unique session identifier
        config: Simulation configuration
        history: List of round results
        agent_score: Final agent score
        human_score: Final human score
        agent_name: Name of the agent
        agent_type: Type/strategy of the agent
        
    Returns:
        Path to the saved file
    """
    ensure_data_dir()
    
    # Build the session data structure
    session_data = {
        "session_id": session_id,
        "timestamp": datetime.now().astimezone().isoformat(),
        "metadata": {
            "agent_name": agent_name,
            "agent_type": agent_type,
            "num_rounds": config.get("num_rounds", len(history)),
        },
        "config": config,
        "final_scores": {
            "human": human_score,
            "agent": agent_score
        },
        "winner": "human" if human_score > agent_score else ("agent" if agent_score > human_score else "tie"),
        "steps": []
    }
    
    # Convert history to the requested format:
    # (step, human_action, agent_action, outcome_human, outcome_agent, step+1, done)
    num_rounds = len(history)
    for i, round_result in enumerate(history):
        step_data = {
            "step": i,
            "human_action": round_result.human_action,
            "agent_action": round_result.agent_action,
            "outcome_human": round_result.human_payoff,
            "outcome_agent": round_result.agent_payoff,
            "next_step": i + 1,
            "done": (i == num_rounds - 1)
        }
        session_data["steps"].append(step_data)
    
    # Save to file
    filepath = DATA_DIR / f"{session_id}.json"
    with open(filepath, "w") as f:
        json.dump(session_data, f, indent=2)
    
    return str(filepath)


def load_session_data(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Load session data from a JSON file.
    
    Args:
        session_id: The session identifier
        
    Returns:
        Session data dict if found, None otherwise
    """
    filepath = DATA_DIR / f"{session_id}.json"
    if not filepath.exists():
        return None
    
    with open(filepath, "r") as f:
        return json.load(f)


def list_all_sessions() -> List[str]:
    """List all saved session IDs."""
    ensure_data_dir()
    return [f.stem for f in DATA_DIR.glob("*.json")]
