import os
import textract
import re
import nltk
import database.db as db

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from collections import defaultdict

nltk.download('stopwords')
stop_words = stopwords.words('russian') + stopwords.words('english')

accepted_formats = ['.txt', '.doc', '.docx', '.pdf']


def get_lemmas(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = defaultdict(list)
    for token in tokens:
        lemma = pymorphy2_analyzer.parse(token)[0].normal_form
        lemmas[lemma].append(token)
    return lemmas


def get_tokens(text):
    tknzr = RegexpTokenizer('[А-Яа-яёЁ]+')
    re.sub(r"[^А-Яа-яёЁ ]+[-'`][А-Яа-яёЁ]+", " ", text)
    words = tknzr.tokenize(text)
    result = []
    for word in words:
        word = word.lower()
        if word not in stop_words:
            result.append(word)
    return result


def prepare_tokens_and_lemmas(filename):
    file_path = os.path.join('/tmp/diploma_search', filename)
    text = textract.process(file_path).decode()
    all_tokens = get_tokens(text)
    token_count = len(all_tokens)
    lemmas = get_lemmas(all_tokens)

    return lemmas, token_count


def create_temporary_file(file_id):
    value = db.get_document_by_id(file_id)
    file_path = os.path.join('/tmp/diploma_search', value[0][0])
    with open(file_path, 'wb') as f:
        f.write(value[0][1])
    return value[0][0]


def delete_temporary_file(file_id):
    value = db.get_document_by_id(file_id)
    file_path = os.path.join('/tmp/diploma_search', value[0][0])
    os.remove(file_path)


def start(file_id):
    filename = create_temporary_file(file_id)
    lemmas, token_count = prepare_tokens_and_lemmas(filename)
    db.save_lemmas(lemmas)
    db.tie_lemmas_to_document(lemmas, file_id)
    db.update_document_by_word_count(file_id, token_count)
    delete_temporary_file(file_id)