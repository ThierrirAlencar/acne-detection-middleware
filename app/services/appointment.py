from sqlalchemy.orm import Session
from datetime import datetime
from app.models.appointment import Appointment




class appointment_service:
    
    def create(
            self, 
            session: Session,
            user_id: int
        ):
        
        appointment = Appointment(
            user_id=user_id,
            created_at=datetime.utcnow()
        )
        
        session.add(appointment)
        session.commit()
        session.refresh(appointment)
        session.close()
        
        return {"id": appointment.id, "user_id": appointment.user_id, "created_at": appointment.created_at}
    
    def getOne(
            self,
            session: Session,
            id: int
    ):
        appointment = session.query(Appointment).filter(Appointment.id == id).first()
        session.close()
        
        return appointment
    
    def getAll(
            self,
            session: Session,
            user_id: int = None
    ):
        query = session.query(Appointment)
        
        if user_id:
            query = query.filter(Appointment.user_id == user_id)
        
        appointments = query.all()
        session.close()
        
        return appointments
    
    def delete(
            self,
            session: Session,
            id: int
    ):
        appointment = session.query(Appointment).filter(Appointment.id == id).first()
        
        if not appointment:
            session.close()
            return False
        
        session.delete(appointment)
        session.commit()
        session.close()
        
        return appointment
    
    def update(
            self, 
            session: Session, 
            id: int, 
            user_id: int = None
    ):
        appointment = session.query(Appointment).filter(Appointment.id == id).first()
        
        if not appointment:
            session.close()
            return None
        
        if user_id:
            appointment.user_id = user_id
        
        appointment.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(appointment)
        session.close()
        
        return appointment
