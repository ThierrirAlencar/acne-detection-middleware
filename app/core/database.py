
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, registry


mapper_registry = registry()

class Base(DeclarativeBase, MappedAsDataclass):
    registry = mapper_registry
    pass


db = SQLAlchemy(model_class=Base);
