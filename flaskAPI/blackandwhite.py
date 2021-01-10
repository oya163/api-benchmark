from io import BytesIO
import base64
from urllib.request import urlopen
from PIL import Image
import json

def convert_bw():
    encoded_img = Image.open(urlopen("https://i.ibb.co/ZYW3VTp/brown-brim.png")).convert('1')
    buffered = BytesIO()
    encoded_img.save(buffered, format="JPEG")
    encoded_img = base64.b64encode(buffered.getvalue()).decode('ascii')
    json.dumps({
                    'filename': 'bw.jpeg',
                    'encoded_img': encoded_img}
                )

convert_bw()