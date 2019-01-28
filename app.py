from dao.classify import classify,unclassify
from dao.category import query_categories,create_category,modify_category,delete_category,orderChange,colorChange
from dao.note import create_note,modify_note,delete_note
from dao.notes import query_notes,find_notes
from flask import Flask, request
import flask_cors
from classifier import similarAlg
app = Flask(__name__, static_folder='static')
flask_cors.CORS(app, supports_credentials=True)

@app.route('/getSimilar/<note_id>', methods=['GET'])
def getSimilar(note_id):
    return similarAlg(note_id)

@app.route('/changeColor', methods=['POST'])
def changeColor():
    category_id = request.form['categoryId']
    color = request.form['color']
    return colorChange(category_id,color)

@app.route('/classify/<note_id>/<cate_id>', methods=['GET'])
def _classify(note_id,cate_id):
    return classify(note_id,cate_id)

@app.route('/unclassify/<note_id>', methods=['GET'])
def _unclassify(note_id):
    return unclassify(note_id)

@app.route('/notes', methods=['GET'])
def notes(): # 各种条件查询
    categoryId = request.args.get('categoryId')
    pageSize = request.args.get('pageSize')
    pageNum = request.args.get('pageNum')
    return query_notes(categoryId,pageSize,pageNum)

@app.route('/note', methods=['POST']) # post方法要使用  x-www-form来访问，不然400
def note(): 
    content = request.form['content']
    category_id = request.form['category_id']
    return create_note(content,category_id) # return note_id

@app.route('/note/<note_id>', methods=['POST', 'DELETE'])
def note_with_id(note_id):
    if request.method == 'POST':
        content = request.form['content']
        return modify_note(note_id,content)
    if request.method == 'DELETE':
        return delete_note(note_id)

@app.route('/categories', methods=['GET'])
def categories(): # 各种条件查询
    return query_categories()

@app.route('/category', methods=['POST'])
def category(): 
    if request.method == 'POST':
        name = request.form['name']
        return create_category(name) # return category_id

@app.route('/category/<category_id>', methods=['POST', 'DELETE'])
def category_with_id(category_id): 
    if request.method == 'POST':
        name = request.form['name']
        return modify_category(category_id,name)
    if request.method == 'DELETE':
        return delete_category(category_id)
@app.route('/order/<category_id>/<order>', methods=['GET'])
def order(category_id,order): 
    return orderChange(category_id,order)

@app.route('/search', methods=['POST'])
def search(): 
    if request.method == 'POST':
        content = request.form['content']
    return find_notes(content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6664, debug=False) 
