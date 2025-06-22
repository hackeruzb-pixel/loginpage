from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import auth  # ✅ BUNI ISHLATISH KERAK
from routers import user, upload
from database import Base, engine

# Jadval modellari
import models.user as user_models

app = FastAPI()

# 📦 Statik fayllar (rasmlar uchun)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 💽 Jadvallarni yaratamiz
Base.metadata.create_all(bind=engine)

# 🌐 CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://loginpage-2hce.onrender.com"],  # 🔄 frontend URL'larini qo‘shing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Barcha marshrutlar
app.include_router(auth.router)     # ✅ MUHIM — auth.py ni ulash
app.include_router(user.router)
app.include_router(upload.router)

# 🔍 Test
@app.get("/")
def root():
    return {"message": "Backend ishlayapti!"}
