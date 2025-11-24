from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from enum import Enum

from . import models, schemas, database, utils

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task Manager Backend Mobcom")

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    exist_email = db.query(models.User).filter(models.User.email == user.email).first()
    if exist_email:
        raise HTTPException(400, "email sudah terdaftar")
    
    hashed_password = utils.get_password_hash(user.password)

    new_user = models.User(
        email = user.email,
        password = hashed_password,
        nama = user.nama,
        npm = user.npm,
        prodi = user.prodi
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user_creds: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()
    if not user:
        raise HTTPException(401, "Email atau password salah")

    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(401, "Email atau password salah")
    
    return {"status": "berhasil login"}

@app.get("/me", response_model=schemas.UserBase)
def get_profile_data(user_creds: schemas.UserMe, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()

    if not user:
        raise HTTPException(404, "Email tidak ditemukan")

    return user

@app.post("/tugas", response_model=schemas.Tugas)
def create_tugas(tugas: schemas.TugasCreate, db: Session = Depends(database.get_db)):
    db_tugas = models.Tugas(**tugas.dict())
    db.add(db_tugas)
    db.commit()
    db.refresh(db_tugas)
    return db_tugas

class StatusFilter(str, Enum):
    selesai = "selesai"
    belum_selesai = "belum_selesai"

@app.get("/tugas", response_model=List[schemas.Tugas])
def get_tugas(
    user_id: int = Depends(utils.get_user_id),
    skip: int=0,
    limit: int=100,
    status: Optional[StatusFilter] = None,
    matakuliah_id: Optional[int] = None,
    db: Session = Depends(database.get_db)
    ):

    query = db.query(models.Tugas).filter(models.Tugas.user_id == user_id)

    if status is not None:
        if status == StatusFilter.selesai:
            query = query.filter(models.Tugas.is_done == True)
        elif status == StatusFilter.belum_selesai:
            query = query.filter(models.Tugas.is_done == False)
    
    if matakuliah_id is not None:
        query = query.filter(models.Tugas.matakuliah_id == matakuliah_id)

    tugas = query.offset(skip).limit(limit).all()
    return tugas

@app.get("/tugas/progres", response_model=schemas.TugasProgress)
def get_progress_tugas(
    user_id: int = Depends(utils.get_user_id),
    db: Session = Depends(database.get_db)
    ):
    query = db.query(models.Tugas).filter(models.Tugas.user_id == user_id)
    selesai = query.filter(models.Tugas.is_done == True).count()
    belum_selesai = query.filter(models.Tugas.is_done == False).count()

    return schemas.TugasProgress(selesai=selesai, belum_selesai=belum_selesai)

@app.get("/tugas/{tugas_id}", response_model=schemas.Tugas)
def get_tugas_by_id(tugas_id: int, db: Session = Depends(database.get_db)):
    tugas = db.query(models.Tugas).filter(models.Tugas.id == tugas_id).first()
    if tugas is None:
        raise HTTPException(status_code=404, detail="tugas not found")
    
    return tugas

@app.patch("/tugas/{tugas_id}/status", response_model=schemas.Tugas)
def update_tugas_status(tugas_id: int, db: Session = Depends(database.get_db)):
    tugas = db.query(models.Tugas).filter(models.Tugas.id == tugas_id).first()
    if not tugas:
        raise HTTPException(status_code=404, detail=f"Tugas dengan id {tugas_id} tidak ditemukan")
    
    tugas.is_done = not tugas.is_done
    db.commit()
    db.refresh(tugas)
    
    return tugas

@app.get("/matakuliah", response_model=List[schemas.Matakuliah])
def get_matakuliah(db: Session = Depends(database.get_db)):
    matakuliah = db.query(models.Matakuliah).all()
    return matakuliah

@app.get("/")
def read_root():
    return {"Hello from FastAPI Mobcom Backend Hehe!!"}