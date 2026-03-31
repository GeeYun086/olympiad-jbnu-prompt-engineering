from openai import OpenAI

from config import API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS, STREAM, USE_MOCK
from prompt_builder import build_messages, build_debug_context
from mock_response import generate_mock_response
from logger import setup_logger

logger = setup_logger()


def create_client(base_url: str):
    if USE_MOCK:
        logger.info("mock 모드 활성화: 실제 API 클라이언트를 생성하지 않습니다.")
        return None

    client = OpenAI(
        base_url=base_url,
        api_key=API_KEY,
        default_headers={
            "Content-Type": "application/json"
        }
    )
    logger.info("API 클라이언트 생성 완료")
    return client


def solve_question(client, question_id, question: str) -> dict:
    messages, rag_info = build_messages(question_id=question_id, question=question)

    logger.info(
        f"질문 처리 시작 | id={question_id} | selected_topics={rag_info['selected_topics']} | "
        f"block_count={rag_info['block_count']}"
    )

    if USE_MOCK:
        mock_result = generate_mock_response(question, rag_info)

        logger.info(f"mock 응답 생성 완료 | id={question_id}")

        return {
            "id": question_id,
            "question": question,
            "run_mode": "mock",
            "selected_topics": ", ".join(rag_info["selected_topics"]),
            "rag_block_count": rag_info["block_count"],
            "rag_match_scores": str(rag_info.get("match_scores", {})),
            "prompt": mock_result.get("prompt", ""),
            "context": mock_result.get("context", ""),
            "response": mock_result.get("response", ""),
            "score": mock_result.get("score", 0),
            "reasoning": mock_result.get("reasoning", ""),
            "error": ""
        }

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

        logger.info(f"API 응답 수신 완료 | id={question_id}")

        return {
            "id": question_id,
            "question": question,
            "run_mode": "api",
            "selected_topics": ", ".join(rag_info["selected_topics"]),
            "rag_block_count": rag_info["block_count"],
            "rag_match_scores": str(rag_info.get("match_scores", {})),
            "prompt": result.get("prompt", ""),
            "context": result.get("context", ""),
            "response": result.get("response", ""),
            "score": result.get("score", 0),
            "reasoning": result.get("reasoning", ""),
            "error": ""
        }

    except Exception as e:
        logger.exception(f"질문 처리 중 에러 발생 | id={question_id}")

        return {
            "id": question_id,
            "question": question,
            "run_mode": "api",
            "selected_topics": ", ".join(rag_info["selected_topics"]),
            "rag_block_count": rag_info["block_count"],
            "rag_match_scores": str(rag_info.get("match_scores", {})),
            "prompt": "",
            "context": build_debug_context(rag_info),
            "response": "",
            "score": 0,
            "reasoning": "",
            "error": str(e)
        }
