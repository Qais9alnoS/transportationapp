from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import Feedback, Route
from ..schemas.feedback import FeedbackCreate, FeedbackRead
from sqlalchemy.exc import IntegrityError
from ..routers.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/", response_model=FeedbackRead)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # تحقق من وجود route_id إذا تم إرساله
    if feedback.route_id is not None:
        route = db.query(Route).filter(Route.id == feedback.route_id).first()
        if not route:
            raise HTTPException(status_code=400, detail="المسار المحدد غير موجود")
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    try:
        db.commit()
        db.refresh(db_feedback)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="خطأ في حفظ التقييم: تأكد من صحة البيانات المدخلة وعدم تكرار التقييم لنفس المسار")
    return db_feedback

@router.get("/", response_model=List[FeedbackRead])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).all()

@router.get("/{feedback_id}", response_model=FeedbackRead)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this feedback")
    db.delete(feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"} 