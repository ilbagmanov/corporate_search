import io
import os
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request, send_file

import database.db as db
import prepare_tokens_and_lemmas
import search_inverted_index
import search_vector_model

app = Flask(__name__)


def prepare_app():
    if not os.path.exists("/tmp/diploma_search"):
        os.makedirs("/tmp/diploma_search")
prepare_app()
Document_file = namedtuple('Document_file', 'text')
document_files = []


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', document_files=document_files)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    document_files.clear()
    titles = search_vector_model.search(text)
    for title in titles:
        document_files.append(Document_file(text=title))
    # result = search_inverted_index.search(text)
    # if len(result) != 0:
    #     sql_str = '(' + ', '.join(map(str, result)) + ')'
    #     titles = db.execute_query(f"SELECT array_agg(title) as titles FROM documents WHERE id IN {sql_str}")
    #     for title in titles[0][0]:
    #         document_files.append(Document_file(text=title))
    return redirect(url_for('main'))


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_id = db.save_document(file)
    prepare_tokens_and_lemmas.start(file_id)
    return redirect(url_for('main'))


@app.route('/all_files', methods=['GET'])
def all_files():
    document_files.clear()
    titles = db.get_all_documents_names()
    for title in titles:
        document_files.append(Document_file(text=title[0]))
    return redirect(url_for('main'))


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    result = db.execute_query(f"SELECT file_data, title FROM documents WHERE title = '{filename}' LIMIT 1")
    file_data = io.BytesIO(result[0][0].tobytes())
    file_name = result[0][1]

    return send_file(file_data, download_name=file_name, as_attachment=True)


@app.route('/delete/<path:filename>', methods=['GET'])
def delete(filename):
    return None
