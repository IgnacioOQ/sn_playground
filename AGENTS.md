# AGENTS.md

## SHORT ADVICE
- The whole trick is providing the AI Assistants with context, and this is done using the *.md files (AGENTS.md, AGENTS_LOG.md, and the AI_AGENTS folder)
- Learn how to work the Github, explained below.
- Keep logs of changes in AGENTS_LOG.md
- Make sure to execute the HOUSEKEEPING.md protocol often.
- Always ask several forms of verification, so because the self-loop of the chain of thought improves performance.
- Impose restrictions and constraints explicitly in the context.

## HUMAN-ASSISTANT WORKFLOW
1. Open the assistant and load the ai-agents-branch into their local repositories. Do this by commanding them to first of all read the AGENTS.md file.
2. Work on the ASSISTANT, making requests, modifying code, etc.
3. IMPORTANT: GIT MECHANISM
    3.1. This is basically solved in Antigravity, but Jules (and maybe Claude) push the changes into a newly generated branch. In my case, this is `jules-sync-main-v1-15491954756027628005`. **This is different from the `ai-agents-branch`!!**
    3.2. So what you need to do is merge the newly generated branch and the `ai-agents-branch` often. Usually in the direction from `jules-sync-main-v1-15491954756027628005` to `ai-agents-branch`. I do this by:
        3.2.1. Going to pull requests.
        3.2.2. New Pull request
        3.2.3. Base: `ai-agents-branch`, Compare: `jules-sync-main-v1-15491954756027628005` (arrow in the right direction).
        3.2.4. Follow through. It should allow to merge and there should not be incompatibilities. If there are incompatibilities, you can delete the `ai-agents-branch` and create a new one cloning the `jules-sync-main-v1-15491954756027628005` one. After deleting `ai-agents-branch`, go to the `jules-sync-main-v1-15491954756027628005` branch, look at the dropdown bar with the branches (not the link), and create a new copy.
4. It is very useful to use specialized agents for different sectors of the code. 
5. Enjoy!

## WORKFLOW & TOOLING

*   **Documentation Logs (`AGENTS_LOG.md`):**
    *   **Rule:** Every agent that performs a significant intervention or modifies the codebase **MUST** update the `AGENTS_LOG.md` file.
    *   **Action:** Append a new entry under the "Intervention History" section summarizing the task, the changes made, and the date.

## DEVELOPMENT RULES & CONSTRAINTS
1.  **Immutable Core Files:** Do not modify 
    *   If you need to change the logic of an agent or the model, you must create a **new version** (e.g., a subclass or a new file) rather than modifying the existing classes in place.
2.  **Consistency:** Ensure any modifications or new additions remain as consistent as possible with the logic and structure of the `main` branch.
3.  **Coding Conventions:** Always keep the coding conventions pristine.

## CONTEXT FINE-TUNING
You cannot "fine-tune" an AI agent (change its underlying neural network weights) with files in this repository. **However**, you **CAN** achieve a similar result using **Context**.

**How it works (The "Context" Approach):**
If you add textbooks or guides to the repository (preferably as Markdown `.md` or text files), agents can read them. You should then update the relevant agent instructions (e.g., `AI_AGENTS/LINEARIZE_AGENT.md`) to include a directive like:

> "Before implementing changes, read `docs/linearization_textbook.md` and `docs/jax_guide.md`. Use the specific techniques described in Chapter 4 for sparse matrix operations."

**Why this is effective:**
1.  **Specific Knowledge:** Adding a specific textbook helps if you want a *specific style* of implementation (e.g., using `jax.lax.scan` vs `vmap` in a particular way).
2.  **Domain Techniques:** If the textbook contains specific math shortcuts for your network types, providing the text allows the agent to apply those exact formulas instead of generic ones.

**Recommendation:**
If you want to teach an agent a new language (like JAX) or technique:
1.  Add the relevant chapters as **text/markdown** files.
2.  Update the agent's instruction file (e.g., `AI_AGENTS/LINEARIZE_AGENT.md`) to reference them.
3.  Ask the agent to "Refactor the code using the techniques in [File X]".

