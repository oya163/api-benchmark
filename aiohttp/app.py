from aiohttp import web
from io import BytesIO
import base64
from PIL import Image
import aiohttp
import multidict
import json

# Post for image url
# async def post(request):
#     # data = await request.post()
#     # image_url = data.get('image_url')
#
#     ###################################################
#     ## REQUIRED for wrk performance checkup  ##########
#     ###################################################
#     data = await request.read()
#     data = json.loads(data)
#     image_url = data['image_url']
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(image_url) as resp:
#             image_data = await resp.read()
#             transformed_image = Image.open(BytesIO(image_data)).convert('1')
#             img_byte_arr = BytesIO()
#             transformed_image.save(img_byte_arr, format='JPEG')
#             encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
#             return web.json_response({
#                 'filename': 'bw.jpeg',
#                 'encoded_img': encoded_img
#             })

# Post for image payload + base64 encoding
async def post(request):
    # data = await request.post()
    # image_url = data.get('image_url')

    ###################################################
    ## REQUIRED for wrk performance checkup  ##########
    ###################################################
    data = await request.read()
    data = json.loads(data)
    filename = data['filename']
    image = data['image']

    decoded_image = base64.b64decode(image)
    blackAndWhite_img = Image.open(BytesIO(decoded_image)).convert('1')
    buffered = BytesIO()
    blackAndWhite_img.save(buffered, format="JPEG")
    print("Image converted")
    buffered.seek(0)
    encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return web.json_response({
                    'filename': filename,
                    'encoded_img': encoded_img
                })


# Post for image payload + multipart/form
# async def post(request):
#     # data = await request.post()
#     # image_url = data.get('image_url')
#
#     ###################################################
#     ## REQUIRED for wrk performance checkup  ##########
#     ###################################################
#
#     data = await request.post()
#
#     filename = data['filename']
#     image = data['image']
#     decoded_image = image.file.read()
#     blackAndWhite_img = Image.open(BytesIO(decoded_image)).convert('1')
#     buffered = BytesIO()
#     blackAndWhite_img.save(buffered, format="JPEG")
#     print("Image converted")
#     buffered.seek(0)
#     # encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
#     return web.Response(
#         body=buffered.getvalue(),
#         headers={
#             'filename': filename
#         }
#     )

app = web.Application()
app.router.add_post('/magic', post)


web.run_app(app)