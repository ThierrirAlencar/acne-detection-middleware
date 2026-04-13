from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.schemas.user import UserUpdate




class user_service:
    
    def create(
            self, 
            session:Session,
            email:str,
            password:str,
            username:str
        ):

        user = User(email=email,
                    password=password,
                    username=username, 
                    created_at=datetime.utcnow()
                    )
        
        session.add(user);

        session.commit(); 

        session.refresh(user);

        session.close()

        return {"email":user.email, "username":user.username}
    
    def getOne(
            self,
            session:Session,
            id:int
    ):
        user = session.query(User).filter(User.id == id);

        session.close();

        return user;

    def delete(
            self,
            session:Session,
            id:int
    ):
        user = session.query(User).filter(User.id == id).first()

        if not user:
            session.close()
            return False

        session.delete(user)
        session.commit()

        session.close()
        return user;

    def update(self, session:Session, id: int, data:UserUpdate):
        
        user = session.query(User).filter(User.id == id).first()
        
        if not user:
            session.close()
            return None

        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        if data.password:
            user.password = data.password
        if data.status:
            user.status = data.status

        session.commit()
        session.refresh(user)

        session.close()
        return user

