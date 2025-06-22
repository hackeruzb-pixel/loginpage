# routes/upload.py

from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
import shutil, os
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from auth.deps import get_current_user  # 👈 JWT orqali user olish (agar mavjud bo‘lsa)

router = APIRouter(
    prefix="/upload",
    tags=["upload"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/avatar")
def upload_avatar(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fayl nomini foydalanuvchi ID bilan sozlaymiz
    file_ext = image.filename.split(".")[-1]
    filename = f"user_{current_user.id}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Faylni saqlash
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # DB dagi user avatar maydonini yangilash
    current_user.avatar = file_path
    db.commit()

    return JSONResponse({"message": "Avatar uploaded", "avatar": file_path})
