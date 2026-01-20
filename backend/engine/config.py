"""
Simulation Configuration

Pydantic models for configuring the Prisoners Dilemma simulation.
"""

from pydantic import BaseModel, Field


class PayoffConfig(BaseModel):
    """Configuration for the payoff matrix."""
    temptation: int = Field(default=5, description="T: Defect while opponent cooperates")
    reward: int = Field(default=3, description="R: Both cooperate")
    punishment: int = Field(default=1, description="P: Both defect")
    sucker: int = Field(default=0, description="S: Cooperate while opponent defects")


class SimulationConfig(BaseModel):
    """
    Configuration for a Prisoners Dilemma simulation.
    
    Attributes:
        num_rounds: Number of rounds in the iterated game (default: 10)
        agent_type: Type of agent strategy to use
        payoffs: Payoff matrix configuration
    """
    num_rounds: int = Field(default=10, ge=1, le=100, description="Number of rounds")
    agent_type: str = Field(default="tit_for_tat", description="Agent strategy type")
    payoffs: PayoffConfig = Field(default_factory=PayoffConfig)
