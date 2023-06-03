# Database settings
DATABASE_NAME = 'diploma_search'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'qwerty808'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432

# TAGS на удаление
TAGS = ['style', 'script', 'meta', 'link', 'code']
# Название папки для выкачки
FOLDER = 'Выкачка'
# Название папки с необработанными файлами
UNPROCESSED_DOCS_FOLDER = 'unprocessed_docs'
# Папка с генерируемыми данными
GENERATED_FOLDER = 'data'
# Папка с токенами
TOKENS_FOLDER = f'{GENERATED_FOLDER}/токены'
# Папка с леммами
LEMMAS_FOLDER = f'{GENERATED_FOLDER}/леммы'
# Папка с обработанными файлами
PROCESSED_DOCS_FOLDER = 'processed_docs'
# Файл с индексами
INDEX_FILE = f'{GENERATED_FOLDER}/index.txt'