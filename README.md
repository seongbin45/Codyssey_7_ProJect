# 삼성전자 시계열 주가 분석 프로젝트 (2023-2024)

본 프로젝트는 AI 응용 학습 미션의 일환으로, 삼성전자(005930.KS)의 2023~2024년 주가 데이터를 수집, 정제, 분석하여 인사이트를 도출하는 과정을 담고 있습니다. 필수 과제 외에도 **시계열 분해, 단기 예측 모델, 일간/주간 집계 비교, ACF 통계 검증, 대화형 웹 대시보드(Dash)** 등의 보너스 과제가 포함되어 있습니다.

## 📁 폴더 및 파일 구조

```
Codyssey_7_ProJect/
├── data/
│   └── samsung_2023_2024.csv         # 수집된 원본 주가 데이터
├── images/
│   ├── 01_price_trend.png            # 종가 및 이동평균선 시각화
│   ├── 02_monthly_return.png         # 월별 수익률 막대 차트
│   ├── 03_volatility_volume.png      # 변동성(일별 수익률 기준) 및 거래량 시각화
│   ├── 04_seasonal_decompose.png     # 시계열 분해 차트 (보너스)
│   ├── 05_forecast.png               # 단기 베이스라인 예측 차트 (보너스)
│   ├── 06_weekly_comparison.png      # 일간/주간 집계 비교 차트 (보너스)
│   └── 07_acf_plot.png               # ACF(자기상관함수) 플롯 (보너스)
├── log/                               # 이 저장소를 검증한 작업 기록 (아래 "관련 문서" 참고)
│   ├── verification-log.md
│   └── full-command-log.md
├── collect_data.py                   # 데이터 수집 스크립트 (yfinance)
├── analysis.py                       # 핵심 데이터 분석 및 시각화 생성 스크립트
├── analysis.ipynb                    # analysis.py와 동일한 분석을 셀 단위로 대화형으로 실행하는 노트북
├── create_nb.py                      # analysis.ipynb를 코드로부터 재생성하는 스크립트 (analysis.py와 동기화 유지)
├── dashboard.py                      # Dash 기반 인터랙티브 웹 대시보드 스크립트 (보너스)
├── verify_results.py                 # data/·images/·analysis.ipynb 산출물이 모두 있는지 자동으로 확인하는 스크립트
├── test_env.py                       # (개발용) 로컬 환경의 파이썬/패키지 버전과 yfinance 연결 상태를 점검하는 스크립트
├── REPORT.md                         # 최종 분석 결과 및 인사이트 리포트
├── Jargon_Buster_for_Beginners.md    # 통계·코드 용어를 처음 접하는 분들을 위한 초심자용 치트 시트
├── requirements.txt                  # Python 패키지 의존성 목록
├── README.md                         # 현재 파일 (실행 가이드)
└── 과제_조건.html                     # 원본 과제 안내 페이지 (미션 "AI 응용 학습" 스냅샷, 참고용)
```

---

## 🛠️ 개발 환경 및 필수 라이브러리

- **언어**: Python 3.10 이상
- **주요 라이브러리**:
  - 데이터 분석: `pandas`, `numpy`, `statsmodels`
  - 데이터 수집: `yfinance`
  - 시각화: `matplotlib`, `seaborn`
  - 대시보드: `dash`, `plotly`
  - (선택) 노트북 실행: `jupyter`, `nbconvert`

## 🚀 실행 가이드

모든 스크립트는 가상환경 내부에서 순서대로 실행하는 것을 권장합니다. 아래는 Windows(PowerShell) 기준이며, macOS/Linux는 각 단계 아래에 별도로 표기했습니다.

### 1. 가상환경 세팅 및 패키지 설치
```powershell
# 가상환경 생성 (Windows 기준)
py -m venv venv

# 가상환경 활성화
.\venv\Scripts\activate

# 의존성 패키지 설치
pip install -r requirements.txt
```
> **macOS / Linux**
> ```bash
> python3 -m venv venv
> source venv/bin/activate
> python3 -m pip install -r requirements.txt
> ```
> `pip`만 단독으로 실행하면 macOS 환경에 따라 PATH가 꼬여 엉뚱한 파이썬을 참조하거나 명령을 못 찾는 경우가 있습니다. `python3 -m pip`는 방금 활성화한 `venv`의 `python3`에 확실히 묶인 pip를 쓰므로 더 안전합니다.

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
- 수집된 CSV 데이터를 바탕으로 이동평균, 수익률, 변동성(일별 수익률 기준 표준편차)을 계산합니다.
- 보너스 과제인 시계열 분해(Seasonal Decomposition), 예측(Baseline Forecast), 일간/주간 집계 비교, ACF 분석도 함께 수행됩니다.
- 결과물은 `images/` 폴더에 `.png` 파일 7개로 저장됩니다.
- 같은 내용을 셀 단위로 하나씩 실행하며 살펴보고 싶다면 `jupyter notebook analysis.ipynb`를 대신 사용할 수 있습니다. (노트북 자체를 코드로 다시 만들고 싶다면 `python create_nb.py`)

### 4. (선택) 산출물 자동 검증
```powershell
python verify_results.py
```
- `data/samsung_2023_2024.csv`, `images/*.png` 7개, `analysis.ipynb`가 모두 정상적으로 존재하는지 확인합니다.
- 하나라도 빠지면 어떤 파일이 없는지 출력하고 종료 코드 1로 끝납니다(전부 있으면 0).

### 5. 웹 대시보드 실행 (보너스 과제)
```powershell
python dashboard.py
```
- 스크립트를 실행한 후 브라우저에서 `http://127.0.0.1:8050/` 에 접속합니다.
- 기간을 변경하거나 이동평균선 일수를 조정하면서 인터랙티브하게 주가 추이를 탐색할 수 있습니다.

---

## 📄 분석 결과 및 관련 문서

- **[REPORT.md](REPORT.md)** — 생성된 모든 분석 결과와 이로부터 도출한 **3가지 주요 인사이트**를 상세히 확인할 수 있습니다.
- **[Jargon_Buster_for_Beginners.md](Jargon_Buster_for_Beginners.md)** — 이 프로젝트에 나오는 통계·코드 용어(이동평균, 표준편차, 시계열 분해 등)가 낯설다면 여기서 쉬운 설명을 먼저 참고하세요.
- **[log/verification-log.md](log/verification-log.md)** — 이 저장소의 문서·코드를 실제 데이터와 실행 결과로 교차검증한 이력입니다. 어떤 부분이 왜 수정됐는지 궁금하다면 참고하세요.
