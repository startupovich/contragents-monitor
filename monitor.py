#!/usr/bin/env python3
from sheets import fetch_inn_list
from parsers import fetch_card_raw, extract_essentials
from storage import load_previous, save_current, diff, log_csv
from datetime import datetime

def main():
    inns = fetch_inn_list()
    print(f"{datetime.now():%Y-%m-%d %H:%M} — старт, {len(inns)} контрагентов")

    csv_rows = []
    total_changes = 0

    for inn in inns:
        raw = fetch_card_raw(inn)
        if raw is None:
            print(f"[{inn}] ❌ не смог получить данные")
            continue

        now = extract_essentials(raw)
        old = load_previous(inn)
        changes = diff(old, now)

        if changes:
            total_changes += len(changes)
            org_name = raw.get("name", "Неизвестно")
            print(f" • {org_name} ({inn}): {len(changes)} изм.")
            for field, o, n in changes:
                csv_rows.append(
                    dict(dt=datetime.now(), inn=inn, field=field, old=o, new=n)
                )
        save_current(inn, now)

    csv_path = log_csv(csv_rows)
    print(
        f"✅ Завершено: {total_changes} изменений "
        f"({csv_path.name if csv_path else 'без лога'})"
    )

if __name__ == "__main__":
    main()