from flask_restful import Resource, reqparse, HTTPException
from flask import send_file, Response
from io import BytesIO
import base64
from urllib.request import urlopen
from PIL import Image
import flask
import requests
from requests_toolbelt import MultipartEncoder

# Write try catch

class ProcessImageEndpoint(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        # parser.add_argument("image", type=werkzeug.datastructures.FileStorage, location='files')
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

    def transform_image(self, image_file):
        return Image.open(urlopen(image_file)).convert('1')

    # def post(self):
    #     image_url = self.req_parser.parse_args(strict=True).get("image_url", None)
    #     if image_url:
    #         encoded_img = Image.open(urlopen(image_url)).convert('1')
    #         buffered = BytesIO()
    #         encoded_img.save(buffered, format="JPEG")
    #         encoded_img = base64.b64encode(buffered.getvalue()).decode('ascii')
    #         return flask.jsonify({
    #             'filename': 'bw.jpeg',
    #             'encoded_img': buffered.getvalue()
    #         })
    #     else:
    #         return "Error: Please send an image", 500

    def post(self):
        image_url = self.req_parser.parse_args(strict=True).get("image_url", None)
        if image_url:
            # image_url = urlopen(image_url)
            # encoded_img = Image.open(urlopen(image_url)).convert('1')
            resp = requests.get(image_url)
            encoded_img = Image.open(BytesIO(resp.content)).convert('1')
            buffered = BytesIO()
            encoded_img.save(buffered, format="JPEG")
            buffered.seek(0)
            return send_file(buffered,
                             attachment_filename='bw.jpeg',
                             as_attachment=True,
                             mimetype='image/jpeg')
            # m = MultipartEncoder(
            #     fields={'filename': 'bw.jpeg',
            #             'encoded_img': buffered}
            # )
            # return Response(m.to_string(), mimetype=m.content_type)
        else:
            return "Error: Please send an image", 500

