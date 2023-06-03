import psycopg2
import config
import re

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
    file_name = re.sub(r'[^\w.]', '', file.filename)
    file_data = file.read()
    query = 'INSERT INTO documents (title, file_data) values (%s, %s) RETURNING id'
    cursor = connection.cursor()
    cursor.execute(query, (file_name, file_data))
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
        cursor.execute(f"INSERT INTO word_documents (word_id, document_id, count) VALUES ({lemma_id}, {file_id}, {len(lemmas[lemma])})")
        connection.commit()
    cursor.close()


def update_document_by_word_count(file_id, token_count):
    cursor = connection.cursor()
    cursor.execute(f"UPDATE documents SET word_count = {token_count} WHERE id = {file_id}")
    connection.commit()
    cursor.close()


def get_all_documents():
    files = execute_query("SELECT id, title FROM documents")
    return files


def delete_file_by_id(file_id):
    cursor = connection.cursor()
    cursor.execute(f'''
        DELETE FROM word_documents
        WHERE document_id = {file_id};
        DELETE FROM documents
        WHERE id = {file_id};
    ''')
    connection.commit()
    cursor.close()


def execute_query(query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
