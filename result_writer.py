import pandas as pd


def save_results(results: list[dict], output_path: str) -> None:
    """
    결과를 DataFrame으로 변환 후 엑셀 저장
    """
    results_df = pd.DataFrame(results)
    results_df.to_excel(output_path, index=False)
    print(f"\n결과 저장 완료: {output_path}")
