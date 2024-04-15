import base64
from flask import Flask, request
from wand.image import Image
from io import BytesIO

app = Flask(__name__, static_url_path='/')

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

# acceptable mime types
mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']

def remove_white_background(image_file):
    with Image(file=image_file) as img:
        img.background_color = img.transparent_color
        img.alpha_channel = 'remove'
        img.format = 'png'
        
        # Save the image to BytesIO object
        cropped_image = BytesIO()
        img.save(cropped_image)
        
        # Encode the image to base64
        base64_string_str = base64.b64encode(cropped_image.getvalue()).decode()
        
        return "<img src='data:image/png;base64,{}'>".format(base64_string_str)

def base64_image(file):
    return base64.b64encode(file.getvalue()).decode() 

@app.route('/crop', methods=['POST'])
def crop_image():
    if 'image' not in request.files:
        return 'No file provided', 400

    image_file = request.files['image']

    wat = request.form['format']
    print(wat, wat)

    with Image(file=image_file) as img:
        img.trim()
        cropped_image = BytesIO()
        img.save(cropped_image)
        base64_string_str = base64_image(cropped_image)
        # base64_string_str = base64.b64encode(cropped_image.getvalue()).decode()
        # match the mime type for the uploaded image, using mime_types array
        mime_type = image_file.content_type

        print('mime:', mime_type)

        # return "<img src='data:image/{};base64,{}'>".format(img.format.lower(), base64_string_str)
        return "<img src='data:image/jpeg;base64,{}'>".format(base64_string_str)



if __name__ == '__main__':
    app.run(debug=True)
