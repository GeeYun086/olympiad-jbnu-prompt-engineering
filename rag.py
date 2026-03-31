from config import RAG_CONTEXT_FILE


def load_rag_context() -> str:
    if not RAG_CONTEXT_FILE.exists():
        raise FileNotFoundError(f"RAG 컨텍스트 파일이 없습니다: {RAG_CONTEXT_FILE}")

    return RAG_CONTEXT_FILE.read_text(encoding="utf-8").strip()


def add_rag(question: str) -> str:
    context = load_rag_context()

    if context:
        question = (
            question
            + '\n\nYou may use the following sources if needed to answer the user\'s question. '
              'If you don\'t know the answer, say "I don\'t know."\n\n<BEGIN SOURCE>'
            + context
        )
    return question
