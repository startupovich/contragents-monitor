import os
from pathlib import Path

# ---- Google Sheet ----
GSPREAD_SERVICE_ACC_JSON = Path("service_account.json")   # файл скачан из Google Cloud
SHEET_NAME              = "Контрагенты"       # название таблицы
WORKSHEET_NAME          = "Лист1"             # или любой

# ---- парсинг ----
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; INJITEK-monitor/1.0)",
}
RUSPROFILE_URL = "https://www.rusprofile.ru/ajax.php?uid={inn}&method=card"

# ---- storage ----
DB_PATH = "snapshot.db"
CSV_LOG_DIR = Path("logs")
CSV_LOG_DIR.mkdir(exist_ok=True)

# ---- прочее ----
TIMEOUT = 15   # seconds