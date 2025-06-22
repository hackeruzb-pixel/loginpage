from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Pydantic model
class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


# ✅ DB ulanish funksiyasi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 Parolni hash qilish
def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/sign-up", status_code=201)
def register_user(payload: RegisterRequest, db: Session = next(get_db())):
    # 🛑 Email yoki username allaqachon mavjudligini tekshirish
    if db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bunday email yoki username allaqachon mavjud."
        )

    # ✅ Yangi foydalanuvchi yaratish
    new_user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"}
