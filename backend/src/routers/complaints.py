from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import Complaint, Route
from ..schemas.complaint import ComplaintCreate, ComplaintRead, ComplaintUpdate
from sqlalchemy.exc import IntegrityError
from ..routers.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/complaints", tags=["Complaints"])

@router.post("/", response_model=ComplaintRead)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # تحقق من وجود route_id إذا تم إرساله
    if complaint.route_id is not None:
        route = db.query(Route).filter(Route.id == complaint.route_id).first()
        if not route:
            raise HTTPException(status_code=400, detail="المسار المحدد غير موجود")
    db_complaint = Complaint(**complaint.dict())
    db.add(db_complaint)
    try:
        db.commit()
        db.refresh(db_complaint)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="خطأ في حفظ الشكوى: تأكد من صحة البيانات المدخلة وعدم تكرار الشكوى")
    return db_complaint

@router.get("/", response_model=List[ComplaintRead])
def get_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).all()

@router.get("/{complaint_id}", response_model=ComplaintRead)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.put("/{complaint_id}", response_model=ComplaintRead)
def update_complaint(complaint_id: int, update: ComplaintUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if complaint.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="You do not have permission to update this complaint")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(complaint, key, value)
    db.commit()
    db.refresh(complaint)
    return complaint

@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if complaint.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this complaint")
    db.delete(complaint)
    db.commit()
    return {"message": "Complaint deleted successfully"} 