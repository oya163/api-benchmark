import base64
from PIL import Image
import io, os, json
import aiohttp
import asyncio
from multidict import CIMultiDict

url = "http://0.0.0.0:8080/magic/imageurl"
base64_url = "http://0.0.0.0:8080/magic/base64"
multipart_url = "http://0.0.0.0:8080/magic/multipart"

# payload = {'image_url': """https://i.ibb.co/ZYW3VTp/brown-brim.png"""}
payload="{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
headers = {
    'Content-Type': 'application/json'
}

file_path = '../flaskAPI/static/images/3.jpeg'
filename = os.path.basename(file_path)
ENCODING = 'utf-8'

image_file = open(file_path, "rb")
encoded_string = base64.b64encode(image_file.read()).decode(ENCODING)
base64_files = json.dumps({
    'filename': filename,
    'encoded_image': encoded_string
})
image_file.seek(0)

# For image url
async def fetch_imageurl_results():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            response = await resp.json()
            if resp.status == 200:
                filename = response['filename']
                image = base64.b64decode(response['encoded_img'])
                img = Image.open(io.BytesIO(image))
                img.save(filename)
                print("Image saved after POST from image_url")
            else:
                print(resp)



# For image payload + base64 encoding
async def fetch_base64_results():
    async with aiohttp.ClientSession() as session:
        async with session.post(base64_url, data=base64_files, headers=headers) as resp:
            response = await resp.json()
            if resp.status == 200:
                filename = response['filename']
                image = base64.b64decode(response['encoded_img'])
                img = Image.open(io.BytesIO(image))
                img.save('bw_'+filename)
                print("Image saved after POST in base 64")
            else:
                print(resp)

# Multi-part form data
files = {'filename': filename, 'image':image_file, 'content-type': 'multipart/form-data'}

# For image payload + multipart/form
async def fetch_multipart_results():
    async with aiohttp.ClientSession() as session:
        async with session.post(multipart_url, data=files) as resp:
            response = await resp.read()
            if resp.status == 200:
                data = CIMultiDict(resp.headers)
                filename = data['filename']
                # image = base64.b64decode(response)
                img = Image.open(io.BytesIO(response))
                img.save('bw_multipart'+filename)
                print("Image saved after POST in multipart")
            else:
                print(resp)


loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_imageurl_results())
loop.run_until_complete(fetch_base64_results())
loop.run_until_complete(fetch_multipart_results())
