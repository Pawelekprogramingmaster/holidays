import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


def convert_time_ranges_to_utc(date_str, time_ranges_str, local_tz_str="Etc/GMT-1"):
    if not isinstance(time_ranges_str, str) or not time_ranges_str.strip():
        return []

    time_ranges = [line.strip() for line in time_ranges_str.split("\n") if line.strip()]
    utc_ranges = []
    local_tz = ZoneInfo(local_tz_str)
    utc_tz = ZoneInfo("UTC")

    for time_range in time_ranges:
        try:
            start_str, end_str = [t.strip() for t in time_range.split("-")]

            start_dt = datetime.strptime(f"{date_str} {start_str}", "%d.%m.%Y %H:%M")

            # Obsługa 24:00 jako 00:00 następnego dnia
            if end_str == "24:00":
                end_dt = datetime.strptime(f"{date_str} 00:00", "%d.%m.%Y %H:%M") + pd.Timedelta(days=1)
            else:
                end_dt = datetime.strptime(f"{date_str} {end_str}", "%d.%m.%Y %H:%M")

            start_dt = start_dt.replace(tzinfo=local_tz)
            end_dt = end_dt.replace(tzinfo=local_tz)

            utc_ranges.append((
                start_dt.astimezone(utc_tz),
                end_dt.astimezone(utc_tz)
            ))

        except Exception as e:
            print(f"Błąd przetwarzania '{time_range}' dla daty {date_str}: {e}")
            continue

    return utc_ranges

if __name__ == "__main__":
    plik_excel = input("Podaj ścieżkę do pliku Excel (.xlsx): ").strip()

    plik_excel2 = (
        plik_excel
        .replace("\\", "/")
        .replace('"', "")
    )


    def parse_excel_and_convert(file_path):
        # 1. Wczytaj plik Excel
        df = pd.read_excel(file_path, engine="openpyxl")

        # 2. OD RAZU zamień wszystkie "- 00:00" na "- 24:00" we wszystkich kolumnach z godzinami
        df.iloc[:, 1:] = df.iloc[:, 1:].replace("- 00:00", "- 24:00", regex=False)

        # 3. Dalej normalne przetwarzanie
        results = []
        date_columns = df.columns[1:]  # od kolumny B w prawo

        for idx, row in df.iterrows():
            instrument = row[0]  # kolumna A

            for col in date_columns:
                date = str(col).strip()  # np. "03.07.2025"
                raw_time_ranges = row[col]
                utc_ranges = convert_time_ranges_to_utc(date, raw_time_ranges)

                for start_utc, end_utc in utc_ranges:
                    results.append({
                        "instrument": instrument,
                        "date": date,
                        "start_utc": start_utc.strftime("%d.%m.%Y %H:%M"),
                        "end_utc": end_utc.strftime("%d.%m.%Y %H:%M")
                    })

        return pd.DataFrame(results)

    try:
        df_result = parse_excel_and_convert(plik_excel2)
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {plik_excel2}")
        exit(1)
    except Exception as e:
        print(f"Wystąpił błąd podczas przetwarzania: {e}")
        exit(1)

    # Wyświetl pierwsze 5 wierszy
    print("\n✅ Przykładowe wyniki:")
    print(df_result.head())

    # Zapisz wynik
    output_path = "przeksztalcone_godziny_UTC.xlsx"
    df_result.to_excel(output_path, index=False)
    print(f"\n✅ Zapisano wynik do pliku: {output_path}")



