import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
from utils.logging_config import setup_logging

setup_logging()

WEB_URL = "https://web.metro.taipei/RidershipCounts/c/11310.htm"

def get_max_ridership_from_web():
    """從捷運官網爬取 113/10 總運量最高日"""

    logging.info("爬取捷運官網數據...")

    # 取得網站
    response = requests.get(WEB_URL)
    response.raise_for_status()
    response.encoding = "big5"

    # 解析網站 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 取得所有表格
    rows = soup.select("table tr")
    max_day, max_ridership = None, 0

    # 儲存每日運量與平均
    daily_data = []
    summary_data = {}

    logging.info("解析網頁數據...")

    # 分析數據類型
    for i, row in enumerate(rows):
        cols = row.find_all("td")

        # 分析每個欄位
        row_text = [] 
        for col in cols:
            text = col.text  # 取得該欄位的文字
            cleaned_text = text.strip()
            row_text.append(cleaned_text)

        # 判斷是否為每日數據
        if len(row_text) == 3 and row_text[0].startswith("113/10"):  
            date = row_text[0]  # 營運日
            day_of_week = row_text[1]  # 星期
            raw_ridership = row_text[2]  # 總運量

            if raw_ridership.replace(",", "").isdigit():
                ridership = int(raw_ridership.replace(",", ""))
                daily_data.append((date, ridership))

                logging.info(f"每日數據: 營運日 {date}, 總運量 {ridership}")

        # 判斷是否為摘要資訊
        elif len(row_text) == 2:  
            title = row_text[0]
            value = row_text[1]

            if "總計" in title or "當月" in title:
                summary_data["total_ridership"] = int(value.replace(",", ""))
                logging.info(f"總計: {summary_data['total_ridership']}")

            elif "平均" in title:
                summary_data["avg_ridership"] = int(value.replace(",", ""))
                logging.info(f"日平均: {summary_data['avg_ridership']}")

    # 計算最高運量日
    if daily_data:
        df = pd.DataFrame(daily_data, columns=["營運日", "總運量"])
        max_row = df.loc[df["總運量"].idxmax()]
        max_day = max_row["營運日"]
        max_ridership = max_row["總運量"]

    logging.info(f"網站最高運量日: {max_day} 總運量為: {max_ridership}")
    logging.info(f"當月總計: {summary_data.get('total_ridership')}, 日平均: {summary_data.get('avg_ridership')}")

    return max_day, max_ridership, summary_data.get("total_ridership"), summary_data.get("avg_ridership")