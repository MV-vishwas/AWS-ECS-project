import requests
import pytest
import json
def test_get_book_id_exist():
    url='http://127.0.0.1:5000/get_book/123'
    response=requests.get(url)
    assert response.status_code==200
    assert response.headers.get('Content-Type')=='application/json'

def test_get_book_book_id_not_exist():
    url='http://127.0.0.1:5000/get_book/54323'
    response=requests.get(url)
    assert response.status_code==404
    assert response.headers.get('Content-Type')=='application/json'