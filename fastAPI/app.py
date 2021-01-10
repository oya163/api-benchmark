from io import BytesIO
import base64
from urllib.request import urlopen
from urllib.error import HTTPError
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image


class ImageModel(BaseModel):
    image_url: str


class OtherException(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.error_code = code


app = FastAPI()


@app.exception_handler(OtherException)
async def unicorn_exception_handler(request: Request, exc: OtherException):
    return JSONResponse(
        status_code=exc.error_code,
        content={"message": "ERROR: {}".format(exc.name)},
    )


@app.get("/")
def index():
    return {"Hello": "LibraX"}


@app.get("/magic/")
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


@app.post("/magic/")
def magic(image: ImageModel):
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

# if __name__ == "__main__":
#     uvicorn.run("app:app")
