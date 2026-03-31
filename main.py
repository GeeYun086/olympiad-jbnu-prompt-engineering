from data_loader import load_data
from client import create_client, solve_question
from result_writer import save_results


def main():
    file_path = "./problem.xlsx"
    base_url = "https://ryeon.elpai.org/submit/v1"
    output_path = "response_results.xlsx"

    data = load_data(file_path)
    client = create_client(base_url=base_url)

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

    save_results(results, output_path)


if __name__ == "__main__":
    main()
