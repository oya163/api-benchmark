import requests
import base64
from PIL import Image
import os, io, json
from fastapi.testclient import TestClient

from fastAPI.app import app

client = TestClient(app)

url = "http://127.0.0.1:8000/magic/imageurl"
base64_url = "http://127.0.0.1:8000/magic/base64"
multipart_url = "http://127.0.0.1:8000/magic/multipart"

# Payloads for imageurl endpoints
payload = "{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"

headers = {
    'Content-Type': 'application/json'
}

file_path = '../flaskAPI/static/images/3.jpeg'
filename = os.path.basename(file_path)
ENCODING = 'utf-8'

# Base-64 encoding
image_file = open(file_path, "rb")
encoded_string = base64.b64encode(image_file.read()).decode(ENCODING)
base64_files = json.dumps({
    'filename': filename,
    'encoded_image': encoded_string
})

# Take the pointer to the beginning
image_file.seek(0)

# Multi-part form data
multipart_files = {'image': (filename, image_file, 'multipart/form-data')}

# Image url testing
with requests.request("POST", url=url, data=payload, headers=headers, stream=True) as r:
    if r.status_code == 200:
        # To handle the response object sent using flask jsonify
        response = r.json()
        filename = response['filename']
        image = base64.b64decode(response['encoded_img'])
        img = Image.open(io.BytesIO(image))
        img.save(filename)

        # To handle the Response object sent using send_file
        # img = Image.open(io.BytesIO(r.content))
        # img.save('bw.jpeg')
        print("Image received from /magic/imageurl")
    else:
        print(r)

# Base64 client testing
with requests.request("POST", url=base64_url, json=base64_files, headers=headers) as r:
    if r.status_code == 200:
        response = r.json()
        filename = 'bw_'+response['filename']

        image = base64.b64decode(response['encoded_img'])
        img = Image.open(io.BytesIO(image))
        img.save(filename)
        print("Image received from /magic/base64")
    else:
        print(r)


# Multipart client testing
with requests.request("POST", url=multipart_url, files=multipart_files) as r:
    if r.status_code == 200:
        filename = r.headers['filename']
        img = Image.open(io.BytesIO(r.content))
        img.save('bw_'+filename)
        print("Image received from /magic/multipart_url")
    else:
        print(r)


