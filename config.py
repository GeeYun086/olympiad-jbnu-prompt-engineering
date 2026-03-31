from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 파일 경로
INPUT_FILE = BASE_DIR / "problem.xlsx"
OUTPUT_FILE = BASE_DIR / "response_results.xlsx"

SYSTEM_PROMPT_FILE = BASE_DIR / "prompts" / "system_prompt.txt"
RAG_CONTEXT_FILE = BASE_DIR / "rag_data" / "rag_context.txt"

# API 설정
BASE_URL = "https://ryeon.elpai.org/submit/v1"
API_KEY = "dummy-key"
MODEL_NAME = "olympiad"

# 생성 옵션
TEMPERATURE = 0.7
MAX_TOKENS = None
STREAM = False
