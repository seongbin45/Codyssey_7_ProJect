import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf
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
    monthly_close = df['close'].resample('ME').last()
    monthly_return = monthly_close.pct_change() * 100
    
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
    """3. 변동성 민감도 분석 (10일, 20일, 40일 롤링 표준편차, 일별 수익률 기준) 및 거래량"""
    daily_return = df['close'].pct_change() * 100
    df['volatility_10'] = daily_return.rolling(window=10).std()
    df['volatility_20'] = daily_return.rolling(window=20).std()
    df['volatility_40'] = daily_return.rolling(window=40).std()

    fig, ax1 = plt.subplots(figsize=(14, 7))
    
    # 변동성 라인차트 (다중 윈도우)
    ax1.plot(df.index, df['volatility_10'], color='cyan', label='10-Day Volatility', alpha=0.6)
    ax1.plot(df.index, df['volatility_20'], color='purple', label='20-Day Volatility', linewidth=2)
    ax1.plot(df.index, df['volatility_40'], color='magenta', label='40-Day Volatility', alpha=0.6)
    
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Volatility (Std Dev of Daily Return, %)', color='purple')
    ax1.tick_params(axis='y', labelcolor='purple')
    ax1.legend(loc='upper left')

    # 거래량 바차트 (우측 축)
    ax2 = ax1.twinx()
    ax2.bar(df.index, df['volume'], color='gray', alpha=0.3, label='Volume')
    ax2.set_ylabel('Volume', color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    ax2.legend(loc='upper right')

    plt.title('Volatility Sensitivity Analysis (10, 20, 40 days, Daily Return %) and Trading Volume')
    fig.tight_layout()
    
    save_path = os.path.join(save_dir, '03_volatility_volume.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

def generate_seasonal_decompose(df: pd.DataFrame, save_dir: str):
    """4. 시계열 분해 (Seasonal Decomposition)"""
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
    """5. 간단한 베이스라인 예측 (마지막 60일 비교)"""
    test_size = 60
    train = df.iloc[:-test_size]
    test = df.iloc[-test_size:]
    
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

def generate_weekly_comparison_chart(df: pd.DataFrame, save_dir: str):
    """6. 집계단위 비교 (일간 vs 주간 종가 흐름)"""
    weekly_close = df['close'].resample('W').last()
    
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['close'], label='Daily Close (Noise)', color='lightgray', alpha=0.7)
    plt.plot(weekly_close.index, weekly_close, label='Weekly Close (Trend)', color='blue', linewidth=2, marker='o', markersize=4)
    
    plt.title('Data Aggregation Comparison: Daily vs Weekly Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price (KRW)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    save_path = os.path.join(save_dir, '06_weekly_comparison.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved: {save_path}")

def generate_acf_pacf_chart(df: pd.DataFrame, save_dir: str):
    """7. ACF 플롯을 통한 트렌드 및 주기성 검증"""
    plt.figure(figsize=(14, 6))
    ax = plt.subplot(111)
    # 결측치 없는 시계열 생성 (B freq)
    close_b = df['close'].asfreq('B').ffill()
    # Lags = 40 (두 달 정도의 영업일)
    plot_acf(close_b, lags=40, ax=ax, title='Autocorrelation Function (ACF) of Close Price')
    
    plt.xlabel('Lags (Business Days)')
    plt.ylabel('Autocorrelation')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    save_path = os.path.join(save_dir, '07_acf_plot.png')
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
    generate_weekly_comparison_chart(df.copy(), SAVE_DIR)
    generate_acf_pacf_chart(df.copy(), SAVE_DIR)
    
    print("[INFO] 전체 분석 시각화 완료.")
