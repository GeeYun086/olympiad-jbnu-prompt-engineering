from data_loader import load_data
from client import create_client, solve_question
from result_writer import save_results
from config import INPUT_FILE, OUTPUT_FILE, BASE_URL


def main():
    data = load_data(INPUT_FILE)
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


if __name__ == "__main__":
    main()
