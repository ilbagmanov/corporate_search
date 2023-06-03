import psycopg2
import config

connection = psycopg2.connect(
    database=config.DATABASE_NAME,
    user=config.DATABASE_USER,
    password=config.DATABASE_PASSWORD,
    host=config.DATABASE_HOST,
    port=config.DATABASE_PORT
)


def close_connection():
    connection.close()


def save_document(file):
    file_data = file.read()
    query = 'INSERT INTO documents (title, file_data) values (%s, %s) RETURNING id'
    cursor = connection.cursor()
    cursor.execute(query, (file.filename, file_data))
    id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    return id


def get_document_by_id(file_id):
    return execute_query(f"SELECT title, file_data FROM documents WHERE id = {file_id}")


def save_lemmas(lemmas):
    lemmas_to_save = [', '.join(["('{}')".format(item[0]) for item in lemmas.items()][i:i + 10]) for i in
                      range(0, len(lemmas), 10)]
    cursor = connection.cursor()
    for line in lemmas_to_save:
        cursor.execute(f"INSERT INTO words (word) values {line} ON CONFLICT DO NOTHING")
        connection.commit()
    cursor.close()


def tie_lemmas_to_document(lemmas, file_id):
    cursor = connection.cursor()
    for lemma in lemmas:
        lemma_id = execute_query(f"SELECT id FROM words WHERE word = '{lemma}'")[0][0]
        cursor.execute(f"INSERT INTO word_documents (word_id, document_id) VALUES ({lemma_id}, {file_id})")
        connection.commit()
    cursor.close()


def get_all_documents_names():
    titles = execute_query("SELECT title FROM documents")
    return titles


def execute_query(query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
