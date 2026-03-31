from openai import OpenAI

from config import API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS, STREAM
from prompt_builder import build_messages, build_debug_context


def create_client(base_url: str) -> OpenAI:
    client = OpenAI(
        base_url=base_url,
        api_key=API_KEY,
        default_headers={
            "Content-Type": "application/json"
        }
    )
    return client


def solve_question(client: OpenAI, question_id, question: str) -> dict:
    messages, rag_info = build_messages(question_id=question_id, question=question)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=STREAM,
            extra_headers={
                "Question-ID": str(question_id)
            }
        )

        response_dict = response.model_dump()
        result = response_dict.get("result", {})

        print(f"\nID {question_id} 처리 완료")
        print(f"선택된 RAG 토픽: {', '.join(rag_info['selected_topics']) if rag_info['selected_topics'] else '없음'}")
        print(f"응답: {result.get('response', '')}")

        return {
            "id": question_id,
            "question": question,
            "selected_topics": ", ".join(rag_info["selected_topics"]),
            "rag_block_count": rag_info["block_count"],
            "prompt": result.get("prompt", ""),
            "context": result.get("context", ""),
            "response": result.get("response", ""),
            "score": result.get("score", 0),
            "reasoning": result.get("reasoning", "")
        }

    except Exception as e:
        print(f"ID {question_id} 처리 중 에러 발생: {str(e)}")

        return {
            "id": question_id,
            "question": question,
            "selected_topics": ", ".join(rag_info["selected_topics"]),
            "rag_block_count": rag_info["block_count"],
            "prompt": "",
            "context": build_debug_context(rag_info),
            "response": "",
            "score": 0,
            "reasoning": f"ERROR: {str(e)}"
        }
