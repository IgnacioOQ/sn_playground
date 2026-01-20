"""
Game Session Model

Main orchestrator for the Prisoners Dilemma game.
"""

from typing import Optional
import uuid

from backend.environment import PrisonersDilemmaEnvironment, PayoffMatrix, Action
from backend.agents import (
    BaseAgent, 
    TitForTatAgent, 
    AlwaysCooperateAgent, 
    AlwaysDefectAgent,
    RandomAgent
)
from backend.engine.config import SimulationConfig
from backend.engine.state import GameState, RoundResult, ActionType
from backend.logging import save_session_data


# Agent factory
AGENT_REGISTRY = {
    "tit_for_tat": TitForTatAgent,
    "always_cooperate": AlwaysCooperateAgent,
    "always_defect": AlwaysDefectAgent,
    "random": RandomAgent,
}


class GameSession:
    """
    Manages a single game session of iterated Prisoners Dilemma.
    
    Flow per round:
    1. Agent selects action (computed immediately)
    2. Frontend displays agent's action
    3. Human selects action
    4. Payoffs calculated and state updated
    """
    
    def __init__(
        self,
        session_id: str,
        config: SimulationConfig,
        agent: BaseAgent,
        environment: PrisonersDilemmaEnvironment
    ):
        """
        Initialize a game session.
        
        Args:
            session_id: Unique session identifier
            config: Simulation configuration
            agent: The AI agent to play against
            environment: The game environment
        """
        self.session_id = session_id
        self.config = config
        self.agent = agent
        self.environment = environment
        
        # Game state
        self.current_round = 0
        self.agent_score = 0
        self.human_score = 0
        self.history: list[RoundResult] = []
        
        # Current round state
        self._pending_agent_action: Optional[Action] = None
        
        # Prepare first round
        self._prepare_round()
    
    @classmethod
    def create(cls, config: SimulationConfig, session_id: Optional[str] = None) -> "GameSession":
        """
        Factory method to create a new game session.
        
        Args:
            config: Simulation configuration
            session_id: Optional session ID (generated if not provided)
            
        Returns:
            A new GameSession instance
        """
        session_id = session_id or str(uuid.uuid4())
        
        # Create agent
        agent_class = AGENT_REGISTRY.get(config.agent_type, TitForTatAgent)
        agent = agent_class()
        
        # Create environment with configured payoffs
        payoff_matrix = PayoffMatrix(
            temptation=config.payoffs.temptation,
            reward=config.payoffs.reward,
            punishment=config.payoffs.punishment,
            sucker=config.payoffs.sucker
        )
        environment = PrisonersDilemmaEnvironment(payoff_matrix)
        
        return cls(session_id, config, agent, environment)
    
    def _prepare_round(self) -> None:
        """Prepare the next round by having the agent select their action."""
        if self.current_round < self.config.num_rounds:
            self._pending_agent_action = self.agent.select_action()
    
    def step(self, human_action_str: str) -> GameState:
        """
        Process a human action and advance the game.
        
        Args:
            human_action_str: "cooperate" or "defect"
            
        Returns:
            Updated game state
        """
        if self.is_game_over():
            return self.get_state()
        
        # Parse human action
        human_action = Action(human_action_str.lower())
        agent_action = self._pending_agent_action
        
        # Calculate payoffs
        agent_payoff, human_payoff = self.environment.calculate_payoffs(
            agent_action, human_action
        )
        
        # Update scores
        self.agent_score += agent_payoff
        self.human_score += human_payoff
        
        # Record round result
        round_result = RoundResult(
            round_number=self.current_round + 1,  # 1-indexed for display
            agent_action=ActionType(agent_action.value),
            human_action=ActionType(human_action.value),
            agent_payoff=agent_payoff,
            human_payoff=human_payoff
        )
        self.history.append(round_result)
        
        # Update agent's knowledge
        self.agent.update(agent_action, human_action)
        
        # Advance to next round
        self.current_round += 1
        
        # Prepare next round if game continues
        if not self.is_game_over():
            self._prepare_round()
        else:
            # Game just ended - save session data
            self._save_session()
        
        return self.get_state()
    
    def is_game_over(self) -> bool:
        """Check if the game has ended."""
        return self.current_round >= self.config.num_rounds
    
    def get_state(self) -> GameState:
        """
        Get the current game state for frontend rendering.
        
        Returns:
            GameState with all current information
        """
        return GameState(
            session_id=self.session_id,
            current_round=self.current_round,
            total_rounds=self.config.num_rounds,
            agent_score=self.agent_score,
            human_score=self.human_score,
            agent_action=ActionType(self._pending_agent_action.value) if self._pending_agent_action else None,
            waiting_for_human=not self.is_game_over() and self._pending_agent_action is not None,
            history=self.history,
            game_over=self.is_game_over(),
            agent_name=self.agent.name,
            agent_strategy=self._get_strategy_description(),
            payoff_matrix=self.environment.get_payoff_description()
        )
    
    def _get_strategy_description(self) -> str:
        """Get a human-readable description of the agent's strategy."""
        descriptions = {
            "TitForTat": "Starts cooperating, then mirrors your last action",
            "AlwaysCooperate": "Always cooperates",
            "AlwaysDefect": "Always defects",
            "Random": "Randomly chooses to cooperate or defect",
        }
        return descriptions.get(self.agent.name, "Unknown strategy")
    
    def _save_session(self) -> None:
        """Save session data to a JSON file when game ends."""
        try:
            config_dict = {
                "num_rounds": self.config.num_rounds,
                "agent_type": self.config.agent_type,
                "payoffs": {
                    "temptation": self.config.payoffs.temptation,
                    "reward": self.config.payoffs.reward,
                    "punishment": self.config.payoffs.punishment,
                    "sucker": self.config.payoffs.sucker,
                }
            }
            
            filepath = save_session_data(
                session_id=self.session_id,
                config=config_dict,
                history=self.history,
                agent_score=self.agent_score,
                human_score=self.human_score,
                agent_name=self.agent.name,
                agent_type=self.config.agent_type
            )
            print(f"Session data saved to: {filepath}")
        except Exception as e:
            # Log error but don't crash the game
            print(f"Warning: Failed to save session data: {e}")

