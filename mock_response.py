def generate_mock_response(question: str, rag_info: dict) -> dict:
    selected_topics = rag_info.get("selected_topics", [])
    topic_text = ", ".join(selected_topics) if selected_topics else "없음"

    if selected_topics:
        response_text = (
            f"이 응답은 mock 모드에서 생성되었습니다. "
            f"질문과 관련된 주제로 {topic_text} 블록이 선택되었습니다. "
            f"실제 API 서버 없이도 파이프라인 구조와 RAG 선택 흐름을 검증할 수 있습니다."
        )
    else:
        response_text = (
            "이 응답은 mock 모드에서 생성되었습니다. "
            "질문과 관련된 RAG 블록이 선택되지 않아, 질문 자체만 기반으로 처리된 것으로 간주합니다."
        )

    return {
        "prompt": "mock_prompt",
        "context": rag_info.get("combined_context", ""),
        "response": response_text,
        "score": 0,
        "reasoning": (
            "실제 대회 서버가 종료되어 API 기반 정량 검증은 수행할 수 없으므로 "
            "mock 모드로 파이프라인 실행과 구조를 점검했습니다."
        )
    }
