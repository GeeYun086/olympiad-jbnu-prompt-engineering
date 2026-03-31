from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 파일 경로
INPUT_FILE = BASE_DIR / "problem.xlsx"
OUTPUT_FILE = BASE_DIR / "response_results.xlsx"

SYSTEM_PROMPT_FILE = BASE_DIR / "prompts" / "system_prompt.txt"
RAG_BLOCKS_FILE = BASE_DIR / "rag_data" / "knowledge_blocks.json"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

# API 설정
BASE_URL = "https://ryeon.elpai.org/submit/v1"
API_KEY = "dummy-key"
MODEL_NAME = "olympiad"

# 생성 옵션
TEMPERATURE = 0.7
MAX_TOKENS = None
STREAM = False

# RAG 설정
MAX_RAG_BLOCKS = 3
MIN_RAG_SCORE = 1

# 실행 모드
USE_MOCK = True
