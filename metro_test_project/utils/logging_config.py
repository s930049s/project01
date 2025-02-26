import logging

def setup_logging():
    """設定 logging只輸出到終端機"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",

        # 確保日誌輸出到終端
        handlers=[logging.StreamHandler()]  
    )