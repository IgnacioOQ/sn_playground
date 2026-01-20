import { useState, useEffect } from 'react'
import Controls from './Controls'
import './App.css'

function App() {
    const [health, setHealth] = useState<string | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetch('http://localhost:8000/health')
            .then(res => res.json())
            .then(data => setHealth(data.status))
            .catch(err => setError(err.message))
    }, [])

    return (
        <div className="app-container">
            <header className="app-header">
                <h1>🎮 Iterated Prisoner's Dilemma</h1>
                <p className="subtitle">Play against a strategic AI agent</p>
            </header>
            
            <div className="status-card">
                <span className="status-label">Backend Status:</span>
                {error ? (
                    <span className="status-indicator error">❌ {error}</span>
                ) : health ? (
                    <span className="status-indicator success">✓ Connected</span>
                ) : (
                    <span className="status-indicator loading">⏳ Connecting...</span>
                )}
            </div>
            
            {health === 'ok' && <Controls />}
            
            {!health && !error && (
                <div className="loading-message">
                    <p>Waiting for backend connection...</p>
                    <p className="hint">Make sure the backend is running on port 8000</p>
                </div>
            )}
        </div>
    )
}

export default App
