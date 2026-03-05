import csv
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, # Минимальный уровень отображения
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # формат строки
    datefmt='%Y-%m-%d %H:%M:%S' # формат времени
)

logger = logging.getLogger(__name__) # Получение логера для текущего файла

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

def parse_date(date_str):
    if not date_str or not date_str.strip():
        return 'Unknown'
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return date_str.strip()
    except ValueError:
        return 'Unknown'

def validation_data(data):
    clean_data = []
    filtered_count = 0

    for idx, row in enumerate(data, 1):
        if not row.get('name') or not row.get('email'):
            logger.warning(f'Пропуск в данных, строка {idx}')
            filtered_count += 1
            continue
        
        row['signup_date'] = parse_date(row.get('signup_date', ''))
        clean_data.append(row)

    logger.info(f'Обработано: {len(clean_data)}, отфильтровано: {filtered_count}')
    return clean_data

def write_csv_file(path, data):
    if not data:
        logger.warning("Нет данных для записи")
        return
    fieldnames = data[0].keys()
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Записать заголовки
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    logger.info('Скрипт запущен')
    csv_data = read_csv_file(INPUT_FILE)
    clean_data = validation_data(csv_data)
    write_csv_file(OUTPUT_FILE, clean_data)
    logger.info(f'Скрипт закончился свою работу')