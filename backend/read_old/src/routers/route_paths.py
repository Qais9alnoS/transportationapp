from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.route_path import RoutePathCreate, RoutePathRead, RoutePathUpdate
from src.models import models
from config.database import SessionLocal
from src.routers.auth import get_current_user

router = APIRouter(prefix="/route-paths", tags=["RoutePaths"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RoutePathRead)
def create_route_path(route_path: RoutePathCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_route_path = models.RoutePath(
        route_id=route_path.route_id,
        lat=route_path.lat,
        lng=route_path.lng,
        geom=f'POINT({route_path.lng} {route_path.lat})',
        point_order=route_path.point_order
    )
    db.add(db_route_path)
    db.commit()
    db.refresh(db_route_path)
    return db_route_path

@router.get("/", response_model=list[RoutePathRead])
def read_route_paths(db: Session = Depends(get_db)):
    return db.query(models.RoutePath).all()

@router.get("/{route_path_id}", response_model=RoutePathRead)
def read_route_path(route_path_id: int, db: Session = Depends(get_db)):
    route_path = db.query(models.RoutePath).filter(models.RoutePath.id == route_path_id).first()
    if not route_path:
        raise HTTPException(status_code=404, detail="RoutePath not found")
    return route_path

@router.put("/{route_path_id}", response_model=RoutePathRead)
def update_route_path(route_path_id: int, route_path: RoutePathUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_route_path = db.query(models.RoutePath).filter(models.RoutePath.id == route_path_id).first()
    if not db_route_path:
        raise HTTPException(status_code=404, detail="RoutePath not found")
    for var, value in vars(route_path).items():
        if value is not None:
            setattr(db_route_path, var, value)
    db.commit()
    db.refresh(db_route_path)
    return db_route_path

@router.delete("/{route_path_id}")
def delete_route_path(route_path_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_route_path = db.query(models.RoutePath).filter(models.RoutePath.id == route_path_id).first()
    if not db_route_path:
        raise HTTPException(status_code=404, detail="RoutePath not found")
    db.delete(db_route_path)
    db.commit()
    return {"ok": True} 