from category import *
from note import *
from notes import *
from flask import Flask, request
import flask_cors
app = Flask(__name__, static_folder='static')
flask_cors.CORS(app, supports_credentials=True)

@app.route('/notes', methods=['GET'])
def notes(): # 各种条件查询
    categoryId = request.args.get('categoryId')
    pageSize = request.args.get('pageSize')
    pageNum = request.args.get('pageNum')
    return query_notes(categoryId,pageSize,pageNum)

@app.route('/note/<note_id>', methods=['POST', 'PUT', 'DELETE'])
def note(note_id): # CRUD
    if request.method == 'POST':
        return create_note() # return note_id
    if request.method == 'PUT':
        return modify_note(note_id)
    if request.method == 'DELETE':
        return delete_note(note_id)

@app.route('/categories', methods=['GET'])
def categories(): # 各种条件查询
    return query_notes()

@app.route('/category/<category_id>', methods=['POST', 'PUT', 'DELETE'])
def category(note_id): # CRUD
    if request.method == 'POST':
        return create_category() # return category_id
    if request.method == 'PUT':
        return modify_category(category_id)
    if request.method == 'DELETE':
        return delete_category(category_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) 
