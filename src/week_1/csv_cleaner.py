import csv
import logging
from datetime import datetime
from pathlib import Path
 
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR.parent.parent / 'data' / 'raw' / 'raw_users.csv'
OUTPUT_FILE = BASE_DIR.parent.parent / 'data' / 'clean' / 'clean_users.csv'
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

date_format = "%Y-%m-%d"

def read_csv_file(path):
    csv_data = []
    with open(path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            csv_data.append(row)
    return csv_data

def validation_data(data):
    clean_data = []
    count_row = 0

    for row in data:
        count_row += 1
        if row['name'] == '' or row['email'] == '':
            print('Найден пропуск в данных')
            continue
        try:
            if datetime.strptime(row['signup_date'], date_format):
                pass
        except ValueError:
            row['signup_date'] = 'Unknown'
        clean_data.append(row)

    return clean_data

def write_csv_file(path, data):
    fieldnames = data[0].keys()
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Записать заголовки
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    csv_data = read_csv_file(INPUT_FILE)
    clean_data = validation_data(csv_data)
    write_csv_file(OUTPUT_FILE, clean_data)