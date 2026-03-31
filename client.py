from openai import OpenAI
from prompt_builder import build_messages


def create_client(base_url: str) -> OpenAI:
    """
    OpenAI 클라이언트를 생성, 기존 코드의 base_url, api_key, Content-Type 설정 유지
    """
    client = OpenAI(
        base_url=base_url,
        api_key="dummy-key",
        default_headers={
            "Content-Type": "application/json"
        }
    )
    return client


def solve_question(client: OpenAI, question_id, question: str) -> dict:
    """
    단일 질문 처리 함수, 기존 process_with_openai 내부 로직을 한 문제 단위로 분리
    """
    messages = build_messages(question_id=question_id, question=question)

    try:
        response = client.chat.completions.create(
            model="olympiad",
            messages=messages,
            temperature=0.7,
            max_tokens=None,
            stream=False,
            extra_headers={
                "Question-ID": str(question_id)
            }
        )

        response_dict = response.model_dump()
        result = response_dict.get("result", {})

        print(f"\nID {question_id} 처리 완료")
        print(f"응답: {result.get('response', '')}")

        return {
            "id": question_id,
            "question": question,
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
            "prompt": "",
            "context": "",
            "response": "",
            "score": 0,
            "reasoning": f"ERROR: {str(e)}"
        }
