import config
from collections import defaultdict
import os
import re
import operator


def get_lemmas(text):
    return [token.split(':')[0] for token in text.split('\n')]


def get_inverted_index():
    term_documents_dict = defaultdict(list)
    for root, dirs, files in os.walk(config.LEMMAS_FOLDER):
        for file in files:
            if file.lower().endswith('_lemmas.txt'):
                idx = re.search('\d+', file).group(0)
                with open(os.path.join(root, file), encoding='utf-8') as f:
                    lemmas = get_lemmas(f.read())
                for lemma in lemmas:
                    if lemma == '':
                        continue
                    term_documents_dict[lemma].append(idx)
    return term_documents_dict


def start():
    inverted_index = get_inverted_index()
    keys = sorted(inverted_index.keys())
    with open(f'{config.GENERATED_FOLDER}/inverted_index.txt', 'w', encoding='utf-8') as f:
        for term in keys:
            f.write(f"{term} {' '.join(map(str, inverted_index[term]))}\n")
    inverted_index_info = [{'count': len(docs), 'inverted_array': docs, 'word': term} for term, docs in
                           inverted_index.items()]
    with open(f'{config.GENERATED_FOLDER}/inverted_index_2.txt', 'w', encoding='utf-8') as f:
        for term_info in inverted_index_info:
            f.write(str(term_info) + '\n')
