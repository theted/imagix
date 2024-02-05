import base64
from flask import Flask, request, send_file
from wand.image import Image
from io import BytesIO

app = Flask(__name__,  static_url_path='/')

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route('/crop', methods=['POST'])
def crop_image():
    if 'image' not in request.files:
        return 'No file provided', 400

    image_file = request.files['image']

    with Image(file=image_file) as img:
        img.trim()
        cropped_image = BytesIO()
        img.save(cropped_image)
        base64_string_str = base64.b64encode(cropped_image.getvalue()).decode()
        return "<img src='data:image/jpeg;base64,{}'>".format(base64_string_str)

if __name__ == '__main__':
    app.run(debug=True)
