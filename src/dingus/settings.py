"""settings.py

Settings for the Dingus app.
"""

import os

APP_TITLE = "DINGUS | Chat with Logs"

MODEL_PRICING = {
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
}

TRUNCATE_LOGS = int(100)

LOGGING_FILE = "/logs/dingus.log"
LOG_DATA_FILE_PATH = "/data/loki_stream.json"
LOKI_QUERY_RANGE_ENDPOINT = "/loki/api/v1/query_range"
LOKI_URL = os.getenv("LOKI_URL")
LOKI_JOB_NAME = os.getenv("LOKI_JOB_NAME")
LOKI_END_HOURS_AGO = 1

QDRANT_PORT = os.getenv("QDRANT_PORT")
QDRANT_HOST = f"{os.getenv('QDRANT_HOST')}:{QDRANT_PORT}"
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "defaul_collection")
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
QDRANT_VECTOR_SIZE = 384  # 384D for MiniLM

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
