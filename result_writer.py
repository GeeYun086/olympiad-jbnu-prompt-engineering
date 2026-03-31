import pandas as pd

from logger import setup_logger

logger = setup_logger()


def save_results(results: list[dict], output_path) -> None:
    results_df = pd.DataFrame(results)
    results_df.to_excel(output_path, index=False)
    logger.info(f"결과 저장 완료 | output={output_path}")
