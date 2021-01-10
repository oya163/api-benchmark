import base64
from PIL import Image
import io
import aiohttp
import asyncio

url = "http://0.0.0.0:8080/magic"

payload = {'image_url': """https://i.ibb.co/ZYW3VTp/brown-brim.png"""}
# payload="{\n    \"image_url\": \"https://i.ibb.co/ZYW3VTp/brown-brim.png\"\n}"
headers = {
    'Content-Type': 'application/json'
}


async def fetch_results():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            response = await resp.json()
            if resp.status == 200:
                filename = response['filename']
                image = base64.b64decode(response['encoded_img'])
                img = Image.open(io.BytesIO(image))
                img.save(filename)
                print("Image saved after POST")
            else:
                print(resp)


loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_results())
