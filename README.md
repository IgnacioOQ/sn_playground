# Iterated Prisoners Dilemma Simulation

## Project Overview
**Iterated Prisoners Dilemma Simulation** is a web-based game where human subjects play against AI agents in the classic iterated prisoners dilemma. The backend handles all game logic and agent strategies, while the frontend provides a premium dark-themed UI for human interaction.

## Setup & Testing

### Prerequisites
- Python 3.x
- Node.js & npm

### Installation
1.  **Install Backend Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Install Frontend Dependencies:**
    ```bash
    cd frontend && npm install
    ```

### Running the Application
1.  **Run Backend:**
    ```bash
    python -m uvicorn backend.api.main:app --reload --port 8000
    ```
    The API will be available at `http://localhost:8000`.

2.  **Run Frontend:**
    ```bash
    cd frontend && npm run dev
    ```
    The UI will be available at `http://localhost:5173` (default Vite port).

### Running Tests
To run the backend unit tests:
```bash
python -m pytest tests/ -v
```

## Key Architecture & Logic

### 1. Architecture (Monorepo)
*   **Backend (`backend/`)**: Python/FastAPI application handling all game logic, agent strategies, and session data logging.
*   **Frontend (`frontend/`)**: React/Vite/TypeScript application for the user interface, communicating with backend via REST API.

### 2. Game Logic
*   **Payoff Matrix (Classic PD):**
    *   Both Cooperate: R=3, R=3
    *   Both Defect: P=1, P=1
    *   One Defects: T=5 (defector), S=0 (cooperator)
*   **Constraints:** T > R > P > S and 2R > T + S

### 3. Agents (`backend/agents.py`)
*   **`TitForTatAgent`**: Cooperates first, then mirrors opponent's last action
*   **`AlwaysCooperateAgent`**: Always cooperates
*   **`AlwaysDefectAgent`**: Always defects
*   **`RandomAgent`**: Randomly chooses

### 4. Simulation Loop
1.  Game initializes; agent pre-selects action for round 1
2.  Frontend displays agent's action
3.  Human selects Cooperate or Defect
4.  Backend calculates payoffs and updates scores
5.  Agent observes human action and prepares next round
6.  After final round (default: 10), session data saved to JSON

## Directory Structure

```
sn_playground/
├── backend/
│   ├── api/             # FastAPI app, routes, session management
│   ├── engine/          # Game logic, state models, simulation configuration
│   ├── agents.py        # Agent implementations
│   ├── environment.py   # Payoff matrix and environment definitions
│   └── logging.py       # Session data logging
├── frontend/
│   └── src/             # React application source
├── data/
│   └── sessions/        # JSON files for completed game sessions
├── AI_AGENTS/           #- Documentation and guides for AI assistants
├── tests/               # Unit tests for agents and environment
└── requirements.txt     # Python dependencies
```

## Data Logging
Session data is automatically saved to `data/sessions/{session_id}.json` when a game ends. verified JSON format includes session metadata, final scores, and step-by-step actions and outcomes.
