import pytest
from fastapi.testclient import TestClient
from main import app
from db import models, db

client = TestClient(app)

@pytest.fixture
def client_authorization_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuaWtoaWwiLCJleHAiOjE3MDc3NDIzMzd9.A4T2RWEMrwj909A8AEy2Wel9O1cPTwJQW8tK0su_zpw"
    }

@pytest.fixture
def sign_up_client_info():
    return {
        "username": "nikhil",
        "password": "123",
        "role": "client"
    }

@pytest.fixture
def sign_up_ops_info():
    return {
        "username": "admin",
        "password": "admin",
        "role": "ops"
    }

def test_user_creation(sign_up_client_info):
    response = client.post('/signup', json=sign_up_client_info)
    assert response.status_code == 201

def test_get_files(client_authorization_headers):
    session = db.SessionLocal()
    try:
        client_user = models.UserModal(username="nikhil", password="123", role="client")
        session.add(client_user)
        test_file = models.FileModal(filename="test_file.docx", contents=b"Test file content")
        session.add(test_file)
        session.commit()
    finally:
        session.close()

    response = client.get("/files", headers=client_authorization_headers)
    assert response.status_code == 201
    assert response.json() == [{"name": "test_file.docx", "download_link": "/download-file/1"}]


def test_download_file(client_authorization_headers):
    session = db.SessionLocal()
    try:
        test_file = models.FileModal(filename="test_file.docx", contents=b"Test file content")
        session.add(test_file)
        session.commit()
    finally:
        session.close()

    response = client.get("/download-file/1", headers=client_authorization_headers)
    assert response.status_code == 200

    expected_content = b"Test file content"
    assert response.content == expected_content


def test_user_creation(sign_up_ops_info):
    response = client.post('/signup', json=sign_up_ops_info)
    assert response.status_code == 201

def test_user_login():
    response = client.post('/login', json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert response is not None
    assert "access_token" in response.json()
    assert response.json()["access_token"] != ""
