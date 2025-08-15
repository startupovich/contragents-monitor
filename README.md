# 📊 Контрагенты-24 — Rustprofile Monitor  

> Лёгкий Python-скрипт, который раз в сутки проверяет ваших контрагентов на Rusprofile / bo.nalog.ru,  
> фиксирует изменения (банкротство, арбитраж, смена директора …), пишет полноценный CSV-лог  
> и, при желании, шлёт уведомления (Telegram / e-mail — опционально).

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Зачем это нужно

* Снимает рутину due-diligence: экономит 10–15 минут на каждого контрагента.  
* Снижает риск: узнаёте о банкротстве / крупном иске в день публикации.  
* Формирует датасет изменений ➜ можно показывать клиентам/руководству.  

---

## ⚙️ Что умеет

| 🔍 Проверка | Источник | Как фиксируем |
|-------------|----------|--------------|
| Новые арбитражные дела | kad.arbitr / cardData | `last_arbitrazh` |
| Банкротство / ликвидация | cardData | `bankrot`, `liquidated` |
| Выручка / штрафы ФССП | finance / fssp | `revenue`, `fssp_sum` |
| Смена директора | management → name | `director` |
| Перестановка учредителей | founders[] | `founders` |

Каждое отличие между «вчера» и «сегодня» попадает в `logs/diff_YYYY-MM-DD.csv`.

---

## 🛠️ Быстрый старт

```bash
git clone https://github.com/ВАШ_ЛОГИН/contragents-monitor.git
cd contragents-monitor

python -m venv venv           # создаём виртуалку
venv/Scripts/activate         # Windows
# source venv/bin/activate    # Linux / macOS

pip install -r requirements.txt
```

1. Создайте Google-таблицу 📄  
   *A1* — заголовок «INN», дальше в колонке список ИНН.

2. Cделайте сервис-аккаунт в Google Cloud → скачайте `service_account.json` →  
   положите в корень проекта и выдайте ему доступ *edit* к вашей таблице.

3. Запустите:

```bash
python monitor.py
```

На экране появится краткая сводка, а в `logs/` — CSV с изменениями (если они найдены).  

---

## 🗂️ Структура проекта

```
monitor/
├─ monitor.py      # точка входа
├─ parsers.py      # забираем и упрощаем cardData
├─ sheets.py       # читаем список ИНН из Google Sheet
├─ storage.py      # SQLite-снимки + diff + CSV-лог
├─ config.py       # все настройки / пути / токены
├─ requirements.txt
└─ logs/           # сюда кидаются diff_*.csv
```

---

## 🔧 Конфигурация (`config.py`)

```python
SHEET_NAME      = "Контрагенты"     # название таблицы
WORKSHEET_NAME  = "Лист1"           # лист c ИНН
RUSPROFILE_URL  = "https://www.rusprofile.ru/ajax.php?uid={inn}&method=card"
DB_PATH         = "snapshot.db"     # SQLite-хранилище
```

Все «секреты» (токены, chat-id) можно задавать через переменные среды, чтобы не коммитить их.

---

## ⏰ Автоматический запуск

### a) Windows Task Scheduler  
```
Program/script:  <путь к python.exe>
Arguments:       monitor.py
Trigger:         Daily at 07:00
```

### b) Cron (Linux)
```cron
0 7 * * * /home/user/monitor/venv/bin/python /home/user/monitor/monitor.py
```

### c) GitHub Actions — 100 % в облаке (бесплатно)

`.github/workflows/monitor.yml`
```yaml
name: Daily monitor
on:
  schedule: [ { cron: "0 4 * * *" } ]   # UTC → 07:00 МСК
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: python monitor.py
```

---

## 📈 Пример вывода

```
2025-08-14 07:01 — старт, 27 контрагентов
 • ООО «Ромашка» (7703123456): 2 изм.
 • ИП Сидоров (7726999999):    1 изм.
✅ Завершено: 3 изменений (diff_2025-08-14.csv)
```

`diff_2025-08-14.csv`

| dt | inn | field | old | new |
|----|-----|-------|-----|-----|
| 2025-08-14 07:01 | 7703123456 | last_arbitrazh | 2024-06-01 | 2025-08-13 |
| 2025-08-14 07:01 | 7703123456 | fssp_sum       | 0          | 250 000 |
| 2025-08-14 07:01 | 7726999999 | director       | Иванов И.И. | Петров П.П. |

---

