import csv
import logging
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    """Возвращает соединение с БД из переменных окружения."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def load_csv_to_db(csv_path: Path, conn):
    """Загружает CSV в таблицу users с обработкой дубликатов."""
    # Твой код здесь:
    # 1. Открыть CSV
    # 2. Пройти по строкам
    # 3. Вставить в БД с параметризованным запросом
    # 4. Обработать дубликаты: ON CONFLICT (email) DO NOTHING
    # 5. Посчитать и залогировать: прочитано / вставлено / пропущено
    pass

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    csv_file = base_dir.parent.parent / 'data' / 'clean' / 'clean_users.csv'
    
    logger.info(f"Загружаем данные из {csv_file}")
    
    with get_db_connection() as conn:
        loaded = load_csv_to_db(csv_file, conn)
        logger.info(f"✅ Загружено строк: {loaded}")