"""
    Description: aioHTTP API framework
    These APIs consumes image_url or image file
    and returns its corresponding black/white image

    Author: Oyesh Mann Singh
    Date: 01/11/2021
"""

from aiohttp import web
from io import BytesIO
import base64
from PIL import Image
import aiohttp
import json


# POST method
# Consumes image_url and retrieves it
# Returns black/white image
async def url_post(request):
    # data = await request.post()
    # image_url = data.get('image_url')

    ###################################################
    ## REQUIRED for wrk performance checkup  ##########
    ###################################################
    data = await request.read()
    data = json.loads(data)
    image_url = data['image_url']

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            image_data = await resp.read()
            transformed_image = Image.open(BytesIO(image_data)).convert('1')
            img_byte_arr = BytesIO()
            transformed_image.save(img_byte_arr, format='JPEG')
            encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
            return web.json_response({
                'filename': 'bw.jpeg',
                'encoded_img': encoded_img
            })


# POST method
# Consumes base64 encoded image
# Returns black/white image
async def base64_post(request):
    # data = await request.post()
    # filename = data.get('filename')
    # image = data.get('encoded_image')

    ###################################################
    ## REQUIRED for wrk performance checkup  ##########
    ###################################################
    data = await request.read()
    data = json.loads(data)
    filename = data['filename']
    image = data['encoded_image']

    image = base64.b64decode(image)
    blackAndWhite_img = Image.open(BytesIO(image)).convert('1')
    buffered = BytesIO()
    blackAndWhite_img.save(buffered, format="JPEG")
    buffered.seek(0)
    encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return web.json_response({
        'filename': filename,
        'encoded_img': encoded_img
    })


# POST method
# Consumes image file as multipart/form-data
# Returns black/white image
async def multipart_post(request):
    # data = await request.post()
    # image_url = data.get('image_url')

    ###################################################
    ## REQUIRED for wrk performance checkup  ##########
    ###################################################

    data = await request.post()
    filename = data['filename']
    image = data['image']

    decoded_image = image.file.read()
    blackAndWhite_img = Image.open(BytesIO(decoded_image)).convert('1')
    buffered = BytesIO()
    blackAndWhite_img.save(buffered, format="JPEG")
    buffered.seek(0)
    return web.Response(
        body=buffered.getvalue(),
        headers={
            'filename': filename
        }
    )


app = web.Application()
app.router.add_post('/magic/imageurl', url_post)
app.router.add_post('/magic/base64', base64_post)
app.router.add_post('/magic/multipart', multipart_post)

web.run_app(app)
