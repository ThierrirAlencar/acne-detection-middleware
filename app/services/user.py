from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User




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

        return {"email":user.email, "username":user.userbame}
    
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

    def update(self, session:Session, id: int, name: str = None, email: str = None):
        user = session.query(User).filter(User.id == id).first()
        
        if not user:
            session.close()
            return None

        if name:
            user.name = name
        if email:
            user.email = email

        session.commit()
        session.refresh(user)

        session.close()
        return user

