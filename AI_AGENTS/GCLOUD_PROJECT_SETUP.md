# Google Cloud Project Setup Guide

> **Purpose:** Instructions for creating a simulation project fully integrated with the Google Cloud ecosystem (React + Firebase, FastAPI + Vertex AI, BigQuery, Cloud Storage).

---

## Required Project Structure

Every simulation project must have **6 core parts minimum**, adapted for Google Cloud:

```
project_name/
├── frontend/          # React/TypeScript + Firebase
├── backend/           # Python/FastAPI + Vertex AI + Cloud Run ready
├── database/          # BigQuery schemas & migration scripts
├── AI_AGENTS/         # Documentation for AI assistants
├── tests/             # Unit tests (pytest)
└── notebooks/         # Jupyter notebooks (Colab/Vertex Workbench)
```

---

## 1. Frontend (`frontend/`)

**Purpose:** Display layer for human subjects. Hosted on Firebase Hosting, uses Firebase Auth (optional) and Firestore (optional real-time sync).

**Required files:**
```
frontend/
├── src/
│   ├── firebase.ts       # Firebase initialization & config
│   ├── main.tsx          # React entry point
│   ├── App.tsx           # Root component
│   ├── ...
├── firebase.json         # Firebase Hosting config
├── .firebaserc           # Firebase project alias
├── vite.config.ts        # Vite configuration
└── ...
```

**Guidelines:**
- **Stack:** Vite + React + TypeScript
- **Integration:** Install Firebase SDK: `npm install firebase`
- **Hosting:** Deploy to Firebase Hosting: `firebase deploy`
- **Design:** Premium dark theme with modern aesthetics
- **Communication:** API calls to Backend (Cloud Run URL)

**Setup:**
1. Create a project in [Firebase Console](https://console.firebase.google.com/).
2. Run `npm install -g firebase-tools`.
3. `firebase login` and `firebase init` in `frontend/` (select Hosting).

---

## 2. Backend (`backend/`)

**Purpose:** Simulation logic, utilizing Vertex AI for agent intelligence. Designed to be containerized (Cloud Run).

**Required structure:**
```
backend/
├── api/
│   ├── main.py           # FastAPI app
│   └── routes.py         # Endpoints
├── engine/
│   ├── model.py          # Simulation logic
│   └── ...
├── services/
│   ├── vertex_service.py # Vertex AI SDK wrapper
│   ├── bq_service.py     # BigQuery logging
│   └── gcs_service.py    # Cloud Storage wrapper
├── Dockerfile            # Container definition for Cloud Run
├── requirements.txt      # Dependencies
└── ...
```

**Guidelines:**
- **Framework:** FastAPI
- **AI:** Use **Vertex AI SDK** (`google-cloud-aiplatform`) for LLM agents.
- **Deployment:** Containerize with Docker and deploy to **Cloud Run**.
- **Auth:** Use Google Application Default Credentials (ADC) for local dev (`gcloud auth application-default login`).

**Vertex AI Integration (`services/vertex_service.py`):**
```python
import vertexai
from vertexai.language_models import TextGenerationModel

def init_vertex():
    vertexai.init(project="your-project-id", location="us-central1")
    model = TextGenerationModel.from_pretrained("text-bison@001")
    return model
```

---

## 3. Database & Storage (`database/`)

**Purpose:** BigQuery for structured analytics (logs), Cloud Storage (GCS) for unstructured simulation artifacts (JSON dumps).

**Options:**

### Structured Data (BigQuery)
- **Library:** `google-cloud-bigquery`
- **Usage:** Stream simulation steps to BigQuery tables for analysis.
- **Setup:** Create a Dataset `simulation_logs` in BigQuery console.

### Unstructured Data (Cloud Storage)
- **Library:** `google-cloud-storage`
- **Usage:** Save complete session JSON files to a GCS bucket.
- **Setup:** Create a standard bucket `gs://your-project-sessions`.

**BigQuery Schema Example (`database/schema.json`):**
```json
[
  { "name": "session_id", "type": "STRING", "mode": "REQUIRED" },
  { "name": "step", "type": "INTEGER", "mode": "REQUIRED" },
  { "name": "human_action", "type": "STRING", "mode": "NULLABLE" },
  { "name": "agent_action", "type": "STRING", "mode": "NULLABLE" },
  { "name": "reward", "type": "FLOAT", "mode": "NULLABLE" }
]
```

---

## 4. AI_AGENTS (`AI_AGENTS/`)

**Purpose:** Documentation and instructions for AI coding assistants.

**Required files:**
```
AI_AGENTS/
├── REACT_ASSISTANT.md       # React + Firebase Setup
├── GCLOUD_PROJECT_SETUP.md  # (This file)
├── Student_Instructions.md  # Guide
└── ...
```

---

## 5. Tests (`tests/`)

**Purpose:** Unit tests for backend logic.

**Guidelines:**
- Mock GCP services (Vertex AI, BigQuery) to avoid costs/auth issues during tests.
- Use `unittest.mock` or `pytest-mock`.

---

## 6. Notebooks (`notebooks/`)

**Purpose:** Analysis using Vertex AI Workbench or Colab.

**Guidelines:**
- **BigQuery Magic:** Use `%%bigquery` magic to query results directly into Pandas DataFrames.
- **Vertex SDK:** Iterate on prompts using the SDK in notebooks before moving to backend.

---

## Quick Setup Commands (Google Cloud)

### 1. Prerequisites
```bash
# Install CLI tools
brew install --cask google-cloud-sdk
npm install -g firebase-tools

# Login
gcloud auth login
gcloud auth application-default login
firebase login
```

### 2. Create New Project
```bash
mkdir project_name && cd project_name
mkdir -p frontend backend/api backend/engine backend/services database AI_AGENTS tests notebooks
touch backend/Dockerfile backend/requirements.txt
```

### 3. Initialize Frontend (React + Firebase)
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install firebase
firebase init hosting
# (Setup "build" as public directory, configure boolean "yes" for single-page app)
```

### 4. Backend Dependencies
`backend/requirements.txt`:
```
fastapi
uvicorn
pydantic
google-cloud-aiplatform
google-cloud-bigquery
google-cloud-storage
```

### 5. Run Locally
```bash
# Backend (Ensure ADC is set)
python -m uvicorn backend.api.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev
```

### 6. Deployment (Summary)
- **Frontend:** `firebase deploy --only hosting`
- **Backend:**
  ```bash
  gcloud builds submit --tag gcr.io/PROJECT_ID/backend
  gcloud run deploy backend --image gcr.io/PROJECT_ID/backend --platform managed
  ```

---

## Checklist for GCloud Integration

- [ ] **GCP Project**: Created and Billing enabled.
- [ ] **APIs Enabled**: Vertex AI API, BigQuery API, Cloud Run API, Container Registry API.
- [ ] **Frontend**: Connected to Firebase project.
- [ ] **Backend**: `vertexai` initialized, BigQuery client configured.
- [ ] **Service Account**: Created for production (if not using default compute service account).
