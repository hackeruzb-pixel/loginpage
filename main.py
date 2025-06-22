from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import user, upload
from database import Base, engine

# Jadval modellari
import models.user as user_models

# FastAPI ilova
app = FastAPI()

# Jadvallarni yaratamiz (agar mavjud bo'lmasa)
Base.metadata.create_all(bind=engine)

# 📦 Statik fayllar (rasmlar uchun)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🌐 CORS sozlamalari (frontend bilan bog'lanish uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # frontend manzili
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚪 Marshrutlar
app.include_router(user.router)
app.include_router(upload.router)

# 🔍 Test endpoint
@app.get("/")
def root():
    return {"message": "Backend ishlayapti!"}
