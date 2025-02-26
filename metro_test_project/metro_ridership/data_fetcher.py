import requests
import pandas as pd
import logging
from utils.logging_config import setup_logging

setup_logging()

CSV_URL = "https://data.taipei/api/dataset/660e3969-c011-481c-aa24-8a949ac2d62d/resource/4d06b680-f527-4f23-a1fd-45af752b4862/download"

def get_max_ridership_from_csv():
    """從捷運開放平台下載CSV，並找出2024-10的最高運量日"""

    response = requests.get(CSV_URL)
    response.raise_for_status()
    
    with open("metro_data.csv", "wb") as file:
        file.write(response.content)
    
    # 讀取csv並分析檔案
    try:
        metro_data_df = pd.read_csv("metro_data.csv", encoding="big5")

    except UnicodeDecodeError:
        logging.warning("Big5 分析失敗，嘗試 UTF-8-SIG 分析")
        metro_data_df = pd.read_csv("metro_data.csv", encoding="utf-8-sig")

    # 分析每個營運日
    metro_data_df = metro_data_df[metro_data_df["營運日"].astype(str).str.match(r"^2024-10")]  # 確保日期格式正確
    metro_data_df = metro_data_df[metro_data_df["總運量"].apply(lambda x: str(x).replace(",", "").isdigit())]  # 確保總運量為數字
    
    # 取得最高總運量
    max_ridership_record = metro_data_df.loc[metro_data_df["總運量"].idxmax()]
    max_day = max_ridership_record["營運日"]
    max_ridership = max_ridership_record["總運量"]

    # 統一日期格式
    year, month, day = max_day.split("-")
    roc_year = str(int(year) - 1911)  # 轉換為民國年
    max_day_roc = f"{roc_year}/{month}/{day}"
    
    logging.info(f"CSV 最高運量日: {max_day_roc} 總運量: {max_ridership}")

    return max_day_roc, max_ridership