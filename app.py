from flask import Flask, request
import flask_cors
import jieba
import json
app = Flask(__name__, static_folder='static')
flask_cors.CORS(app, supports_credentials=True)

@app.route('/wordscut', methods=['POST'])
def wordscut(): 
    if request.method == 'POST':
        content = request.form['content']
        words_list = jieba.lcut_for_search(content)
    return json.dumps(words_list,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6664, debug=False) 
