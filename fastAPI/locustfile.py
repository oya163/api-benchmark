import time
from locust import HttpUser, task
import json, os, base64

url = "/magic/imageurl"
base64_url = "/magic/base64"
multipart_url = "/magic/multipart"

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
    'image': encoded_string
})

# Take the pointer to the beginning
image_file.seek(0)

# Multi-part form data
multipart_files = {'image': (filename, image_file, 'image/jpeg')}


def _get_image_part(self, file_path, file_content_type='image/jpeg'):
    import os
    file_name = os.path.basename(file_path)
    file_content = open(file_path, 'rb')
    return file_name, file_content, file_content_type


class ImageUrlUser(HttpUser):
    @task
    def benchmark_imageurl(self):
        self.client.post(url=url, data=payload, headers=headers, stream=True)


class Base64User(HttpUser):
    @task
    def benchmark_base64(self):
        self.client.post(url=base64_url, json=base64_files, headers=headers)


class MultipartUser(HttpUser):
    @task
    def benchmark_multipart(self):
        file_path = '../flaskAPI/static/images/3.jpeg'
        filename = os.path.basename(file_path)
        image_file = open(file_path, "rb")
        multipart_files = {'image': (filename, image_file, 'multipart/form-data')}
        self.client.post(url=multipart_url, files=multipart_files)
        image_file.close()