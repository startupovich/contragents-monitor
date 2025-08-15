import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List
from config import GSPREAD_SERVICE_ACC_JSON, SHEET_NAME, WORKSHEET_NAME

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name(
        GSPREAD_SERVICE_ACC_JSON, SCOPE
    )

def fetch_inn_list() -> List[str]:
    gc = gspread.authorize(get_creds())
    ws = gc.open(SHEET_NAME).worksheet(WORKSHEET_NAME)
    inns = ws.col_values(1)[1:]        # первая колонка, без заголовка
    return [inn.strip() for inn in inns if inn.strip()]