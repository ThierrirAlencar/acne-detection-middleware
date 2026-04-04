from flask_openapi3 import Tag, APIBlueprint

tag = Tag(name="user",description="Routes used for user management")

router = APIBlueprint(
    "user",
    __name__,
    abp_tags=[tag],
    url_prefix="/users"
)

@router.get("/")
async def getone():
    return "you should get one"