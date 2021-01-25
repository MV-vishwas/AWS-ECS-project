import requests
import pytest
import json

def test_add_favourite_without_login():
    url='http://127.0.0.1:5000/add_favourite/345/demo@gmail.com'
    response=requests.get(url)
    assert response.status_code==401
    # print(response.headers)
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'



def test_add_favourite_with_login_and_bookID_not_exist():

    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'
    
    ###############if book ID not exist'#########

    url='http://127.0.0.1:5000/add_favourite/43567543/demo@gmail.com'
    response=s.get(url)
    assert response.status_code==404
    assert response.headers.get('Content-Type')=='application/json'
    
    

def test_add_favourite_with_login_book_already_in_fav_list():
    ##### if book ID is already in fav list #####
    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'
    
    ###############if book ID not exist'#########

    url='http://127.0.0.1:5000/add_favourite/123/demo@gmail.com'
    response=s.get(url)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='application/json'
    

def test_add_favourite_with_login_book_ID_is_not_in_fav_list():
    ##### if book ID is not in fav list #####
    s=requests.session()
    url='http://127.0.0.1:5000/check'
    with open('./Test_cases/json_data/login_data.json','r') as f:
        json_input=f.read()
        request_json=json.loads(json_input)
    response=s.post(url,request_json)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='text/html; charset=utf-8'

    url='http://127.0.0.1:5000/add_favourite/123/demo@gmail.com'
    response=s.get(url)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='application/json'


