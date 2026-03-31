from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# 파일 경로
INPUT_FILE = BASE_DIR / "problem.xlsx"
OUTPUT_FILE = BASE_DIR / "response_results.xlsx"

SYSTEM_PROMPT_FILE = BASE_DIR / "prompts" / "system_prompt.txt"
RAG_BLOCKS_FILE = BASE_DIR / "rag_data" / "knowledge_blocks.json"

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
