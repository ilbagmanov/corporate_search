import os
import textract
import re
import config
import nltk

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from collections import defaultdict

nltk.download('stopwords')
stop_words = stopwords.words('russian') + stopwords.words('english')

accepted_formats = ['.txt', '.doc', '.docx', '.pdf']

def upload_index_to_file(index, path):
    file = open(path, "w", encoding="utf-8")
    for k, v in index.items():
        file.write(f'{k} {v}\n')
    file.close()

def upload_lemmas_to_file(lemmas, path):
    file = open(path, "w", encoding="utf-8")
    for k, v in lemmas.items():
        file.write(k + ": ")
        for word in v:
            file.write(word + " ")
        file.write("\n")
    file.close()


def upload_tokens_to_file(content, path):
    file = open(path, "w", encoding="utf-8")
    file.write(content)
    file.close()


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


def prepare_tokens_and_lemmas(filenames):
    idx = 0
    index = dict()
    for filename in filenames:
        text = textract.process(f"{config.UNPROCESSED_DOCS_FOLDER}/{filename}").decode()
        tokens = list(set(get_tokens(text)))
        lemmas = get_lemmas(tokens)
        upload_tokens_to_file('\n'.join(tokens), f'{config.TOKENS_FOLDER}/{idx}_tokens.txt')
        upload_lemmas_to_file(lemmas, f'{config.LEMMAS_FOLDER}/{idx}_lemmas.txt')
        index.update({idx : filename})
        idx = idx + 1
        print('DONE')
    upload_index_to_file(index, config.INDEX_FILE)


def prepare_folders():
    os.makedirs(os.path.dirname(config.TOKENS_FOLDER + '/'), exist_ok=True)
    os.makedirs(os.path.dirname(config.LEMMAS_FOLDER + '/'), exist_ok=True)
    os.makedirs(os.path.dirname(config.PROCESSED_DOCS_FOLDER + '/'), exist_ok=True)


def find_files():
    filenames = []
    for name in os.listdir(f"{config.UNPROCESSED_DOCS_FOLDER}"):
        file_type = re.findall('\\.[^ .]+$', name)
        if len(file_type) == 0 or file_type[0] not in accepted_formats:
            print(f'ERROR: file_type not detected - {name}')
            continue
        print(f'Название: {name}')
        filenames.append(name)
    return filenames


def start():
    filenames = find_files()
    prepare_folders()
    prepare_tokens_and_lemmas(filenames)
    print(str(filenames))
