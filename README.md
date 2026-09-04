# 삼성전자 시계열 주가 분석 프로젝트 (2023-2024)

본 프로젝트는 AI 응용 학습 미션의 일환으로, 삼성전자(005930.KS)의 2023~2024년 주가 데이터를 수집, 정제, 분석하여 인사이트를 도출하는 과정을 담고 있습니다. 필수 과제 외에도 **시계열 분해, 단기 예측 모델, 대화형 웹 대시보드(Dash)** 등의 보너스 과제가 포함되어 있습니다.

## 📁 폴더 및 파일 구조

```
Codyssey_7_ProJect/
├── data/
│   └── samsung_2023_2024.csv         # 수집된 원본 주가 데이터
├── images/
│   ├── 01_price_trend.png            # 종가 및 이동평균선 시각화
│   ├── 02_monthly_return.png         # 월별 수익률 막대 차트
│   ├── 03_volatility_volume.png      # 변동성 및 거래량 시각화
│   ├── 04_seasonal_decompose.png     # 시계열 분해 차트 (보너스)
│   ├── 05_forecast.png               # 단기 베이스라인 예측 차트 (보너스)
│   ├── 06_weekly_comparison.png      # 일간/주간 집계 비교 차트 (보너스)
│   └── 07_acf_plot.png               # ACF(자기상관함수) 플롯 (보너스)
├── collect_data.py                   # 데이터 수집 스크립트 (yfinance)
├── analysis.py                       # 핵심 데이터 분석 및 시각화 생성 스크립트
├── dashboard.py                      # Dash 기반 인터랙티브 웹 대시보드 스크립트 (보너스)
├── REPORT.md                         # 최종 분석 결과 및 인사이트 리포트
├── requirements.txt                  # Python 패키지 의존성 목록
└── README.md                         # 현재 파일 (실행 가이드)
```

---

## 🛠️ 개발 환경 및 필수 라이브러리

- **언어**: Python 3.10 이상
- **주요 라이브러리**: 
  - 데이터 분석: `pandas`, `numpy`, `statsmodels`
  - 데이터 수집: `yfinance`
  - 시각화: `matplotlib`, `seaborn`
  - 대시보드: `dash`, `plotly`

## 🚀 실행 가이드

모든 스크립트는 가상환경 내부에서 순서대로 실행하는 것을 권장합니다.

### 1. 가상환경 세팅 및 패키지 설치
```powershell
# 가상환경 생성 (Windows 기준)
py -m venv venv

# 가상환경 활성화
.\venv\Scripts\activate

# 의존성 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터 수집
```powershell
python collect_data.py
```
- Yahoo Finance API를 통해 삼성전자(005930.KS)의 2023-01-01 ~ 2024-12-31 데이터를 수집합니다.
- `data/` 폴더에 `samsung_2023_2024.csv` 파일이 생성됩니다.

### 3. 데이터 분석 및 시각화 이미지 생성
```powershell
python analysis.py
```
- 수집된 CSV 데이터를 바탕으로 이동평균, 수익률, 변동성을 계산합니다.
- 보너스 과제인 시계열 분해(Seasonal Decomposition), 예측(Baseline Forecast), 일간/주간 집계 비교, ACF 분석도 함께 수행됩니다.
- 결과물은 `images/` 폴더에 `.png` 파일 7개로 저장됩니다.

### 4. 웹 대시보드 실행 (보너스 과제)
```powershell
python dashboard.py
```
- 스크립트를 실행한 후 브라우저에서 `http://127.0.0.1:8050/` 에 접속합니다.
- 기간을 변경하거나 이동평균선 일수를 조정하면서 인터랙티브하게 주가 추이를 탐색할 수 있습니다.

---

## 📄 분석 결과 확인
생성된 모든 분석 결과와 이로부터 도출한 **3가지 주요 인사이트**는 [REPORT.md](REPORT.md) 파일에서 상세히 확인할 수 있습니다.
