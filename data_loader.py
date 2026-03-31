import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """엑셀 파일을 읽어 DataFrame으로 반환"""
    data = pd.read_excel(file_path)
    print("데이터 로드 완료!")
    print(data.head())
    return data
