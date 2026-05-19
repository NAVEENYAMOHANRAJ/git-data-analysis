import os
from dotenv import load_dotenv

load_dotenv()

# GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL = "https://api.github.com/graphql"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pr_dashboard.db")

# Analytics
STALE_PR_DAYS = 30
PR_FETCH_LIMIT = 100

# ML Models
ML_MODELS_DIR = "ml/trained_models"
ML_CONTAMINATION = 0.1  # For Isolation Forest
ML_KMEANS_CLUSTERS = 3

# API
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True

# CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]
