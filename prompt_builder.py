from config import SYSTEM_PROMPT_FILE
from rag import add_rag, get_relevant_rag_info


def load_system_prompt() -> str:
    if not SYSTEM_PROMPT_FILE.exists():
        raise FileNotFoundError(f"시스템 프롬프트 파일이 없습니다: {SYSTEM_PROMPT_FILE}")

    return SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()


def build_messages(question_id, question: str) -> tuple[list[dict], dict]:
    system_prompt = load_system_prompt()
    rag_info = get_relevant_rag_info(question)
    user_message = add_rag(question, rag_info["combined_context"])

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    return messages, rag_info


def build_debug_context(rag_info: dict) -> str:
    if rag_info["combined_context"]:
        return rag_info["combined_context"]
    return ""
