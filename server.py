from flask_cors import *
from flask import Flask, render_template, Response, request
import json
import mysql_operation as sql
from w2v import findSimilarWords
from w2v.WordsCompress import WordsCompress
from string2word import String2word
from w2v import noteSearch
app = Flask(__name__, static_folder='static')
CORS(app, supports_credentials=True)
s2w = String2word()

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
    word_list = s2w.segment(sentence).filter()
    if len(word_list) > 5:
        compress = WordsCompress()
        word_list = compress.feedWordlist(word_list)

    found_list = findSimilarWords.by_word_list(word_list,25)
    # found_list = noteSearch.by_single_word(word_list)
    for word in word_list:
        sql.writeHistory(word) # 添加列表

    if len(found_list) != 0:
        return json.dumps(found_list)
    else:
        return json.dumps([])


@app.route('/history', methods=['GET'])
def history():
    arr = sql.readHistory()
    if len(arr) != 0:
        return json.dumps(arr)
    else:
        return json.dumps([])

# @app.route('/history/<word>', methods=['GET'])
# def writeHistory(word):
#     sql.writeHistory(word)
#     return json.dumps('ok')


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
        wordlist = s2w.segment(content).filter()
        sql.touchNote(item_id,content,json.dumps(wordlist,ensure_ascii=False))
    
    if request.method == 'DELETE':
        sql.deleteNote(item_id)
    
    return json.dumps('ok')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)  # ,  debug=True
