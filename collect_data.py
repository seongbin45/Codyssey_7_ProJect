# collect_data.py
# 삼성전자(005930.KS) 주가 데이터 수집 스크립트
# 출처: Yahoo Finance (yfinance 라이브러리)
# 기간: 2023-01-01 ~ 2024-12-31

import os
import yfinance as yf
import pandas as pd


def collect_samsung_stock(ticker: str, start: str, end: str, save_path: str) -> pd.DataFrame:
    """
    Yahoo Finance에서 삼성전자 주가 OHLCV 데이터를 수집하여 CSV로 저장한다.

    Args:
        ticker: Yahoo Finance 티커 심볼 (예: '005930.KS')
        start: 수집 시작일 (YYYY-MM-DD)
        end: 수집 종료일 (YYYY-MM-DD)
        save_path: CSV 저장 경로

    Returns:
        수집된 DataFrame
    """
    print(f"[INFO] {ticker} 데이터 수집 중... ({start} ~ {end})")
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

    if df.empty:
        raise ValueError(f"데이터를 가져오지 못했습니다. 티커: {ticker}")

    # MultiIndex 컬럼인 경우 단일 레벨로 변환
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 인덱스를 날짜 컬럼으로 변환
    df = df.reset_index()
    df.rename(columns={"Date": "date", "Open": "open", "High": "high",
                        "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # 저장 디렉터리 생성
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"[INFO] 저장 완료: {save_path}")

    return df


def print_data_summary(df: pd.DataFrame) -> None:
    """수집된 데이터의 기본 정보를 출력한다."""
    print("\n" + "=" * 50)
    print("  데이터 기본 정보")
    print("=" * 50)
    print(f"  기간          : {df['date'].min()} ~ {df['date'].max()}")
    print(f"  데이터 포인트  : {len(df)}개 (거래일 기준)")
    print(f"  컬럼          : {list(df.columns)}")
    print(f"  결측치 여부   :")
    for col in df.columns:
        null_count = df[col].isnull().sum()
        print(f"    - {col}: {null_count}개")
    print(f"\n  종가(close) 통계:")
    print(df["close"].describe().to_string())
    print("=" * 50 + "\n")


if __name__ == "__main__":
    TICKER = "005930.KS"
    START_DATE = "2023-01-01"
    END_DATE = "2024-12-31"
    SAVE_PATH = "data/samsung_2023_2024.csv"

    df = collect_samsung_stock(TICKER, START_DATE, END_DATE, SAVE_PATH)
    print_data_summary(df)
