from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

#Matakuliah Schema
class MatakuliahBase(BaseModel):
    nama: str
    sks: Optional[int] = None
    hari: Optional[str] = None
    jam_mulai: Optional[str] = None
    jam_selesai: Optional[str] = None

class MatakuliahCreate(MatakuliahBase):
    pass

class Matakuliah(MatakuliahBase):
    id: int
    class Config:
        from_attributes = True

#Tugas Schema
class TugasBase(BaseModel):
    judul: str
    deskripsi: Optional[str] = None
    deadline: Optional[datetime] = None
    is_done: bool = False
    prioritas: Optional[str] = "Sedang"
    matakuliah_id: Optional[int] = None

class TugasCreate(TugasBase):
    user_id: int

class Tugas(TugasBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    matakuliah_nama: str

    class Config:
        from_attributes = True

class TugasProgress(BaseModel):
    selesai: int
    belum_selesai: int

#User Schema
class UserBase(BaseModel):
    email: str
    nama: str
    npm: str
    prodi: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserMe(BaseModel):
    email: str

class User(UserBase):
    id: int
    tugas: List[Tugas] = []

    class Config:
        from_attributes = True