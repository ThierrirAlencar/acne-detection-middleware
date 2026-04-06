from flask_openapi3 import Tag, APIBlueprint
from app.services.user import user_service
tag = Tag(name="user",description="Routes used for user management")

router = APIBlueprint(
    "user",
    __name__,
    abp_tags=[tag],
    url_prefix="/users"
)

service = user_service;

@router.post("/")
async def getone():
    return "you should get one"