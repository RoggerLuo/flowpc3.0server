from flask_cors import *
from flask import Flask, render_template, Response, request
import json
import mysql_operation as sql
from sentence import Sentence

app = Flask(__name__, static_folder='static')
CORS(app, supports_credentials=True)


@app.route('/header', methods=['GET','POST'])
def header():
    if (request.method == 'POST'):
        text = sql.writeHeaderText(request.form['text'])
        return json.dumps('ok')

    if (request.method == 'GET'):
        text = sql.getHeaderText()
        return json.dumps(text)


@app.route('/search/<sentence>', methods=['GET'])
def search(sentence):
    s = Sentence(sentence)
    word_list = s.segment().filter().word_list
    found_list = findSimilarWords.by_word_list(word_list, 20)
    if len(found_list) != 0:
        return json.dumps(found_list)
    else:
        return json.dumps([])


@app.route('/notes', methods=['GET'])
def notes():
    notes = sql.readNotes()
    if len(notes) != 0:
        return json.dumps(notes)
    else:
        return json.dumps([])


@app.route('/note/<item_id>', methods=['POST', 'PUT', 'DELETE'])
def note(item_id):
    if (request.method == 'POST') or (request.method == 'PUT'):
        content = request.form['content']
        sql.touchNote(item_id, content)
    
    if request.method == 'DELETE':
        sql.deleteNote(item_id)
    
    return json.dumps('ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)  # ,  debug=True


# if request.method == 'GET':
#     notes = sql.readNotesById(item_id)
#     if len(notes) != 0:
#         return json.dumps(notes[0])
#     else:
#         return json.dumps({})
