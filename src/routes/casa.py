import os
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import base64

home_bp = Blueprint('casa', __name__)

db = SQLAlchemy()

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    rfid_code = db.Column(db.String(55), nullable=False)
    
""" @home_bp.before_app_first_request
def setup_db():
    db.init_app(current_app)
    with current_app.app_context():
        db.create_all() """

led_cosina_status = False
led_cuarto_status = False
led_sala_status = False
led_frente_status = False
take_photo = False

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
    
    if image_file and card_code:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        try:
            # Leer la imagen en base64 y decodificarla
            base64_image = image_file.read()
            decoded_image = base64.b64decode(base64_image)
            
            # Convertir la imagen decodificada a un objeto de imagen PIL
            image = Image.open(BytesIO(decoded_image))
            
            # Crear un nombre de archivo seguro y único
            filename = secure_filename(datetime.now().strftime("%Y%m%d%H%M%S%f") + '.jpg')
            filepath = os.path.join(upload_folder, filename)
            
            # Guardar la imagen en formato jpg
            image.save(filepath, 'JPEG')

            new_image = ImageModel(image_path=filepath, rfid_code=card_code)
            db.session.add(new_image)
            db.session.commit()

            return jsonify({'message': 'Image uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'message': f'Error saving image: {e}'}), 500

    return jsonify({'message': 'Missing image file or RFID code'}), 404
