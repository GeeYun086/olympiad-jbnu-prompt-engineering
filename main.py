from data_loader import load_data
from client import create_client, solve_question
from result_writer import save_results
from config import INPUT_FILE, OUTPUT_FILE, BASE_URL, USE_MOCK
from logger import setup_logger

logger = setup_logger()


def main():
    logger.info("프로그램 시작")
    logger.info(f"실행 모드: {'mock' if USE_MOCK else 'api'}")

    data = load_data(INPUT_FILE)
    logger.info(f"입력 데이터 로드 완료 | rows={len(data)}")

    client = create_client(base_url=BASE_URL)

    results = []

    for _, row in data.iterrows():
        question_id = row["id"]
        question = row["question"]

        result = solve_question(
            client=client,
            question_id=question_id,
            question=question
        )
        results.append(result)

    save_results(results, OUTPUT_FILE)
    logger.info("프로그램 종료")


if __name__ == "__main__":
    main()
