import  bcrypt
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

def verify_password(plain_password: str, hashed_password_from_db: str) -> bool:
    bytes_plain_password = plain_password.encode('utf-8')
    bytes_hashed_password_from_db = hashed_password_from_db.encode('utf-8')

    return bcrypt.checkpw(bytes_plain_password, bytes_hashed_password_from_db)

def get_password_hash(password: str) -> str:
    bytes_password = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
    stored_password = hashed_bytes.decode('utf-8')

    return stored_password

def get_user_id(
    user: schemas.UserMe,
    db: Session = Depends(database.get_db)
    ) -> int:
    user_object = db.query(models.User).filter(models.User.email == user.email).first()
    if not user_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email tidak ditemukan"
        )
    
    print("user id = ", user_object.id)
    
    return user_object.id