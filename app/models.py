from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    nama = Column(String, nullable=False)
    npm = Column(String, nullable=False)
    prodi = Column(String, nullable=False)

    #relasi
    tugas = relationship("Tugas", back_populates="owner")

class Matakuliah(Base):
    __tablename__ = "matakuliah"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    sks = Column(Integer, nullable=False)
    hari = Column(String)
    jam_mulai = Column(String)
    jam_selesai = Column(String)

    #relasi dengan tabel tugas
    tugas = relationship("Tugas", back_populates="matakuliah")

class Tugas(Base):
    __tablename__ = "tugas"

    id = Column(Integer, primary_key=True, index=True)
    judul = Column(String, nullable=False)
    deskripsi = Column(String)
    deadline = Column(DateTime)
    is_done = Column(Boolean, default=False)
    prioritas = Column(String)

    #foreign_key
    user_id = Column(Integer, ForeignKey("users.id"))
    matakuliah_id = Column(Integer, ForeignKey("matakuliah.id"))

    #relasi
    owner = relationship("User", back_populates="tugas")
    matakuliah = relationship("Matakuliah", back_populates="tugas")

    #Metadata
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def matakuliah_nama(self):
        return self.matakuliah.nama if hasattr(self, "matakuliah") and self.matakuliah else None