"""
Tests for Prisoners Dilemma Environment
"""

import pytest
from backend.environment import (
    Action, 
    PayoffMatrix, 
    PrisonersDilemmaEnvironment
)


class TestPayoffMatrix:
    """Tests for the PayoffMatrix dataclass."""
    
    def test_default_values(self):
        """Test default payoff values satisfy PD constraints."""
        pm = PayoffMatrix()
        assert pm.temptation == 5
        assert pm.reward == 3
        assert pm.punishment == 1
        assert pm.sucker == 0
    
    def test_constraints_t_r_p_s(self):
        """Test that T > R > P > S constraint is enforced."""
        # Valid: T=5 > R=3 > P=1 > S=0
        pm = PayoffMatrix(temptation=5, reward=3, punishment=1, sucker=0)
        assert pm.temptation > pm.reward > pm.punishment > pm.sucker
    
    def test_constraint_2r_greater_than_t_plus_s(self):
        """Test that 2R > T + S constraint is satisfied."""
        pm = PayoffMatrix()
        assert 2 * pm.reward > pm.temptation + pm.sucker


class TestPrisonersDilemmaEnvironment:
    """Tests for the game environment."""
    
    @pytest.fixture
    def env(self):
        """Create a default environment."""
        return PrisonersDilemmaEnvironment()
    
    def test_mutual_cooperation(self, env):
        """Both players cooperate: both get R=3."""
        p1, p2 = env.calculate_payoffs(Action.COOPERATE, Action.COOPERATE)
        assert p1 == 3
        assert p2 == 3
    
    def test_mutual_defection(self, env):
        """Both players defect: both get P=1."""
        p1, p2 = env.calculate_payoffs(Action.DEFECT, Action.DEFECT)
        assert p1 == 1
        assert p2 == 1
    
    def test_player1_defects_player2_cooperates(self, env):
        """Player 1 defects, Player 2 cooperates: T=5 vs S=0."""
        p1, p2 = env.calculate_payoffs(Action.DEFECT, Action.COOPERATE)
        assert p1 == 5  # Temptation
        assert p2 == 0  # Sucker
    
    def test_player1_cooperates_player2_defects(self, env):
        """Player 1 cooperates, Player 2 defects: S=0 vs T=5."""
        p1, p2 = env.calculate_payoffs(Action.COOPERATE, Action.DEFECT)
        assert p1 == 0  # Sucker
        assert p2 == 5  # Temptation
    
    def test_get_payoff_description(self, env):
        """Test payoff description for API."""
        desc = env.get_payoff_description()
        assert "mutual_cooperation" in desc
        assert "mutual_defection" in desc
        assert "temptation_vs_sucker" in desc
        assert desc["labels"]["T"] == 5


class TestAction:
    """Tests for the Action enum."""
    
    def test_action_values(self):
        """Test action string values."""
        assert Action.COOPERATE.value == "cooperate"
        assert Action.DEFECT.value == "defect"
    
    def test_action_from_string(self):
        """Test creating actions from strings."""
        assert Action("cooperate") == Action.COOPERATE
        assert Action("defect") == Action.DEFECT
