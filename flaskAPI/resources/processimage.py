from flask_restful import Resource, reqparse, HTTPException
from flask import send_file, Response
from io import BytesIO
import base64
from urllib.request import urlopen
from PIL import Image
import flask
import requests
from requests_toolbelt import MultipartEncoder
import werkzeug


"""
    This API consumes image url
"""
class ImageUrlEndpoint(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image_url", type=str)
        self.req_parser = parser

    def get(self):
        image_url = "https://i.ibb.co/ZYW3VTp/brown-brim.png"
        transformed_image = Image.open(urlopen(image_url)).convert('1')
        img_byte_arr = BytesIO()
        transformed_image.save(img_byte_arr, format='JPEG')
        encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
        return flask.jsonify({
            'filename': 'bw.jpeg',
            'encoded_img': encoded_img}
        )

    # base64 encoding
    def post(self):
        image_url = self.req_parser.parse_args(strict=True).get("image_url", None)
        if image_url:
            encoded_img = Image.open(urlopen(image_url)).convert('1')
            buffered = BytesIO()
            encoded_img.save(buffered, format="JPEG")
            encoded_img = base64.b64encode(buffered.getvalue()).decode('ascii')
            return flask.jsonify({
                'filename': 'bw.jpeg',
                'encoded_img': buffered.getvalue()
            })
        else:
            return "Error: Please send an image", 500

    # multipart form response
    def post(self):
        image_url = self.req_parser.parse_args(strict=True).get("image_url", None)
        if image_url:
            resp = requests.get(image_url)
            encoded_img = Image.open(BytesIO(resp.content)).convert('1')
            buffered = BytesIO()
            encoded_img.save(buffered, format="JPEG")
            buffered.seek(0)
            return send_file(buffered,
                             attachment_filename='bw.jpeg',
                             as_attachment=True,
                             mimetype='image/jpeg')
        else:
            return "Error: Please send an image", 500

"""
    This API consumes base64 encoded image file
"""
class Base64Endpoint(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=str, location='json')
        parser.add_argument("filename", type=str, location='json')
        self.req_parser = parser

    # Input is base64 encoded image
    def post(self):
        image = self.req_parser.parse_args(strict=True).get("image", None)
        filename = self.req_parser.parse_args(strict=True).get("filename", None)
        if image:
            decoded_image = base64.b64decode(image)
            blackAndWhite_img = Image.open(BytesIO(decoded_image)).convert('1')
            buffered = BytesIO()
            blackAndWhite_img.save(buffered, format="JPEG")
            print("Image converted")
            buffered.seek(0)
            encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return flask.jsonify({
                'filename': filename,
                'encoded_img': encoded_img
            })
        else:
            return "Error: Please send an image", 500

"""
    This API consumes multipart/form image file
"""
class MultiPartEndpoint(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
        self.req_parser = parser

    # Input is multipart/form image data
    def post(self):
        image = self.req_parser.parse_args(strict=True).get("image", None)
        if image:
            filename = image.filename
            blackAndWhite_img = Image.open(BytesIO(image.stream.read())).convert('1')
            buffered = BytesIO()
            blackAndWhite_img.save(buffered, format="JPEG")
            print("Image converted")
            buffered.seek(0)
            return send_file(buffered,
                             attachment_filename=filename,
                             as_attachment=True,
                             mimetype='image/jpeg')
        else:
            return "Error: Please send an image", 500