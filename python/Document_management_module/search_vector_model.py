import operator
import database.db as db
import math

from sklearn.metrics.pairwise import cosine_similarity

import search_inverted_index


def calculate(term, document_tokens_list, documents_count, documents_with_term_count):
    TF = document_tokens_list.count(term) / len(document_tokens_list)
    IDF = math.log(documents_count / documents_with_term_count)
    return round(TF, 6), round(IDF, 6), round(TF * IDF, 6)


def dist_cosine(vec_a, vec_b):
    cosine = cosine_similarity([vec_a], [vec_b])
    return cosine[0][0]


def search(query):
    all_docs_count = db.execute_query("SELECT count(*) FROM documents")[0][0]
    tokens = search_inverted_index.tokenize_query(query)
    if len(tokens) == 0:
        return

    query_vector = []
    for token in tokens:
        doc_with_terms_count = db.execute_query(f'''
            SELECT count(document_id) FROM word_documents
            LEFT JOIN words w on w.id = word_documents.word_id
            WHERE word = '{token}'
        ''')[0][0]

        tf_idf = 0.0
        if doc_with_terms_count != 0:
            _, _, tf_idf = calculate(token,
                                     tokens,
                                     all_docs_count,
                                     doc_with_terms_count)
        query_vector.append(tf_idf)

    distances = {}

    indices = db.execute_query("SELECT array_agg(id) FROM documents")[0][0]
    for index in indices:
        document_vector = []

        for token in tokens:
            try:
                token_count = db.execute_query(f'''
                    SELECT sum(count) FROM word_documents
                    WHERE document_id = {index} AND word_id = (SELECT words.id FROM words WHERE word = '{token}') ''')[
                    0][0]
                doc_words_count = db.execute_query(f'''SELECT word_count FROM documents WHERE id = {index}''')[0][0]
                docs_count_with_token = db.execute_query(f'''
                    SELECT count(document_id) FROM word_documents LEFT JOIN words w on w.id = word_documents.word_id WHERE word = '{token}'
                ''')[0][0]
                TF = token_count / doc_words_count
                IDF = math.log(len(indices) / docs_count_with_token)
                tf_idf = round(TF * IDF, 6)
                document_vector.append(tf_idf)
            except Exception:
                document_vector.append(0.0)

        distances[index] = dist_cosine(query_vector, document_vector)

    searched_indices = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)

    files = []
    for index in searched_indices:
        doc_id, tf_idf = index
        if tf_idf < 0.05:
            continue
        files.append(db.execute_query(f"SELECT id, title FROM documents WHERE id = {doc_id}")[0])
    return files
