import sys

with open('test_result.txt', 'w', encoding='utf-8') as f:
    f.write("=== Python test ===\n")
    f.write(f"Python version: {sys.version}\n")
    
    yf = None
    try:
        import yfinance as yf
        f.write(f"yfinance version: {yf.__version__}\n")
    except Exception as e:
        f.write(f"yfinance import error: {e}\n")

    try:
        import pandas as pd
        f.write(f"pandas version: {pd.__version__}\n")
    except Exception as e:
        f.write(f"pandas error: {e}\n")

    if yf is None:
        f.write("download skipped: yfinance import failed above\n")
    else:
        try:
            df = yf.download('005930.KS', start='2023-01-01', end='2024-12-31',
                             progress=False, auto_adjust=True)
            f.write(f"download rows: {len(df)}\n")
            f.write(f"columns: {list(df.columns)}\n")
            f.write(str(df.head()) + "\n")
        except Exception as e:
            f.write(f"download error: {e}\n")
