import pandas as pd


def save_results(results: list[dict], output_path) -> None:
    results_df = pd.DataFrame(results)
    results_df.to_excel(output_path, index=False)
    print(f"\n결과 저장 완료: {output_path}")
