import pandas as pd


def load_data(file_path) -> pd.DataFrame:
    data = pd.read_excel(file_path)
    print("데이터 로드 완료!")
    print(data.head())
    return data
