import requests
import json
import pytest

def test_update_book_without_login():
    with open('./Test_cases/json_data/add_book.json','r') as f:
            json_input=f.read()
            request_json=json.loads(json_input)
    
    url="http://127.0.0.1:5000/update_book"
    response=requests.post(url,request_json)
    assert response.status_code==401
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'






def test_update_book_with_login_bookID_exist():

    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'

    
    
    ############# if book ID exist #######################  
      
    with open('./Test_cases/json_data/update.json','r') as f:
            json_input=f.read()
            request_json=json.loads(json_input)
            request_json=json_input
    
    url="http://127.0.0.1:5000/update_book"
    response=s.post(url,request_json)
    assert response.status_code==201
    assert response.headers.get('Content-Type')=='application/json'

def test_update_book_with_login_if_book_id_not_exist():

    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'


    ############ if book  ID is not exist #######################  
        
    url="http://127.0.0.1:5000/update_book"
    response=s.post(url,request_json)
    assert response.status_code==409
    assert response.headers.get('Content-Type')=='application/json'

