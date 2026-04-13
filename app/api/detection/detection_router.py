import os
from typing import List
import uuid
from app.schemas.inquiry import InquiryCreate, InquiryDetectionResume
from app.utils.enums import inquiryStatus
from flask import jsonify, request
from flask_openapi3 import Tag, APIBlueprint
from werkzeug.utils import secure_filename
from app.core.config import UPLOAD_FOLDER
from app.core.database import db


from app.core.storage import allowed_file
from app.services.detection import DetectionService
from app.services.inquiry import inquiry_service

tag = Tag(name="detection", description="Routes used for running the detection model")

router = APIBlueprint(
    "detection",
    __name__,
    abp_tags=[tag],
    url_prefix="/models/detection"
)

detection_service = DetectionService()
inquiry_service = inquiry_service()

@router.route('/classificate', methods=['POST'])
def upload_image():

    if 'image' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

    appointment_id = request.form.get('appointment_id')
    if not appointment_id:
        return jsonify({'error': 'appointment_id é obrigatório'}), 400

    try:
        appointment_id = int(appointment_id)
    except ValueError:
        return jsonify({'error': 'appointment_id deve ser um número'}), 400

    image_url = request.form.get('image_url')  # optional

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = secure_filename(file.filename)
    temp_filename = f"{uuid.uuid4()}_{filename}"
    save_path = os.path.join(UPLOAD_FOLDER, temp_filename)
    file.save(save_path)

    try:
        detection_res = detection_service.run(save_path, temp_filename, conf=0.25)
    except Exception as e:
        return jsonify({
            'error': 'Falha na detecção',
            'details': str(e)
        }), 500

    completion_data = InquiryDetectionResume(
        result_text=f"GAGS Score: {detection_res.gags_score}, Severity: {detection_res.gags_severity}",
        result_json_url=detection_res.result_json_path,
        result_image_url=detection_res.result_image_path
    )

    return inquiry_service.create(db.session(), 
                                  appointment_id=appointment_id, 
                                  image_url=image_url or save_path,
                                  inquiry_status=inquiryStatus.COMPLETED,
                                  completion_data=completion_data
                                  )