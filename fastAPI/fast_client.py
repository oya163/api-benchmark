import requests
import base64
from PIL import Image
import io

url = "http://127.0.0.1:8000/magic"
payload="{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
headers = {
  'Content-Type': 'application/json'
}

with requests.request("GET", url) as r:
    if r.status_code == 200:
        response = r.json()
        filename = response['filename']
        image = base64.b64decode(response['encoded_img'])
        img = Image.open(io.BytesIO(image))
        img.save(filename)
        print("Image saved after GET")
    else:
        print(r)

with requests.request("POST", url, data=payload, headers=headers, stream=True) as r:
    if r.status_code == 200:
        response = r.json()
        filename = response['filename']
        image = base64.b64decode(response['encoded_img'])
        img = Image.open(io.BytesIO(image))
        img.save(filename)
        print("Image saved after POST")
    else:
        print(r)


