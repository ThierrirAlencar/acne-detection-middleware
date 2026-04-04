from flask import Flask
from flask_openapi3.openapi import OpenAPI

def api_routes(app: OpenAPI):
    from app.api.user.user_router import router as user_router

    with app.app_context():
        app.register_api(user_router)
    pass;

def create_app():
    app = OpenAPI(
        doc_prefix="/docs",
        import_name=__name__
    )
    with app.app_context():
        api_routes(app=app)

    return app;
