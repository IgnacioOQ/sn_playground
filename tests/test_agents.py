"""
Tests for Prisoners Dilemma Agents
"""

import pytest
from backend.environment import Action
from backend.agents import (
    TitForTatAgent,
    AlwaysCooperateAgent,
    AlwaysDefectAgent,
    RandomAgent
)


class TestTitForTatAgent:
    """Tests for the Tit-for-Tat strategy."""
    
    @pytest.fixture
    def agent(self):
        """Create a fresh TitForTat agent."""
        return TitForTatAgent()
    
    def test_first_move_cooperates(self, agent):
        """TitForTat should cooperate on the first move."""
        action = agent.select_action()
        assert action == Action.COOPERATE
    
    def test_mirrors_cooperation(self, agent):
        """TitForTat mirrors opponent's cooperation."""
        # First move
        action1 = agent.select_action()
        agent.update(action1, Action.COOPERATE)
        
        # Second move: should cooperate (mirroring opponent)
        action2 = agent.select_action()
        assert action2 == Action.COOPERATE
    
    def test_mirrors_defection(self, agent):
        """TitForTat mirrors opponent's defection."""
        # First move
        action1 = agent.select_action()
        agent.update(action1, Action.DEFECT)
        
        # Second move: should defect (mirroring opponent)
        action2 = agent.select_action()
        assert action2 == Action.DEFECT
    
    def test_forgives_after_cooperation(self, agent):
        """TitForTat returns to cooperation after opponent cooperates."""
        # Round 1: Agent cooperates, opponent defects
        agent.update(Action.COOPERATE, Action.DEFECT)
        
        # Round 2: Agent defects (mirroring), opponent cooperates
        action2 = agent.select_action()
        assert action2 == Action.DEFECT
        agent.update(action2, Action.COOPERATE)
        
        # Round 3: Agent should cooperate again
        action3 = agent.select_action()
        assert action3 == Action.COOPERATE
    
    def test_sequence_of_moves(self, agent):
        """Test a complete sequence of moves."""
        # Round 1: First move -> Cooperate
        assert agent.select_action() == Action.COOPERATE
        agent.update(Action.COOPERATE, Action.COOPERATE)
        
        # Round 2: Mirror coop -> Cooperate
        assert agent.select_action() == Action.COOPERATE
        agent.update(Action.COOPERATE, Action.DEFECT)
        
        # Round 3: Mirror defect -> Defect
        assert agent.select_action() == Action.DEFECT
        agent.update(Action.DEFECT, Action.DEFECT)
        
        # Round 4: Mirror defect -> Defect
        assert agent.select_action() == Action.DEFECT
        agent.update(Action.DEFECT, Action.COOPERATE)
        
        # Round 5: Mirror coop -> Cooperate
        assert agent.select_action() == Action.COOPERATE
    
    def test_reset(self, agent):
        """Test agent reset clears history."""
        agent.update(Action.COOPERATE, Action.DEFECT)
        agent.reset()
        
        # After reset, first move should cooperate
        assert agent.select_action() == Action.COOPERATE
        assert len(agent.history) == 0
        assert len(agent.opponent_history) == 0


class TestAlwaysCooperateAgent:
    """Tests for AlwaysCooperate strategy."""
    
    def test_always_cooperates(self):
        """Agent should always return COOPERATE."""
        agent = AlwaysCooperateAgent()
        
        for _ in range(10):
            assert agent.select_action() == Action.COOPERATE
            agent.update(Action.COOPERATE, Action.DEFECT)


class TestAlwaysDefectAgent:
    """Tests for AlwaysDefect strategy."""
    
    def test_always_defects(self):
        """Agent should always return DEFECT."""
        agent = AlwaysDefectAgent()
        
        for _ in range(10):
            assert agent.select_action() == Action.DEFECT
            agent.update(Action.DEFECT, Action.COOPERATE)


class TestRandomAgent:
    """Tests for Random strategy."""
    
    def test_deterministic_with_seed(self):
        """With same seed, agent produces same sequence."""
        agent1 = RandomAgent(seed=42)
        agent2 = RandomAgent(seed=42)
        
        actions1 = [agent1.select_action() for _ in range(10)]
        actions2 = [agent2.select_action() for _ in range(10)]
        
        assert actions1 == actions2
    
    def test_produces_both_actions(self):
        """Random agent should produce both actions over many rounds."""
        agent = RandomAgent(seed=123)
        actions = [agent.select_action() for _ in range(100)]
        
        assert Action.COOPERATE in actions
        assert Action.DEFECT in actions
