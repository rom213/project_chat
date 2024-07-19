import os
from io import BytesIO
from PIL import Image
from flask import Flask, jsonify, request
from config import config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import base64


app = Flask(__name__)
app.config['SECRET_KEY'] = config['development'].SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{config['development'].MYSQL_USER}:{config['development'].MYSQL_PASSWORD}@{config['development'].MYSQL_HOST}/{config['development'].MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'src/uploads/'

db = SQLAlchemy(app)

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    rfid_code = db.Column(db.String(55), nullable=False)

with app.app_context():
    db.create_all()

led_cosina_status = False
led_cuarto_status = False
take_photo = False

@app.route('/toggle', methods=['POST'])
def toggle():
    global led_status, take_photo
    data = request.get_json()
    if "led_on" in data:
        led_status = not led_status
    if "take_photo" in data:
        take_photo = not take_photo
    return jsonify({"take_photo": take_photo, "led_on": led_status})

@app.route('/status', methods=['GET'])
def status():
    global take_photo, led_status
    return jsonify({"take_photo": take_photo, "led_on": led_status})


@app.route('/upload_image', methods=['POST'])
def upload_img():
    if 'photo' not in request.files or 'RFID-Code' not in request.form:
        return jsonify({'message': 'Missing image file or RFID code'}), 404

    image_file = request.files['photo']
    card_code = request.form.get('RFID-Code')
    print(card_code)
    
    if image_file and card_code:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        try:
            # Leer la imagen en base64 y decodificarla
            base64_image = image_file.read()
            decoded_image = base64.b64decode(base64_image)
            
            # Convertir la imagen decodificada a un objeto de imagen PIL
            image = Image.open(BytesIO(decoded_image))
            
            # Crear un nombre de archivo seguro y único
            filename = secure_filename(datetime.now().strftime("%Y%m%d%H%M%S%f") + '.jpg')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Guardar la imagen en formato jpg
            image.save(filepath, 'JPEG')

            new_image = ImageModel(image_path=filepath,rfid_code=card_code)
            db.session.add(new_image)
            db.session.commit()

            return jsonify({'message': 'Image uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'message': f'Error saving image: {e}'}), 500

    return jsonify({'message': 'Missing image file or RFID code'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
