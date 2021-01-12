from flask import Flask, render_template
from flask_restful import Api
from urllib.request import urlopen
from PIL import Image
import numpy as np
import cv2
from resources.processimage import Base64Endpoint, MultiPartEndpoint, ImageUrlEndpoint
import logging


app = Flask(__name__)
api = Api(app)

api.add_resource(ImageUrlEndpoint, '/magic/imageurl')
api.add_resource(Base64Endpoint, '/magic/base64')
api.add_resource(MultiPartEndpoint, '/magic/multipart')

### Uncomment to run wrk benchmark
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

# Just to confirm visually
@app.route('/', methods=['GET'])
def home():
    image_url = 'https://images.dog.ceo/breeds/leonberg/n02111129_2088.jpg'
    save_file_path = "static/images/bw.png"

    # Transformation using Pillow
    # transformer = ProcessImageEndpoint()
    # transformed_image = transformer.transform_image(image_url)
    # transformed_image.save(save_file_path, "PNG")
    # return render_template('index.html', image_url = [image_url, save_file_path])

    # Transformation using OpenCV
    url_response = urlopen(image_url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    originalImage = cv2.imdecode(img_array, -1)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(save_file_path, blackAndWhiteImage)
    return render_template('index.html', image_url=[image_url, save_file_path])


app.run()
