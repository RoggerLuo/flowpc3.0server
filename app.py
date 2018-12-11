#from category import query_categories,create_category,modify_category,delete_category
#from note import create_note,modify_note,delete_note
from note import create_note#,modify_note,delete_note

from notes import query_notes
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

@app.route('/note', methods=['POST']) # post方法要使用  x-www-form来访问，不然400
def notedd(): 
    content = request.form['content']
    return create_note(content) # return note_id

# @app.route('/note/<note_id>', methods=['POST', 'DELETE'])
# def note_with_id(note_id):
#     if request.method == 'PUT':
#         return modify_note(note_id)
#     if request.method == 'DELETE':
#         return delete_note(note_id)

# @app.route('/categories', methods=['GET'])
# def categories(): # 各种条件查询
#     return query_categories()

# @app.route('/category/<category_id>', methods=['POST', 'PUT', 'DELETE'])
# def category(note_id): # CRUD
#     if request.method == 'POST':
#         return create_category() # return category_id
#     if request.method == 'PUT':
#         return modify_category(category_id)
#     if request.method == 'DELETE':
#         return delete_category(category_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5556, debug=False) 
