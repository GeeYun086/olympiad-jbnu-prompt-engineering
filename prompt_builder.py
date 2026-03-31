from config import SYSTEM_PROMPT_FILE
from rag import add_rag


def load_system_prompt() -> str:
    if not SYSTEM_PROMPT_FILE.exists():
        raise FileNotFoundError(f"시스템 프롬프트 파일이 없습니다: {SYSTEM_PROMPT_FILE}")

    return SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()


def build_messages(question_id, question: str) -> list[dict]:
    system_prompt = load_system_prompt()
    user_message = add_rag(question)

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
