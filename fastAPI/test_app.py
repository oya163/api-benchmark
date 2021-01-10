import requests
from fastapi.testclient import TestClient
from fastAPI.archive.fastapiServer import app

client = TestClient(app)

url = "http://127.0.0.1:8000/"

payload = "{\"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"}"
headers = {
    'Content-Type': 'application/json'
}


def test_index():
    # response = client.post(url, headers=headers, data=payload, stream=True)
    response = requests.request("GET", url)
    assert response.json() == {"Hello": "LibraX"}
    assert response.status_code == 200


def test_magic():
    # response = client.post(url, headers=headers, data=payload, stream=True)
    response = requests.request("POST", url+"magic/", headers=headers, data=payload, stream=True)
    assert response.status_code == 200