from flask import Flask, request, send_file
from wand.image import Image

app = Flask(__name__,  static_url_path='/')

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/crop', methods=['POST'])
def crop_image():
    if 'image' not in request.files:
        return 'No file provided', 400

    image_file = request.files['image']

    with Image(file=image_file) as img:
        img.trim()
        img.save(filename='cropped_image.jpg')

    return send_file('cropped_image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)