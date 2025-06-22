from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from uuid import uuid4

from auth.oauth2 import get_current_user  # Token orqali userni aniqlash
from models.user import User
from sqlalchemy.orm import Session
from database import get_db  # ✅ to‘g‘ri db sessiya olish

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# 📁 Rasm saqlanadigan papka
UPLOAD_DIR = "static/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/avatar")
async def upload_avatar(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),  # ✅ db sessiya qo‘shildi
    current_user: User = Depends(get_current_user)
):
    # 🔍 Fayl kengaytmasini tekshirish
    ext = image.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Faqat JPG, JPEG yoki PNG ruxsat etiladi.")

    # 🧾 UUID asosida yangi fayl nomi
    filename = f"{uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # 💾 Faylni saqlash
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # 🛠 DB dagi avatar maydonini yangilash
    current_user.avatar = f"/static/avatars/{filename}"
    db.add(current_user)
    db.commit()

    return JSONResponse({
        "message": "Avatar muvaffaqiyatli yuklandi",
        "avatar": current_user.avatar
    })
