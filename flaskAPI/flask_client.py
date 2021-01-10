import requests
import base64
from PIL import Image
import io, json
from flask import Request

url = "http://127.0.0.1:5000/magic"
payload="{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
headers = {
  'Content-Type': 'application/json'
}

# with requests.request("GET", url) as r:
#     if r.status_code == 200:
#         response = r.json()
#         filename = response['filename']
#         image = base64.b64decode(response['encoded_img'])
#         img = Image.open(io.BytesIO(image))
#         img.save(filename)
#         print("Image saved after GET")
#     else:
#         print(r)


# with requests.request("POST", url, data=payload, headers=headers, stream=True) as r:
#     if r.status_code == 200:
#         # To handle the response object sent using flask jsonify
#         # response = r.json()
#         # filename = response['filename']
#         # image = base64.b64decode(response['encoded_img'])
#         # img = Image.open(io.BytesIO(image))
#         # img.save(filename)
#
#         # To handle the Response object sent using send_file
#         img = Image.open(io.BytesIO(r.content))
#         img.save('bw.jpeg')
#         print("Image saved after POST")
#     else:
#         print(r)


response = requests.get("https://i.ibb.co/ZYW3VTp/brown-brim.png")
print(response.content)
