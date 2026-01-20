import { useState } from 'react'
import './Controls.css'

type ActionType = 'cooperate' | 'defect'

interface RoundResult {
    round_number: number
    agent_action: ActionType
    human_action: ActionType
    agent_payoff: number
    human_payoff: number
}

interface PayoffMatrix {
    labels: {
        T: number
        R: number
        P: number
        S: number
    }
}

interface GameState {
    session_id: string
    current_round: number
    total_rounds: number
    agent_score: number
    human_score: number
    agent_action: ActionType | null
    waiting_for_human: boolean
    history: RoundResult[]
    game_over: boolean
    agent_name: string
    agent_strategy: string
    payoff_matrix: PayoffMatrix
}

interface GameConfig {
    numRounds: number
    agentType: string
}

function Controls() {
    const [config, setConfig] = useState<GameConfig>({
        numRounds: 10,
        agentType: 'tit_for_tat'
    })
    const [state, setState] = useState<GameState | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const startGame = async () => {
        setLoading(true)
        setError(null)

        try {
            const response = await fetch('http://localhost:8000/simulation/init', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    num_rounds: config.numRounds,
                    agent_type: config.agentType
                })
            })

            const data = await response.json()
            setState(data.state)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to start game')
        } finally {
            setLoading(false)
        }
    }

    const makeChoice = async (action: ActionType) => {
        if (!state || state.game_over) return

        setLoading(true)
        try {
            const response = await fetch('http://localhost:8000/simulation/step', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: state.session_id,
                    action: action
                })
            })

            const data = await response.json()
            setState(data.state)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to make choice')
        } finally {
            setLoading(false)
        }
    }

    const resetGame = () => {
        setState(null)
        setError(null)
    }

    // Configuration screen
    if (!state) {
        return (
            <div className="controls-container">
                <div className="config-card">
                    <h2>Game Setup</h2>

                    <div className="config-field">
                        <label htmlFor="numRounds">Number of Rounds</label>
                        <input
                            type="number"
                            id="numRounds"
                            value={config.numRounds}
                            onChange={(e) => setConfig({
                                ...config,
                                numRounds: parseInt(e.target.value) || 10
                            })}
                            min={1}
                            max={100}
                        />
                    </div>

                    <div className="config-field">
                        <label htmlFor="agentType">Opponent Strategy</label>
                        <select
                            id="agentType"
                            value={config.agentType}
                            onChange={(e) => setConfig({
                                ...config,
                                agentType: e.target.value
                            })}
                        >
                            <option value="tit_for_tat">Tit-for-Tat</option>
                            <option value="always_cooperate">Always Cooperate</option>
                            <option value="always_defect">Always Defect</option>
                            <option value="random">Random</option>
                        </select>
                    </div>

                    <button
                        className="btn-primary"
                        onClick={startGame}
                        disabled={loading}
                    >
                        {loading ? 'Starting...' : 'Start Game'}
                    </button>

                    {error && <p className="error-message">{error}</p>}
                </div>

                <div className="info-card">
                    <h3>How to Play</h3>
                    <p>In each round, both you and the AI choose to <strong>Cooperate</strong> or <strong>Defect</strong>:</p>
                    <ul className="payoff-list">
                        <li><span className="coop">Both Cooperate</span>: You both get 3 points</li>
                        <li><span className="defect">Both Defect</span>: You both get 1 point</li>
                        <li><span className="mixed">You Defect, AI Cooperates</span>: You get 5, AI gets 0</li>
                        <li><span className="mixed">You Cooperate, AI Defects</span>: You get 0, AI gets 5</li>
                    </ul>
                </div>
            </div>
        )
    }

    // Game screen
    return (
        <div className="controls-container">
            {/* Score display */}
            <div className="score-panel">
                <div className="score-card you">
                    <span className="score-label">You</span>
                    <span className="score-value">{state.human_score}</span>
                </div>
                <div className="vs">VS</div>
                <div className="score-card agent">
                    <span className="score-label">{state.agent_name}</span>
                    <span className="score-value">{state.agent_score}</span>
                </div>
            </div>

            {/* Round info */}
            <div className="round-info">
                <span className="round-number">
                    Round {state.current_round + 1} of {state.total_rounds}
                </span>
                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${((state.current_round) / state.total_rounds) * 100}%` }}
                    />
                </div>
            </div>

            {/* Game over message */}
            {state.game_over ? (
                <div className="game-over-card">
                    <h2>Game Over!</h2>
                    <div className="final-result">
                        {state.human_score > state.agent_score ? (
                            <span className="winner you-won">🎉 You Won!</span>
                        ) : state.human_score < state.agent_score ? (
                            <span className="winner agent-won">AI Wins!</span>
                        ) : (
                            <span className="winner tie">It's a Tie!</span>
                        )}
                    </div>
                    <p className="final-scores">
                        Final: You {state.human_score} - {state.agent_score} {state.agent_name}
                    </p>
                    <button className="btn-primary" onClick={resetGame}>
                        Play Again
                    </button>
                </div>
            ) : (
                <>
                    {/* Agent's action reveal */}
                    <div className="agent-action-card">
                        <p className="action-label">The AI has chosen:</p>
                        <div className={`action-reveal ${state.agent_action}`}>
                            {state.agent_action === 'cooperate' ? '🤝 Cooperate' : '😈 Defect'}
                        </div>
                    </div>

                    {/* Human choice buttons */}
                    <div className="choice-section">
                        <p className="choice-prompt">What's your move?</p>
                        <div className="choice-buttons">
                            <button
                                className="choice-btn cooperate"
                                onClick={() => makeChoice('cooperate')}
                                disabled={loading}
                            >
                                <span className="choice-icon">🤝</span>
                                <span className="choice-text">Cooperate</span>
                            </button>
                            <button
                                className="choice-btn defect"
                                onClick={() => makeChoice('defect')}
                                disabled={loading}
                            >
                                <span className="choice-icon">😈</span>
                                <span className="choice-text">Defect</span>
                            </button>
                        </div>
                    </div>
                </>
            )}

            {/* History table */}
            {state.history.length > 0 && (
                <div className="history-card">
                    <h3>Round History</h3>
                    <table className="history-table">
                        <thead>
                            <tr>
                                <th>Round</th>
                                <th>You</th>
                                <th>AI</th>
                                <th>Your Points</th>
                                <th>AI Points</th>
                            </tr>
                        </thead>
                        <tbody>
                            {state.history.map((round) => (
                                <tr key={round.round_number}>
                                    <td>{round.round_number}</td>
                                    <td className={round.human_action}>
                                        {round.human_action === 'cooperate' ? '🤝' : '😈'}
                                    </td>
                                    <td className={round.agent_action}>
                                        {round.agent_action === 'cooperate' ? '🤝' : '😈'}
                                    </td>
                                    <td className="points">{round.human_payoff}</td>
                                    <td className="points">{round.agent_payoff}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Restart button */}
            {!state.game_over && (
                <button className="btn-secondary" onClick={resetGame}>
                    Restart Game
                </button>
            )}

            {error && <p className="error-message">{error}</p>}
        </div>
    )
}

export default Controls
