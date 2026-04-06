from flask_openapi3 import Tag, APIBlueprint
from app.schemas.user import UserCreate, UserBase, UserParams, UserUpdate
from app.services.user import user_service
from app.core.database import db

tag = Tag(name="user",description="Routes used for user management")

router = APIBlueprint(
    "user",
    __name__,
    abp_tags=[tag],
    url_prefix="/users"
)

service = user_service;

@router.post("/",responses={200:UserBase},description="Route used for User creation")
async def create(body:UserCreate):
    return service.create(db.session(), 
                          email=body.email,
                          password=body.password, 
                          username=body.username
                            )

@router.put("/",responses={200:UserBase},description="Route used for User update")
async def update(body:UserUpdate, params:UserParams):
    return service.update(db.session(),params.id,data=body)

@router.get("/profile",responses={200:UserBase},description="Route used to get an out of permission user")
async def profile(params:UserParams):
    return service.getOne(db.session(),id=params.id)

@router.delete("/",responses={200:UserBase},description="Route used to delete a user")
async def delete(params:UserParams):
    return service.delete(db.session(),id=params.id)

