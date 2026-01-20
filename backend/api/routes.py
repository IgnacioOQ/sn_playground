"""
API Route Definitions

All endpoint definitions for the Prisoners Dilemma game.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

from backend.engine.config import SimulationConfig
from backend.engine.model import GameSession
from backend.engine.state import GameState
from backend.api.session import get_session, store_session


# Create router
router = APIRouter()


# Request/Response Models
class InitRequest(BaseModel):
    """Request body for initializing a new game."""
    num_rounds: int = 10
    agent_type: str = "tit_for_tat"


class StepRequest(BaseModel):
    """Request body for taking a step in the game."""
    session_id: str
    action: Literal["cooperate", "defect"]


class InitResponse(BaseModel):
    """Response from game initialization."""
    session_id: str
    state: GameState


class StepResponse(BaseModel):
    """Response from taking a step."""
    state: GameState


# Endpoints
@router.get("/health")
def health_check():
    """Health check endpoint - verifies backend is running."""
    return {"status": "ok"}


@router.post("/simulation/init", response_model=InitResponse)
def init_simulation(request: InitRequest):
    """
    Initialize a new game session.
    
    Creates a new game with the specified configuration and returns
    the initial state including the agent's first action.
    """
    # Create config
    config = SimulationConfig(
        num_rounds=request.num_rounds,
        agent_type=request.agent_type
    )
    
    # Create session
    session = GameSession.create(config)
    
    # Store session
    store_session(session)
    
    return InitResponse(
        session_id=session.session_id,
        state=session.get_state()
    )


@router.post("/simulation/step", response_model=StepResponse)
def simulation_step(request: StepRequest):
    """
    Process a human action and advance the game.
    
    The human's action is processed against the agent's pre-selected
    action, payoffs are calculated, and the game advances to the next round.
    """
    # Get session
    session = get_session(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if game is already over
    if session.is_game_over():
        raise HTTPException(status_code=400, detail="Game is already over")
    
    # Process step
    new_state = session.step(request.action)
    
    return StepResponse(state=new_state)


@router.get("/simulation/state/{session_id}", response_model=GameState)
def get_game_state(session_id: str):
    """
    Get the current state of a game session.
    
    Useful for refreshing the frontend or recovering from disconnection.
    """
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.get_state()
