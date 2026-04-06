from flask import Flask
from flask_openapi3.openapi import OpenAPI

def api_routes(app: OpenAPI):
    from app.api.user.user_router import router as user_router
    from app.api.appointment.appointment_router import router as appointment_router
    from app.api.inquiry.inquiry_router import router as inquiry_router 

    with app.app_context():
        app.register_api(user_router)
        app.register_api(inquiry_router)
        app.register_api(appointment_router)
    pass;

def init_db(app):
    #importe a lista de models
    from app.models.user import User
    from app.models.appointment import Appointment
    from app.models.inquiry import Inquiry
    
    from app.core.database import db
    from sqlalchemy.orm import configure_mappers


    db.init_app(app)

    # Configura os troõ 
    configure_mappers()


def create_app():
    app = OpenAPI(
        doc_prefix="/docs",
        import_name=__name__
    )

    from app.core.env import DATABASE_URL

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    with app.app_context():
        api_routes(app=app)
        db = init_db(app=app)
    return app;
