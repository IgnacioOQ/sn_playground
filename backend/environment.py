"""
Prisoners Dilemma Environment

Implements the classic iterated prisoners dilemma game logic.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Action(str, Enum):
    """Possible actions in the Prisoners Dilemma."""
    COOPERATE = "cooperate"
    DEFECT = "defect"


@dataclass
class PayoffMatrix:
    """
    Classic Prisoners Dilemma payoff matrix.
    
    Constraints satisfied:
    - T > R > P > S (Temptation > Reward > Punishment > Sucker)
    - 2R > T + S (Mutual cooperation is better than alternating)
    
    Default values: T=5, R=3, P=1, S=0
    """
    temptation: int = 5  # T: Defect while opponent cooperates
    reward: int = 3       # R: Both cooperate
    punishment: int = 1   # P: Both defect
    sucker: int = 0       # S: Cooperate while opponent defects
    
    def __post_init__(self):
        """Validate PD constraints."""
        assert self.temptation > self.reward > self.punishment > self.sucker, \
            "Must satisfy T > R > P > S"
        assert 2 * self.reward > self.temptation + self.sucker, \
            "Must satisfy 2R > T + S"


class PrisonersDilemmaEnvironment:
    """
    Environment for the iterated Prisoners Dilemma game.
    
    The environment calculates payoffs based on both players' actions.
    """
    
    def __init__(self, payoff_matrix: PayoffMatrix = None):
        """
        Initialize the environment.
        
        Args:
            payoff_matrix: Custom payoff matrix. Uses default if None.
        """
        self.payoff_matrix = payoff_matrix or PayoffMatrix()
    
    def calculate_payoffs(
        self, 
        action1: Action, 
        action2: Action
    ) -> Tuple[int, int]:
        """
        Calculate payoffs for both players.
        
        Args:
            action1: First player's action
            action2: Second player's action
            
        Returns:
            Tuple of (player1_payoff, player2_payoff)
        """
        pm = self.payoff_matrix
        
        if action1 == Action.COOPERATE and action2 == Action.COOPERATE:
            return (pm.reward, pm.reward)
        elif action1 == Action.DEFECT and action2 == Action.DEFECT:
            return (pm.punishment, pm.punishment)
        elif action1 == Action.DEFECT and action2 == Action.COOPERATE:
            return (pm.temptation, pm.sucker)
        else:  # action1 == COOPERATE and action2 == DEFECT
            return (pm.sucker, pm.temptation)
    
    def get_payoff_description(self) -> dict:
        """Return payoff matrix as a dictionary for API responses."""
        pm = self.payoff_matrix
        return {
            "mutual_cooperation": (pm.reward, pm.reward),
            "mutual_defection": (pm.punishment, pm.punishment),
            "temptation_vs_sucker": (pm.temptation, pm.sucker),
            "labels": {
                "T": pm.temptation,
                "R": pm.reward,
                "P": pm.punishment,
                "S": pm.sucker
            }
        }
