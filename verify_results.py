import os
import pandas as pd

def verify():
    errors = []
    
    # 1. Check if data file exists and has > 100 rows
    data_path = 'data/samsung_2023_2024.csv'
    if not os.path.exists(data_path):
        errors.append(f"Missing data file: {data_path}")
    else:
        df = pd.read_csv(data_path)
        if len(df) < 100:
            errors.append(f"Data points < 100: {len(df)}")
        else:
            print(f"[PASS] Data row count = {len(df)} (>= 100)")
            
    # 2. Check if all images exist
    required_images = [
        '01_price_trend.png',
        '02_monthly_return.png',
        '03_volatility_volume.png',
        '04_seasonal_decompose.png',
        '05_forecast.png',
        '06_weekly_comparison.png',
        '07_acf_plot.png'
    ]
    for img in required_images:
        path = os.path.join('images', img)
        if not os.path.exists(path):
            errors.append(f"Missing image: {path}")
        else:
            print(f"[PASS] Image found: {path}")
            
    # 3. Check if Notebook exists
    nb_path = 'analysis.ipynb'
    if not os.path.exists(nb_path):
        errors.append(f"Missing notebook: {nb_path}")
    else:
        print(f"[PASS] Notebook found: {nb_path}")

    # Final result
    if errors:
        print("\n[FAIL] Some verification checks failed:")
        for err in errors:
            print(f" - {err}")
    else:
        print("\n[SUCCESS] All automated verifications passed successfully!")

if __name__ == "__main__":
    verify()
