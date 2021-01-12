"""
    Description:
    Unittest for Flask REST API endpoints
"""

import os, requests, base64, json

url = "http://127.0.0.1:5000/magic/imageurl"
base64_url = "http://127.0.0.1:5000/magic/base64"
multipart_url = "http://127.0.0.1:5000/magic/multipart"

# Payloads for imageurl endpoints
payload = "{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
headers = {
    'Content-Type': 'application/json'
}

file_path = './static/images/3.jpeg'
filename = os.path.basename(file_path)
ENCODING = 'utf-8'

# Base-64 encoding
image_file = open(file_path, "rb")
encoded_string = base64.b64encode(image_file.read()).decode(ENCODING)
base64_files = json.dumps({
    'filename': filename,
    'image': encoded_string
})

# Take the pointer to the beginning
image_file.seek(0)

# Multi-part form data
multipart_files = {'image': (filename, image_file, 'multipart/form-data')}

"""
    Testing Image URL endpoint
"""


def test_imageurl():
    response = requests.request("POST", url=url, data=payload, headers=headers, stream=True)
    assert response.status_code == 200


"""
    Testing Base64 Image endpoint
"""


def test_base64():
    response = requests.request("POST", url=base64_url, data=base64_files, headers=headers, stream=True)
    assert response.status_code == 200
    assert response.json()['filename'] == filename


"""
    Testing Multipart/Image form endpoint
"""


def test_multipart():
    response = requests.request("POST", url=multipart_url, files=multipart_files)
    assert response.status_code == 200
    assert response.headers['content-disposition'].split()[-1].split('=')[-1] == filename
