import os
import uuid

from flask import jsonify, request
from flask_openapi3 import Tag, APIBlueprint
from werkzeug.utils import secure_filename
from app.core.config import UPLOAD_FOLDER
from app.core.storage import allowed_file
from app.models.inquiry import Inquiry
from app.schemas.inquiry import InquiryCreate, InquiryResponse, InquiryParams, InquiryUpdate
from app.services.inquiry import inquiry_service
from app.core.database import db

tag = Tag(name="inquiry", description="Routes used for inquiry management")

router = APIBlueprint(
    "inquiry",
    __name__,
    abp_tags=[tag],
    url_prefix="/inquiries"
)

service = inquiry_service()

# @router.post("/", responses={200: InquiryResponse}, description="Route used for Inquiry creation")
# async def create(body: InquiryCreate):

#     if "file" not in request.files:
#         return jsonify({"error": "No file sent"}), 400

#     file = request.files["file"]

#     filename, url = upload_file(file)
    
#     inquiry = service.create(db.session(), 
#                          appointment_id=body.appointment_id,
#                          image_url=url,
#                          inquiry_status=body.inquiry_status
#                          )
#     if not inquiry:
#         return jsonify({"error":"Erro ao tentar criar registro"}), 400
    
#     return jsonify({
#         "data":inquiry,
#         "upload":f"Upload realizado com sucesso, filename: {filename}"
    # })

@router.put("/", responses={200: InquiryResponse}, description="Route used for Inquiry update")
async def update(body: InquiryUpdate, params: InquiryParams):
    return service.update(db.session(), 
                        params.id,
                        image_url=body.image_url,
                        result_text=body.result_text,
                        result_json_url=body.result_json_url,
                        result_image_url=body.result_image_url,
                        inquiry_status=body.inquiry_status
                    )

@router.get("/<int:id>", responses={200: InquiryResponse}, description="Route used to get an inquiry by ID")
async def get_one(path: InquiryParams):
    return service.getOne(db.session(), id=path.id)

@router.get("/", responses={200: InquiryResponse}, description="Route used to list all inquiries")
async def get_all():
    return service.getAll(db.session())

@router.delete("/", responses={200: InquiryResponse}, description="Route used to delete an inquiry")
async def delete(params: InquiryParams):
    return service.delete(db.session(), id=params.id)


