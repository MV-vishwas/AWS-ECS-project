import requests
import json
import pytest

def test_add_book_without_login():
    with open('./Test_cases/json_data/add_book.json','r') as f:
            json_input=f.read()
            request_json=json.loads(json_input)
    
    url="http://127.0.0.1:5000/add_book"
    response=requests.post(url,request_json)
    assert response.status_code==401
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'




def test_add_book_with_login_book_is_already_present():
    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'

    
    
    ############# if book is already exist #######################  
      
    with open('./Test_cases/json_data/add_book.json','r') as f:
            json_input=f.read()
            request_json=json.loads(json_input)
    url="http://127.0.0.1:5000/add_book"
    response=s.post(url,request_json)
    assert response.status_code==409
    assert response.headers.get('Content-Type')=='application/json'

    

def test_add_book_with_login_book_is_not_present():
    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'

    ############# if book is not  exist #######################      
    # url="http://127.0.0.1:5000/add_book"
    # response=s.post(url,request_json)
    # assert response.status_code==201
    # assert response.headers.get('Content-Type')=='application/json'
