import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 데이터 로드
try:
    df = pd.read_csv('data/samsung_2023_2024.csv', parse_dates=['date'])
    df.set_index('date', inplace=True)
except FileNotFoundError:
    # 데이터 수집 전이라면 임시로 빈 데이터프레임 생성
    df = pd.DataFrame(columns=['close', 'high', 'low', 'open', 'volume'])

app = dash.Dash(__name__, title="삼성전자 주가 분석 대시보드")

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("삼성전자(005930.KS) 주가 분석 대시보드", style={'textAlign': 'center'}),
    
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '20px'}, children=[
        html.Div([
            html.Label("날짜 범위 선택: "),
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=df.index.min() if not df.empty else '2023-01-01',
                max_date_allowed=df.index.max() if not df.empty else '2024-12-31',
                start_date=df.index.min() if not df.empty else '2023-01-01',
                end_date=df.index.max() if not df.empty else '2024-12-31',
                display_format='YYYY-MM-DD'
            )
        ]),
        html.Div([
            html.Label("이동평균(SMA) 기간: "),
            dcc.Slider(
                id='sma-slider',
                min=5,
                max=120,
                step=5,
                value=20,
                marks={i: str(i) for i in [5, 20, 60, 120]},
            )
        ], style={'width': '300px'})
    ]),
    
    dcc.Graph(id='main-chart')
])

@app.callback(
    Output('main-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('sma-slider', 'value')]
)
def update_chart(start_date, end_date, sma_window):
    if df.empty:
        return go.Figure()
        
    # SMA는 날짜로 자르기 전, 전체 이력 기준으로 계산한다.
    # (필터링 후 계산하면 구간 시작부에서 실제 N일치 데이터가 없어 왜곡된 값이 나온다)
    sma_full = df['close'].rolling(window=sma_window).mean()

    filtered_df = df.loc[start_date:end_date].copy()
    if filtered_df.empty:
        return go.Figure()

    filtered_df['SMA'] = sma_full.loc[filtered_df.index]

    # 서브플롯 생성: 캔들차트 & 거래량
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])

    # 캔들차트 (국내 관행: 상승=빨강, 하락=파랑 — 아래 거래량 바 색상과 통일)
    fig.add_trace(go.Candlestick(
        x=filtered_df.index,
        open=filtered_df['open'], high=filtered_df['high'],
        low=filtered_df['low'], close=filtered_df['close'],
        increasing_line_color='red', increasing_fillcolor='red',
        decreasing_line_color='blue', decreasing_fillcolor='blue',
        name='Price'
    ), row=1, col=1)
    
    # 이동평균선
    fig.add_trace(go.Scatter(
        x=filtered_df.index, y=filtered_df['SMA'],
        line=dict(color='orange', width=2),
        name=f'{sma_window}-Day SMA'
    ), row=1, col=1)
    
    # 거래량
    colors = ['red' if row['close'] >= row['open'] else 'blue' for index, row in filtered_df.iterrows()]
    fig.add_trace(go.Bar(
        x=filtered_df.index, y=filtered_df['volume'],
        marker_color=colors,
        name='Volume'
    ), row=2, col=1)
    
    fig.update_layout(
        height=700,
        title_text=f"삼성전자 주가 및 거래량 (SMA {sma_window}일)",
        xaxis_rangeslider_visible=False,
        template='plotly_white'
    )
    
    return fig

if __name__ == '__main__':
    print("[INFO] 대시보드 서버를 시작합니다. http://127.0.0.1:8050 에 접속하세요.")
    app.run(debug=True, port=8050)
