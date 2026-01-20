"""
Agent Implementations for Prisoners Dilemma

Contains the base agent class and specific strategy implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from backend.environment import Action


class BaseAgent(ABC):
    """
    Abstract base class for Prisoners Dilemma agents.
    
    All agents must implement select_action() and update().
    """
    
    def __init__(self, name: str = "Agent"):
        """
        Initialize the agent.
        
        Args:
            name: Human-readable name for the agent
        """
        self.name = name
        self.history: List[Action] = []  # Agent's own action history
        self.opponent_history: List[Action] = []  # Opponent's action history
    
    @abstractmethod
    def select_action(self) -> Action:
        """
        Select an action for the current round.
        
        Returns:
            The chosen Action (COOPERATE or DEFECT)
        """
        pass
    
    def update(self, own_action: Action, opponent_action: Action) -> None:
        """
        Update agent's state after a round.
        
        Args:
            own_action: The action this agent took
            opponent_action: The action the opponent took
        """
        self.history.append(own_action)
        self.opponent_history.append(opponent_action)
    
    def reset(self) -> None:
        """Reset agent state for a new game."""
        self.history = []
        self.opponent_history = []
    
    def get_info(self) -> dict:
        """Return agent info for API responses."""
        return {
            "name": self.name,
            "strategy": self.__class__.__name__,
            "rounds_played": len(self.history)
        }


class TitForTatAgent(BaseAgent):
    """
    Tit-for-Tat Strategy Agent.
    
    - Cooperates on the first round
    - After that, mirrors the opponent's last action
    
    This is one of the most successful strategies in iterated PD tournaments.
    """
    
    def __init__(self, name: str = "TitForTat"):
        """Initialize the Tit-for-Tat agent."""
        super().__init__(name=name)
    
    def select_action(self) -> Action:
        """
        Select action based on Tit-for-Tat strategy.
        
        Returns:
            COOPERATE on first round, then mirrors opponent's last action
        """
        if len(self.opponent_history) == 0:
            # First round: always cooperate
            return Action.COOPERATE
        else:
            # Mirror opponent's last action
            return self.opponent_history[-1]


class AlwaysCooperateAgent(BaseAgent):
    """Agent that always cooperates."""
    
    def __init__(self, name: str = "AlwaysCooperate"):
        super().__init__(name=name)
    
    def select_action(self) -> Action:
        return Action.COOPERATE


class AlwaysDefectAgent(BaseAgent):
    """Agent that always defects."""
    
    def __init__(self, name: str = "AlwaysDefect"):
        super().__init__(name=name)
    
    def select_action(self) -> Action:
        return Action.DEFECT


class RandomAgent(BaseAgent):
    """Agent that randomly cooperates or defects."""
    
    def __init__(self, name: str = "Random", seed: Optional[int] = None):
        super().__init__(name=name)
        import random
        self._rng = random.Random(seed)
    
    def select_action(self) -> Action:
        return self._rng.choice([Action.COOPERATE, Action.DEFECT])
