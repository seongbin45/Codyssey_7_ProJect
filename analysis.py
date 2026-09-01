import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import rcParams

# 한글 폰트 설정 (Windows 기준)
rcParams['font.family'] = 'Malgun Gothic'
rcParams['axes.unicode_minus'] = False

def load_data(file_path: str) -> pd.DataFrame:
    """데이터 로드 및 날짜 인덱싱"""
    df = pd.read_csv(file_path, parse_dates=['date'])
    df.set_index('date', inplace=True)
    return df

def generate_price_trend_chart(df: pd.DataFrame, save_dir: str):
    """1. 주가 추이 및 이동평균선 시각화"""
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_60'] = df['close'].rolling(window=60).mean()
    df['SMA_120'] = df['close'].rolling(window=120).mean()

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['close'], label='Close Price', color='black', alpha=0.6)
    plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='blue', alpha=0.8)
    plt.plot(df.index, df['SMA_60'], label='60-Day SMA', color='orange', alpha=0.8)
    plt.plot(df.index, df['SMA_120'], label='120-Day SMA', color='red', alpha=0.8)
    
    plt.title('Samsung Electronics (005930.KS) Price Trend & Moving Averages (2023-2024)')
    plt.xlabel('Date')
    plt.ylabel('Price (KRW)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    save_path = os.path.join(save_dir, '01_price_trend.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

def generate_monthly_return_chart(df: pd.DataFrame, save_dir: str):
    """2. 월별 수익률 분석"""
    # 월별 마지막 거래일 기준 종가 추출
    monthly_close = df['close'].resample('ME').last()
    # 월간 수익률 계산
    monthly_return = monthly_close.pct_change() * 100
    
    # 2023년 데이터가 잘리므로 첫 달(2023-01)은 시작가 기준으로 보정
    if pd.isna(monthly_return.iloc[0]):
        first_open = df['open'].iloc[0]
        monthly_return.iloc[0] = ((monthly_close.iloc[0] - first_open) / first_open) * 100

    plt.figure(figsize=(12, 6))
    bars = plt.bar(monthly_return.index.strftime('%Y-%m'), monthly_return, 
                   color=['red' if x > 0 else 'blue' for x in monthly_return])
    
    plt.title('Monthly Returns (%)')
    plt.xlabel('Month')
    plt.ylabel('Return (%)')
    plt.xticks(rotation=45)
    plt.axhline(0, color='black', linewidth=1)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    save_path = os.path.join(save_dir, '02_monthly_return.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

def generate_volatility_volume_chart(df: pd.DataFrame, save_dir: str):
    """3. 변동성(20일 롤링 표준편차) 및 거래량 시각화"""
    df['volatility_20'] = df['close'].rolling(window=20).std()
    
    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    # 변동성 라인차트
    ax1.plot(df.index, df['volatility_20'], color='purple', label='20-Day Volatility (Std Dev)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Volatility', color='purple')
    ax1.tick_params(axis='y', labelcolor='purple')
    
    # 거래량 바차트 (우측 축)
    ax2 = ax1.twinx()
    ax2.bar(df.index, df['volume'], color='gray', alpha=0.3, label='Volume')
    ax2.set_ylabel('Volume', color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    
    plt.title('20-Day Rolling Volatility and Trading Volume')
    fig.tight_layout()
    
    save_path = os.path.join(save_dir, '03_volatility_volume.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

def generate_seasonal_decompose(df: pd.DataFrame, save_dir: str):
    """4. [보너스] 시계열 분해 (Seasonal Decomposition)"""
    # 영업일 기준이므로 주기(period)를 20(약 한 달 영업일)으로 설정
    # 결측치가 있으면 분해가 안 되므로 ffill 사용
    close_ffill = df['close'].asfreq('B').ffill()
    
    result = seasonal_decompose(close_ffill, model='multiplicative', period=20)
    
    fig = result.plot()
    fig.set_size_inches(12, 10)
    fig.suptitle('Seasonal Decomposition of Close Price (Period=20)', y=1.02)
    
    save_path = os.path.join(save_dir, '04_seasonal_decompose.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

def generate_forecast(df: pd.DataFrame, save_dir: str):
    """5. [보너스] 간단한 베이스라인 예측 (마지막 60일 비교)"""
    # 마지막 60일을 Test로 분리
    test_size = 60
    train = df.iloc[:-test_size]
    test = df.iloc[-test_size:]
    
    # 베이스라인 모델: 직전 20일 이동평균을 미래 예측값으로 사용 (Naive 접근)
    last_sma20 = train['close'].rolling(20).mean().iloc[-1]
    
    plt.figure(figsize=(14, 7))
    plt.plot(train.index[-120:], train['close'][-120:], label='Train (Last 120 days)', color='black')
    plt.plot(test.index, test['close'], label='Test (Actual)', color='blue')
    plt.plot(test.index, [last_sma20]*len(test), label='Baseline Forecast (Last SMA-20)', color='red', linestyle='--')
    
    plt.title('Baseline Forecast vs Actual (Last 60 Days)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    save_path = os.path.join(save_dir, '05_forecast.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

if __name__ == "__main__":
    DATA_PATH = "data/samsung_2023_2024.csv"
    SAVE_DIR = "images"
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    print("[INFO] 분석 및 시각화를 시작합니다.")
    df = load_data(DATA_PATH)
    
    generate_price_trend_chart(df.copy(), SAVE_DIR)
    generate_monthly_return_chart(df.copy(), SAVE_DIR)
    generate_volatility_volume_chart(df.copy(), SAVE_DIR)
    generate_seasonal_decompose(df.copy(), SAVE_DIR)
    generate_forecast(df.copy(), SAVE_DIR)
    
    print("[INFO] 분석 완료.")
