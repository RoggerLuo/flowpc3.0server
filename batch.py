from dao.classify import classify,unclassify
from dao.category import query_categories,create_category,modify_category,delete_category,orderChange,colorChange
from dao.note import create_note,modify_note,delete_note
from dao.notes import query_notes,find_notes
import json
from urllib import request, parse
from urllib.parse import urlencode

import requests

# base_url="http://rorrc.3322.org:32818/v1/note"

# payload ={"content": "note.content测试"}
# response = requests.post(base_url, data=json.dumps(payload).encode('utf-8'),headers={'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvZ2VyIiwiaWF0IjoxNTUxNjIwNTQ1LCJleHAiOjE1NTE5ODA1NDV9.6ACHXjYMOUIzGNx1xhC3fLyd8NcqlMcLeNB_9LtdY1A'})

# print(response.text) #TEXT/HTML
# print(response.status_code, response.reason) #HTTP



if __name__ == '__main__':
    # categoryId = request.args.get('categoryId')
    pageSize = 9999 #9999
    start = 1


    def post(content):
        apiAddress = 'http://rorrc.3322.org:32818/v1'
        # apiAddress = 'http://localhost:8999/v1'

        url = apiAddress + '/note'
        data = urlencode({'content': content}) #json.dumps
        data = data.encode('utf-8')


        req = request.Request(url)  # 'http://localhost:9911'
        req.add_header('content-type', 'application/x-www-form-urlencoded')
        # req.add_header('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvZ2VyIiwiaWF0IjoxNTUxNjIwNTQ1LCJleHAiOjE1NTE5ODA1NDV9.6ACHXjYMOUIzGNx1xhC3fLyd8NcqlMcLeNB_9LtdY1A')
        req.add_header('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvZ2VyIiwiaWF0IjoxNTUyMTAzODgwfQ.NM93AnkECfQamHyHF0wuFavYsh4n0PlY2g0dnDhnyvo')

        with request.urlopen(req, data=data) as f:
            # print('Status:', f.status, f.reason)
            for k, v in f.getheaders():
                print('%s: %s' % (k, v))
            #print('Data:', f.read().decode('utf-8'))
            value = f.read().decode('utf-8')
            print('------------')
            print(value)
            value=json.loads(value)
            print(value)


    # post('123')

    data = query_notes(None,pageSize,start)
    data = json.loads(data)
    ind=1
    for item in data['data']:
        print(ind)
        ind+=1
        post(item['content'])
        print(item['content'])







