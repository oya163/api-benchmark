"""
    Description: FastAPI framework
    These APIs consumes image_url or image file
    and returns its corresponding black/white image

    Author: Oyesh Mann Singh
    Date: 01/11/2021
"""

from io import BytesIO
import base64
from urllib.request import urlopen
from urllib.error import HTTPError
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, Response
import uvicorn
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Body
import logging
import json


class ImageModel(BaseModel):
    image_url: str


class OtherException(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.error_code = code


app = FastAPI()

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@app.exception_handler(OtherException)
async def unicorn_exception_handler(request: Request, exc: OtherException):
    return JSONResponse(
        status_code=exc.error_code,
        content={"message": "ERROR: {}".format(exc.name)},
    )


@app.get("/")
def index():
    return {"Hello": "LibraX"}

# GET method
# Returns black and white of fixed image
@app.get("/magic/imageurl")
def get():
    image_url = "https://i.ibb.co/ZYW3VTp/brown-brim.png"
    encoded_img = Image.open(urlopen(image_url)).convert('1')
    buffered = BytesIO()
    encoded_img.save(buffered, format="JPEG")
    encoded_img = base64.b64encode(buffered.getvalue())
    return {
        'filename': 'bw.jpeg',
        'encoded_img': encoded_img
    }


# Retrieves image from given image_url
# Return its corresponding b/w image
@app.post("/magic/imageurl")
def magic_url(image: ImageModel):
    image_url = image.image_url
    if image_url:
        try:
            image_url = urlopen(image_url)
        except HTTPError as e:
            if e.code == 404:
                raise HTTPException(status_code=404, detail="URL not found")
            else:
                raise OtherException(name="Error by Oyesh", code=e.code)

        encoded_img = Image.open(image_url).convert('1')
        buffered = BytesIO()
        encoded_img.save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue())
        return {
            'filename': 'bw.jpeg',
            'encoded_img': encoded_img
        }
    else:
        return "Error: Payload empty", 500


# Consumes base64 encoded image
# Returns black/white base64 encoded image
@app.post("/magic/base64")
async def magic_base64(image: str = Body(...)):
    if image:
        image_json = json.loads(image)
        filename = image_json['filename']
        encoded_image = base64.b64decode(image_json['image'])
        blackAndWhite_img = Image.open(BytesIO(encoded_image)).convert('1')
        buffered = BytesIO()
        blackAndWhite_img.save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return {
            'filename': filename,
            'encoded_img': encoded_img
        }
    else:
        return "Error: Please send an image", 500


# Consumes image file as multipart/form-data
# Returns black/white image
@app.post("/magic/multipart")
async def magic_multipart(image: UploadFile = File(...)):
    if image:
        filename = image.filename
        image = await image.read()
        # blackAndWhite_img = Image.open(image).convert('1')
        blackAndWhite_img = Image.open(BytesIO(image)).convert('1')
        buffered = BytesIO()
        blackAndWhite_img.save(buffered, format="JPEG")
        buffered.seek(0)
        return Response(content=buffered.getvalue(), media_type='image/jpeg', headers={'filename': filename})
    else:
        return "Error: Please send an image", 500


if __name__ == "__main__":
    uvicorn.run("app:app")
