import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash
from app.models.user import User
from app.core.env import JWT_SECRET

class auth_service:

    def login(self, session: Session, email: str, password: str):
        user = session.query(User).filter(User.email == email).first()
        if not user or not check_password_hash(user.password, password):
            session.close()
            return None

        # Generate JWT token
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        session.close()
        return {'token': token, 'user': {'id': user.id, 'email': user.email, 'username': user.username}}

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None