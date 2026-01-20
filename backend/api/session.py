"""
Session Management

In-memory storage for active game sessions.
"""

from typing import Dict, Optional
from backend.engine.model import GameSession


# In-memory session store
_sessions: Dict[str, GameSession] = {}


def get_session(session_id: str) -> Optional[GameSession]:
    """
    Retrieve a session by ID.
    
    Args:
        session_id: The session identifier
        
    Returns:
        The GameSession if found, None otherwise
    """
    return _sessions.get(session_id)


def store_session(session: GameSession) -> None:
    """
    Store a session.
    
    Args:
        session: The GameSession to store
    """
    _sessions[session.session_id] = session


def remove_session(session_id: str) -> bool:
    """
    Remove a session.
    
    Args:
        session_id: The session identifier
        
    Returns:
        True if session was removed, False if not found
    """
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


def get_all_sessions() -> Dict[str, GameSession]:
    """Get all active sessions (for debugging)."""
    return _sessions.copy()


def clear_all_sessions() -> None:
    """Clear all sessions (for testing)."""
    _sessions.clear()
