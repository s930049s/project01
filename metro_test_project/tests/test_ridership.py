import pytest
import logging
from metro_ridership.data_fetcher import get_max_ridership_from_csv
from metro_ridership.scraper import get_max_ridership_from_web
from utils.logging_config import setup_logging

setup_logging()


def test_metro_ridership():
    """測試CSV與官網數據的最高運量日是否相符"""

    csv_day, csv_ridership = get_max_ridership_from_csv()
    web_day, web_ridership, total_ridership, avg_ridership = get_max_ridership_from_web()
    
    web_ridership = int(web_ridership)
    logging.info(f"測試數據是否相符: CSV ({csv_day}, {csv_ridership}) VS 網站 ({web_day}, {web_ridership})")
    logging.info(f"網站當月總計: {total_ridership}, 日平均: {avg_ridership}")
    
    # 1. 測試CSV & 爬蟲數據
    assert csv_ridership == web_ridership, f"總運量不匹配！CSV: {csv_ridership}, 官網: {web_ridership}"

    # 2. 測試最高運量日是否一致
    assert csv_day == web_day, f"最高運量日不匹配 CSV: {csv_day}, 官網: {web_day}"

    # 3. 確保爬蟲的數據不為 None
    assert web_day is not None and web_ridership is not None, "官網爬蟲數據異常"

    # 4. 測試CSV是否有空值
    assert csv_day != "" and csv_ridership > 0, "CSV 數據中有空值"

    # 5. 測試爬蟲數據是否有空值
    assert web_day != "" and web_ridership > 0, "官網數據中有空值"

    # 6. 測試最高運量日的格式
    assert isinstance(csv_day, str) and "/" in csv_day, "CSV 最高運量日格式錯誤"
    assert isinstance(web_day, str) and "/" in web_day, "官網 最高運量日格式錯誤"

    # 7. 當月總計與日平均數據應為正數
    assert total_ridership > 0, "當月總計數據異常，應該為正整數"
    assert avg_ridership > 0, "日平均數據異常，應該為正整數"

    # 8. 測試當月總計應大於最高運量日
    assert total_ridership > max(csv_ridership, web_ridership), "當月總計應該大於最高運量日的數據"

    # 測試爬蟲是否能夠正常運行
    assert isinstance(web_day, str) and isinstance(web_ridership, int), "爬蟲返回的數據類型錯誤"

    logging.info("-----所有測試案例通過-----")