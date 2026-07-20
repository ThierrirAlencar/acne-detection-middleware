from typing import List

from flask_openapi3 import Tag, APIBlueprint
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentParams, AppointmentUpdate
from app.services.appointment import appointment_service
from app.core.database import db

tag = Tag(name="appointment", description="Routes used for appointment management")

router = APIBlueprint(
    "appointment",
    __name__,
    abp_tags=[tag],
    url_prefix="/appointments"
)

service = appointment_service()

@router.post("/", responses={200: AppointmentResponse}, description="Route used for Appointment creation")
async def create(body: AppointmentCreate):
    return service.create(db.session(), 
                        user_id=body.user_id
                    )

@router.put("/<int:id>", responses={200: AppointmentResponse}, description="Route used for Appointment update")
async def update(body: AppointmentUpdate, params: AppointmentParams):
    return service.update(db.session(), params.id, user_id=body.user_id)

@router.get("/<int:id>", responses={200: AppointmentResponse}, description="Route used to get an appointment by ID")
async def get_one(path: AppointmentParams):
    return service.getOne(db.session(), id=path.id)

@router.get("/", responses={200: AppointmentResponse}, description="Route used to list all appointments")
async def get_all():
    return service.getAll(db.session())

@router.delete("/", responses={200: AppointmentResponse}, description="Route used to delete an appointment")
async def delete(params: AppointmentParams):
    return service.delete(db.session(), id=params.id)
