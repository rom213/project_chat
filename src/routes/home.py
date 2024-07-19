from flask import Blueprint, jsonify, request
import os
from io import BytesIO
from PIL import Image
from config import config
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import base64

home_bp = Blueprint('users', __name__)



led_cosina_status = False
led_cuarto_status = False
led_sala_status = False
led_frente_status = False
take_photo = False

db = SQLAlchemy(home_bp)

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    rfid_code = db.Column(db.String(55), nullable=False)
    
with home_bp.app_context():
    db.create_all()



@home_bp.route('/toggle', methods=['POST'])
def toggle():
    global led_cosina_status, take_photo
    data = request.get_json()
    if "led_on" in data:
        led_cosina_status = not led_cosina_status
    if "take_photo" in data:
        take_photo = not take_photo
    return jsonify({"take_photo": take_photo, "led_on": led_cosina_status})

@home_bp.route('/status', methods=['GET'])
def status():
    global take_photo, led_cosina_status
    return jsonify({"take_photo": take_photo, "led_cosina": led_cosina_status})

@home_bp.route('/upload_image', methods=['POST'])
def upload_img():
    if 'photo' not in request.files or 'RFID-Code' not in request.form:
        return jsonify({'message': 'Missing image file or RFID code'}), 404

    image_file = request.files['photo']
    card_code = request.form.get('RFID-Code')
    print(card_code)
    
    if image_file and card_code:
        if not os.path.exists(home_bp.config['UPLOAD_FOLDER']):
            os.makedirs(home_bp.config['UPLOAD_FOLDER'])

        try:
            # Leer la imagen en base64 y decodificarla
            base64_image = image_file.read()
            decoded_image = base64.b64decode(base64_image)
            
            # Convertir la imagen decodificada a un objeto de imagen PIL
            image = Image.open(BytesIO(decoded_image))
            
            # Crear un nombre de archivo seguro y único
            filename = secure_filename(datetime.now().strftime("%Y%m%d%H%M%S%f") + '.jpg')
            filepath = os.path.join(home_bp.config['UPLOAD_FOLDER'], filename)
            
            # Guardar la imagen en formato jpg
            image.save(filepath, 'JPEG')

            new_image = ImageModel(image_path=filepath,rfid_code=card_code)
            db.session.add(new_image)
            db.session.commit()

            return jsonify({'message': 'Image uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'message': f'Error saving image: {e}'}), 500

    return jsonify({'message': 'Missing image file or RFID code'}), 404
