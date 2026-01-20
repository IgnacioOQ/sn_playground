"""
Simulation State Models

Pydantic models for representing game state.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class ActionType(str, Enum):
    """Action types for API serialization."""
    COOPERATE = "cooperate"
    DEFECT = "defect"


class RoundResult(BaseModel):
    """Result of a single round."""
    round_number: int
    agent_action: ActionType
    human_action: ActionType
    agent_payoff: int
    human_payoff: int


class GameState(BaseModel):
    """
    Complete game state for frontend rendering.
    
    This is returned by the API after each action.
    """
    session_id: str
    current_round: int = Field(ge=0, description="Current round (0-indexed)")
    total_rounds: int = Field(ge=1, description="Total rounds in the game")
    
    # Scores
    agent_score: int = 0
    human_score: int = 0
    
    # Current round info (for display)
    agent_action: Optional[ActionType] = None
    waiting_for_human: bool = True
    
    # History
    history: List[RoundResult] = Field(default_factory=list)
    
    # Game status
    game_over: bool = False
    
    # Agent info
    agent_name: str = "TitForTat"
    agent_strategy: str = "Starts cooperating, then mirrors your last action"
    
    # Payoff matrix for display
    payoff_matrix: dict = Field(default_factory=dict)
