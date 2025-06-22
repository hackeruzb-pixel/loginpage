from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from uuid import uuid4

from auth.oauth2 import get_current_user  # Token orqali userni aniqlash
from models.user import User
from database import db  # DB sessiya

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# Rasm saqlanadigan papka
UPLOAD_DIR = "static/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/avatar")
async def upload_avatar(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Fayl kengaytmasi tekshiruvi
    ext = image.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Faqat JPG, JPEG yoki PNG ruxsat etiladi.")

    # Fayl nomi yaratish (UUID bilan)
    filename = f"{uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Faylni serverga yozamiz
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # DB da foydalanuvchining avatar manzilini yangilaymiz
    current_user.avatar = f"/static/avatars/{filename}"
    db.add(current_user)
    db.commit()

    return JSONResponse({
        "message": "Avatar muvaffaqiyatli yuklandi",
        "avatar": current_user.avatar  # frontend shu yo‘l bilan oladi
    })
