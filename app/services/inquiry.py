from sqlalchemy.orm import Session
from datetime import datetime
from app.models.inquiry import Inquiry
from app.utils.enums import inquiryStatus




class inquiry_service:
    
    def create(
            self, 
            session: Session,
            appointment_id: int,
            image_url: str = None,
            inquiry_status: inquiryStatus = inquiryStatus.ONGOING
        ):
        
        inquiry = Inquiry(
            appointment_id=appointment_id,
            image_url=image_url,
            inquiry_status=inquiry_status,
            created_at=datetime.utcnow()
        )
        
        session.add(inquiry)
        session.commit()
        session.refresh(inquiry)
        session.close()
        
        return {
            "id": inquiry.id, 
            "appointment_id": inquiry.appointment_id, 
            "image_url": inquiry.image_url,
            "inquiry_status": inquiry.inquiry_status,
            "created_at": inquiry.created_at
        }
    
    def getOne(
            self,
            session: Session,
            id: int
    ):
        inquiry = session.query(Inquiry).filter(Inquiry.id == id).first()
        session.close()
        
        return inquiry
    
    def getAll(
            self,
            session: Session,
            appointment_id: int = None,
            status: inquiryStatus = None
    ):
        query = session.query(Inquiry)
        
        if appointment_id:
            query = query.filter(Inquiry.appointment_id == appointment_id)
        
        if status:
            query = query.filter(Inquiry.inquiry_status == status)
        
        inquiries = query.all()
        session.close()
        
        return inquiries
    
    def delete(
            self,
            session: Session,
            id: int
    ):
        inquiry = session.query(Inquiry).filter(Inquiry.id == id).first()
        
        if not inquiry:
            session.close()
            return False
        
        session.delete(inquiry)
        session.commit()
        session.close()
        
        return inquiry
    
    def update(
            self, 
            session: Session, 
            id: int,
            image_url: str = None,
            result_text: str = None,
            result_json_url: str = None,
            result_image_url: str = None,
            inquiry_status: inquiryStatus = None
    ):
        inquiry = session.query(Inquiry).filter(Inquiry.id == id).first()
        
        if not inquiry:
            session.close()
            return None
        
        if image_url:
            inquiry.image_url = image_url
        if result_text:
            inquiry.result_text = result_text
        if result_json_url:
            inquiry.result_json_url = result_json_url
        if result_image_url:
            inquiry.result_image_url = result_image_url
        if inquiry_status:
            inquiry.inquiry_status = inquiry_status
        
        inquiry.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(inquiry)
        session.close()
        
        return inquiry
