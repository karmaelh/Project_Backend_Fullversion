import os
import time
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        return jsonify({'photoUrl': f'/uploads/{new_filename}'})
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
