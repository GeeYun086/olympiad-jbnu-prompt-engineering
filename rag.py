import json
import re
from typing import List, Dict, Any

from config import RAG_BLOCKS_FILE, MAX_RAG_BLOCKS, MIN_RAG_SCORE


def load_knowledge_blocks() -> List[Dict[str, Any]]:
    if not RAG_BLOCKS_FILE.exists():
        raise FileNotFoundError(f"RAG 블록 파일이 없습니다: {RAG_BLOCKS_FILE}")

    with open(RAG_BLOCKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("knowledge_blocks.json은 리스트 형태여야 합니다.")

    return data


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^0-9a-z가-힣\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def score_block(question: str, block: Dict[str, Any]) -> int:
    normalized_question = normalize_text(question)
    score = 0

    keywords = block.get("keywords", [])
    synonyms = block.get("synonyms", [])
    topic = block.get("topic", "")

    for keyword in keywords:
        if normalize_text(keyword) in normalized_question:
            score += 3

    for synonym in synonyms:
        if normalize_text(synonym) in normalized_question:
            score += 2

    if topic and normalize_text(topic) in normalized_question:
        score += 1

    return score


def format_block(block: Dict[str, Any]) -> str:
    topic = block.get("topic", "unknown")
    block_type = block.get("type", "general")
    content = block.get("content", "").strip()

    return f"[TOPIC] {topic}\n[TYPE] {block_type}\n[CONTENT]\n{content}"


def select_relevant_blocks(question: str) -> List[Dict[str, Any]]:
    blocks = load_knowledge_blocks()

    scored_blocks = []
    for block in blocks:
        score = score_block(question, block)
        if score >= MIN_RAG_SCORE:
            scored_blocks.append((score, block))

    scored_blocks.sort(key=lambda x: x[0], reverse=True)

    selected = [block for score, block in scored_blocks[:MAX_RAG_BLOCKS]]
    return selected


def combine_blocks(blocks: List[Dict[str, Any]]) -> str:
    if not blocks:
        return ""

    formatted_blocks = [format_block(block) for block in blocks]
    return "\n\n---\n\n".join(formatted_blocks)


def get_relevant_rag_info(question: str) -> Dict[str, Any]:
    selected_blocks = select_relevant_blocks(question)
    combined_context = combine_blocks(selected_blocks)

    return {
        "selected_topics": [block.get("topic", "unknown") for block in selected_blocks],
        "block_count": len(selected_blocks),
        "combined_context": combined_context
    }


def add_rag(question: str, context: str) -> str:
    if not context:
        return (
            "[질문]\n"
            f"{question}\n\n"
            "[참고사항]\n"
            "관련 문맥이 선택되지 않았습니다. 질문 자체를 바탕으로만 답변하세요."
        )

    return (
        f"{question}\n\n"
        "You may use the following sources if needed to answer the user's question. "
        "Only use them when they are directly relevant to the user's question.\n\n"
        "<BEGIN SOURCE>\n"
        f"{context}"
    )
