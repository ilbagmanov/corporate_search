import re
import sys
from collections import defaultdict

from nltk import RegexpTokenizer
from pymorphy2 import MorphAnalyzer

from database import db


def get_inverted_index():
    term_documents_dict = defaultdict(list)
    result = db.execute_query('''
        SELECT word, array_agg(document_id) AS word_array FROM word_documents
        LEFT JOIN words w on w.id = word_documents.word_id GROUP BY word
        ''')
    for lemma_data in result:
        lemma = lemma_data[0]
        ids = lemma_data[1]
        term_documents_dict[lemma] = ids
    return term_documents_dict

inverted_index = get_inverted_index()


def get_document_count():
    result = db.execute_query("SELECT array_agg(id) as ids FROM documents")
    return set(result[0][0])

def tokenize(s):
    # токенизатор на регулярных выражениях
    tknzr = RegexpTokenizer(r'[А-Яа-яёЁ&(\|)~\)\(]+')
    clean_words = tknzr.tokenize(s)
    # print(clean_words)
    clean_words = [w.lower() for w in clean_words if w != '']
    return list(clean_words)


def lemmatize(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = []
    for token in tokens:
        if re.match(r'[А-Яа-яёЁ]', token):
            lemma = pymorphy2_analyzer.parse(token)[0].normal_form
            lemmas.append(lemma)
        else:
            lemmas.append(token)
    return lemmas


def priority(oper):
    if oper == '&':
        return 2
    elif oper == '|':
        return 1
    return -1


def get_prn(operands):
    result = []
    stack = []
    for operand in operands:
        if operand not in ['&', '|']:
            result.append(operand)
        else:
            last = None if len(stack) == 0 else stack[-1]
            while priority(last) >= priority(operand):
                result.append(stack.pop())
                last = None if not stack else stack[-1]
            stack.append(operand)
    for el in reversed(stack):
        result.append(el)
    return result


def get_index(word):
    if word[0] == '~':
        try:
            indices = set(inverted_index[word[1:]])
            x = get_document_count()
            y = x - indices
            return y
        except KeyError:
            return set()
    else:
        try:
            index = inverted_index[word]
            return set(index)
        except KeyError:
            return set()


def evaluate(tokens):
    stack = []
    for token in tokens:
        if token in ['&', '|']:
            arg2, arg1 = stack.pop(), stack.pop()
            if token == '&':
                result = arg1 & arg2
            else:
                result = arg1 | arg2
            stack.append(result)
        else:
            stack.append(get_index(token))
    return stack.pop()


def tokenize_query(query):
    tokenized_query = []

    for (index, word) in enumerate(query.split(' ')):
        if word == '&' or word == '|':
            tokenized_query.append(word)
        else:
            if word[0] == '~':
                tokenized_word = lemmatize(tokenize(word[1:]))[0]
                tokenized_query.append('~' + tokenized_word)
            else:
                tokenized_word = lemmatize(tokenize(word))[0]
                tokenized_query.append(tokenized_word)

    return tokenized_query


def search(query):
    tokenized_query = tokenize_query(query)
    converted_query = get_prn(tokenized_query)
    result = evaluate(converted_query)
    print(result)
    return result


def test():
    queries = {
        "эти"
    }
    for query in queries:
        search(query)


if __name__ == '__main__':
    query = sys.argv[1]
    search(query)