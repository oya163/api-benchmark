"""
    Description:
    Unittest for FastAPI endpoints
"""

import base64
from PIL import Image
import io, os, json
import aiohttp
import asyncio
import pytest
import pytest_asyncio
from multidict import CIMultiDict

url = "http://0.0.0.0:8080/magic/imageurl"
base64_url = "http://0.0.0.0:8080/magic/base64"
multipart_url = "http://0.0.0.0:8080/magic/multipart"

# payload = {'image_url': """https://i.ibb.co/ZYW3VTp/brown-brim.png"""}

# Payload for image_url endpoint
payload="{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
headers = {
    'Content-Type': 'application/json'
}

file_path = '../flaskAPI/static/images/3.jpeg'
filename = os.path.basename(file_path)
ENCODING = 'utf-8'
image_file = open(file_path, "rb")
encoded_string = base64.b64encode(image_file.read()).decode(ENCODING)

# Payload for base64 endpoint
base64_files = json.dumps({
    'filename': filename,
    'encoded_image': encoded_string
})

image_file.seek(0)

# Payload for multipart endpoint
files = {'filename': filename, 'image':image_file, 'content-type': 'multipart/form-data'}



"""
    Testing Image URL endpoint
"""
@pytest.mark.asyncio
async def test_imageurl():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            response = await resp.json()
            assert resp.status == 200

"""
    Testing Base64 Image endpoint
"""
@pytest.mark.asyncio
async def test_base64():
    async with aiohttp.ClientSession() as session:
        async with session.post(base64_url, data=base64_files, headers=headers) as resp:
            response = await resp.json()
            assert resp.status == 200
            if resp.status == 200:
                assert filename == response['filename']


"""
    Testing Multipart Image endpoint
"""
@pytest.mark.asyncio
async def test_multipart():
    async with aiohttp.ClientSession() as session:
        async with session.post(multipart_url, data=files) as resp:
            response = await resp.read()
            assert resp.status == 200
            if resp.status == 200:
                data = CIMultiDict(resp.headers)
                assert filename == data['filename']

