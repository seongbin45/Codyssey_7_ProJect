import json
import os

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 삼성전자 주가 트렌드 분석 (2023-2024)\n",
    "\n",
    "이 노트북은 `analysis.py`에 구현된 데이터 정제 및 시각화 과정을 대화형으로 탐색하기 위해 작성되었습니다.\n",
    "데이터 수집(`collect_data.py`)을 통해 확보한 `data/samsung_2023_2024.csv` 파일을 사용합니다."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from statsmodels.tsa.seasonal import seasonal_decompose\n",
    "from statsmodels.graphics.tsaplots import plot_acf\n",
    "from matplotlib import rcParams\n",
    "\n",
    "# 한글 폰트 설정 (Windows 기준)\n",
    "rcParams['font.family'] = 'Malgun Gothic'\n",
    "rcParams['axes.unicode_minus'] = False\n",
    "\n",
    "# 데이터 로드\n",
    "df = pd.read_csv('data/samsung_2023_2024.csv', parse_dates=['date'])\n",
    "df.set_index('date', inplace=True)\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. 주가 추이 및 이동평균선 시각화"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['SMA_20'] = df['close'].rolling(window=20).mean()\n",
    "df['SMA_60'] = df['close'].rolling(window=60).mean()\n",
    "df['SMA_120'] = df['close'].rolling(window=120).mean()\n",
    "\n",
    "plt.figure(figsize=(14, 7))\n",
    "plt.plot(df.index, df['close'], label='Close Price', color='black', alpha=0.6)\n",
    "plt.plot(df.index, df['SMA_20'], label='20-Day SMA', color='blue', alpha=0.8)\n",
    "plt.plot(df.index, df['SMA_60'], label='60-Day SMA', color='orange', alpha=0.8)\n",
    "plt.plot(df.index, df['SMA_120'], label='120-Day SMA', color='red', alpha=0.8)\n",
    "\n",
    "plt.title('Samsung Electronics (005930.KS) Price Trend & Moving Averages (2023-2024)')\n",
    "plt.xlabel('Date')\n",
    "plt.ylabel('Price (KRW)')\n",
    "plt.legend()\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. 월별 수익률 분석"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "monthly_close = df['close'].resample('ME').last()\n",
    "monthly_return = monthly_close.pct_change() * 100\n",
    "\n",
    "if pd.isna(monthly_return.iloc[0]):\n",
    "    first_open = df['open'].iloc[0]\n",
    "    monthly_return.iloc[0] = ((monthly_close.iloc[0] - first_open) / first_open) * 100\n",
    "\n",
    "plt.figure(figsize=(12, 6))\n",
    "bars = plt.bar(monthly_return.index.strftime('%Y-%m'), monthly_return, \n",
    "               color=['red' if x > 0 else 'blue' for x in monthly_return])\n",
    "\n",
    "plt.title('Monthly Returns (%)')\n",
    "plt.xlabel('Month')\n",
    "plt.ylabel('Return (%)')\n",
    "plt.xticks(rotation=45)\n",
    "plt.axhline(0, color='black', linewidth=1)\n",
    "plt.grid(axis='y', linestyle='--', alpha=0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. 변동성 민감도 분석 (10/20/40일) 및 거래량"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "daily_return = df['close'].pct_change() * 100\n",
    "df['volatility_10'] = daily_return.rolling(window=10).std()\n",
    "df['volatility_20'] = daily_return.rolling(window=20).std()\n",
    "df['volatility_40'] = daily_return.rolling(window=40).std()\n",
    "\n",
    "fig, ax1 = plt.subplots(figsize=(14, 7))\n",
    "\n",
    "ax1.plot(df.index, df['volatility_10'], color='cyan', label='10-Day Volatility', alpha=0.6)\n",
    "ax1.plot(df.index, df['volatility_20'], color='purple', label='20-Day Volatility', linewidth=2)\n",
    "ax1.plot(df.index, df['volatility_40'], color='magenta', label='40-Day Volatility', alpha=0.6)\n",
    "\n",
    "ax1.set_xlabel('Date')\n",
    "ax1.set_ylabel('Volatility (Std Dev of Daily Return, %)', color='purple')\n",
    "ax1.tick_params(axis='y', labelcolor='purple')\n",
    "ax1.legend(loc='upper left')\n",
    "\n",
    "ax2 = ax1.twinx()\n",
    "ax2.bar(df.index, df['volume'], color='gray', alpha=0.3, label='Volume')\n",
    "ax2.set_ylabel('Volume', color='gray')\n",
    "ax2.tick_params(axis='y', labelcolor='gray')\n",
    "ax2.legend(loc='upper right')\n",
    "\n",
    "plt.title('Volatility Sensitivity Analysis (10, 20, 40 days, Daily Return %) and Trading Volume')\n",
    "fig.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. [보너스] 시계열 분해 (Seasonal Decomposition)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "close_ffill = df['close'].asfreq('B').ffill()\n",
    "result = seasonal_decompose(close_ffill, model='multiplicative', period=20)\n",
    "fig = result.plot()\n",
    "fig.set_size_inches(12, 10)\n",
    "fig.suptitle('Seasonal Decomposition of Close Price (Period=20)', y=1.02)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. [보너스] 단순 예측 (Baseline Forecast)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "test_size = 60\n",
    "train = df.iloc[:-test_size]\n",
    "test = df.iloc[-test_size:]\n",
    "last_sma20 = train['close'].rolling(20).mean().iloc[-1]\n",
    "\n",
    "plt.figure(figsize=(14, 7))\n",
    "plt.plot(train.index[-120:], train['close'][-120:], label='Train (Last 120 days)', color='black')\n",
    "plt.plot(test.index, test['close'], label='Test (Actual)', color='blue')\n",
    "plt.plot(test.index, [last_sma20]*len(test), label='Baseline Forecast (Last SMA-20)', color='red', linestyle='--')\n",
    "\n",
    "plt.title('Baseline Forecast vs Actual (Last 60 Days)')\n",
    "plt.xlabel('Date')\n",
    "plt.ylabel('Price')\n",
    "plt.legend()\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. [반례 분석] 일간 vs 주간 집계 흐름 비교"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "weekly_close = df['close'].resample('W').last()\n",
    "\n",
    "plt.figure(figsize=(14, 7))\n",
    "plt.plot(df.index, df['close'], label='Daily Close (Noise)', color='lightgray', alpha=0.7)\n",
    "plt.plot(weekly_close.index, weekly_close, label='Weekly Close (Trend)', color='blue', linewidth=2, marker='o', markersize=4)\n",
    "\n",
    "plt.title('Data Aggregation Comparison: Daily vs Weekly Close Price')\n",
    "plt.xlabel('Date')\n",
    "plt.ylabel('Price (KRW)')\n",
    "plt.legend()\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. 트렌드/계절성 통계적 검증 (ACF)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(14, 6))\n",
    "ax = plt.subplot(111)\n",
    "close_b = df['close'].asfreq('B').ffill()\n",
    "plot_acf(close_b, lags=40, ax=ax, title='Autocorrelation Function (ACF) of Close Price')\n",
    "plt.xlabel('Lags (Business Days)')\n",
    "plt.ylabel('Autocorrelation')\n",
    "plt.grid(True, linestyle='--', alpha=0.5)\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open("analysis.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("[INFO] analysis.ipynb 생성 완료.")