## LOCAL PROJECT DESCRIPTION

### Project Overview
**Iterated Prisoners Dilemma Simulation** - A web-based game where human subjects play against AI agents in the classic iterated prisoners dilemma. The backend handles all game logic and agent strategies, while the frontend provides a premium dark-themed UI for human interaction.

### Setup & Testing
*   **Install Dependencies:** `pip install -r requirements.txt` (backend) and `cd frontend && npm install` (frontend)
*   **Run Backend:** `python -m uvicorn backend.api.main:app --reload --port 8000`
*   **Run Frontend:** `cd frontend && npm run dev`
*   **Run Tests:** `python -m pytest tests/ -v`

### Key Architecture & Logic

#### 1. Architecture (Monorepo)
*   **Backend (`backend/`)**: Python/FastAPI application handling all game logic, agent strategies, and session data logging.
*   **Frontend (`frontend/`)**: React/Vite/TypeScript application for the user interface, communicating with backend via REST API.

#### 2. Game Logic
*   **Payoff Matrix (Classic PD):**
    *   Both Cooperate: R=3, R=3
    *   Both Defect: P=1, P=1
    *   One Defects: T=5 (defector), S=0 (cooperator)
*   **Constraints:** T > R > P > S and 2R > T + S

#### 3. Agents (`backend/agents.py`)
*   **`TitForTatAgent`**: Cooperates first, then mirrors opponent's last action
*   **`AlwaysCooperateAgent`**: Always cooperates
*   **`AlwaysDefectAgent`**: Always defects
*   **`RandomAgent`**: Randomly chooses

#### 4. Simulation Loop
*   **Step:**
    1.  Game initializes; agent pre-selects action for round 1
    2.  Frontend displays agent's action
    3.  Human selects Cooperate or Defect
    4.  Backend calculates payoffs and updates scores
    5.  Agent observes human action and prepares next round
    6.  After final round (default: 10), session data saved to JSON

### Key Files and Directories

#### Directory Structure
```
sn_playground/
├── backend/
│   ├── api/
│   │   ├── main.py          # FastAPI app with CORS
│   │   ├── routes.py        # /health, /simulation/init, /simulation/step
│   │   └── session.py       # In-memory session storage
│   ├── engine/
│   │   ├── config.py        # SimulationConfig (num_rounds, agent_type)
│   │   ├── state.py         # GameState, RoundResult Pydantic models
│   │   └── model.py         # GameSession orchestrator
│   ├── agents.py            # TitForTat, AlwaysCooperate, AlwaysDefect, Random
│   ├── environment.py       # PayoffMatrix, payoff calculation
│   └── logging.py           # Session data export to JSON
├── frontend/
│   └── src/
│       ├── App.tsx          # Health check + root component
│       ├── Controls.tsx     # Game UI (config, actions, history)
│       └── *.css            # Premium dark theme
├── data/
│   └── sessions/            # JSON files for each completed game
├── tests/
│   ├── test_environment.py  # Payoff calculation tests
│   └── test_agents.py       # Agent behavior tests (20 tests)
└── requirements.txt         # fastapi, uvicorn, pydantic
```

#### File Dependencies & Logic
*   `backend/engine/model.py` depends on `agents.py`, `environment.py`, and `logging.py`
*   `backend/api/routes.py` depends on `engine/model.py` and `api/session.py`
*   React frontend depends on FastAPI backend running on port 8000

#### Data Logging
Session data is automatically saved to `data/sessions/{session_id}.json` when a game ends. Format:
```json
{
  "session_id": "uuid",
  "timestamp": "ISO-8601",
  "metadata": { "agent_name": "TitForTat", ... },
  "final_scores": { "human": 25, "agent": 22 },
  "steps": [
    { "step": 0, "human_action": "cooperate", "agent_action": "cooperate", 
      "outcome_human": 3, "outcome_agent": 3, "next_step": 1, "done": false },
    ...
  ]
}
```

**Testing & Verification:**
*   **`tests/test_environment.py`**: Verifies payoff calculations for all action combinations
*   **`tests/test_agents.py`**: Verifies TitForTat mirrors correctly, other agent behaviors

