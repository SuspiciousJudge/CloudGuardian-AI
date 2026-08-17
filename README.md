# CloudGuardian AI

Enterprise AI Incident Response Platform built with Google ADK and Vertex AI.

## Setup

1. Install dependencies:
pip install -r app/requirements.txt

2. Configure .env:
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1

3. Run locally:
uvicorn app.main:app --reload

4. Open Swagger UI:
http://127.0.0.1:8000/docs

## Test

POST /analyze
{
  "user_id": "rahul",
  "workflow": "incident",
  "message": "Why is payment service failing?"
}

## Deploy to Cloud Run

gcloud run deploy cloudguardian-ai \
--source . \
--region us-central1 \
--allow-unauthenticated \
--set-env-vars GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1
