import os
import vertexai
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION
)
