import requests, json
from bs4 import BeautifulSoup
from typing import Dict, Optional
from config import HEADERS, RUSPROFILE_URL, TIMEOUT

def fetch_card_raw(inn: str) -> Optional[dict]:
    """
    Получает JSON-блок cardData с Rusprofile.
    Возвращает dict или None.
    """
    url = RUSPROFILE_URL.format(inn=inn)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"[{inn}] HTTP error: {e}")
        return None

    try:
        data = resp.json()
        return data.get("cardData")
    except Exception as e:
        # иногда страница возвращается html — парсим ручками
        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            print(f"[{inn}] no JSON found")
            return None
        try:
            root = json.loads(script.string)
            return root["props"]["pageProps"]["cardData"]
        except Exception as e2:
            print(f"[{inn}] JSON parse error: {e2}")
            return None

def extract_essentials(card: dict) -> Dict:
    """
    Вырезаем только интересующие поля,
    чтобы diff был компактным.
    """
    if not card:
        return {}
    return dict(
        revenue=card.get("finance", {}).get("revenue"),
        fssp_sum=card.get("fssp", {}).get("penaltiesSum"),
        last_arbitrazh=card.get("court", {}).get("lastCaseDate"),
        bankrot=card.get("bankruptStatus"),
        liquidated=card.get("liquidated"),
        director=card.get("management", {}).get("name"),
        founders=tuple(sorted(f["name"] for f in card.get("founders", []))),
    )