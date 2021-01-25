import requests
import json
import pytest




def test_get_books_without_login():      
    with open('./Test_cases/json_data/filter.json','r') as f:
            json_input=f.read()
            request_json=json.loads(json_input)
    url="http://127.0.0.1:5000/get_books"
    response=requests.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='application/json'

    


def test_get_books_with_login():      
    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'
    
    with open('./Test_cases/json_data/filter.json','r') as f:
            json_input=f.read()
            request_json=json.loads(json_input)
    url="http://127.0.0.1:5000/get_books"
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='application/json'

