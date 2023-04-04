import os
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request, send_from_directory

import config
import search_inverted_index

app = Flask(__name__)

Message = namedtuple('Message', 'text')
messages = []


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    result = search_inverted_index.search(text)
    messages.clear()
    with open(config.INDEX_FILE, 'r') as f:
        for line in f.read().split("\n"):
            if line[0:line.find(' ')] in result:
                messages.append(Message(text=line[line.find(' '):].strip()))
    return redirect(url_for('main'))


@app.route('/uploads/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(app.root_path, 'unprocessed_docs/')
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f'{config.UNPROCESSED_DOCS_FOLDER}/{file.filename}')
    messages.clear()
    return redirect(url_for('main'))


@app.route('/delete/<path:filename>', methods=['GET'])
def delete(filename):
    return None


@app.route('/all_message', methods=['GET'])
def all_message():
    messages.clear()
    with open(config.INDEX_FILE, 'r') as f:
        for line in f.read().split("\n"):
            if line.strip() == '':
                continue
            messages.append(Message(text=line[line.find(' '):].strip()))
    return redirect(url_for('main'))
