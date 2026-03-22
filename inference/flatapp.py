from fastapi import FastAPI, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import joblib
import numpy as np
import os
from datetime import datetime
from contextlib import asynccontextmanager

# --- 1. НАЛАШТУВАННЯ БАЗИ ТА МОДЕЛІ ---
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./local_flat.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    price_mounth = Column(Float)
    minutes_to_school = Column(Float)
    looks = Column(Float)
    prediction_result = Column(String)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 2. ІНІЦІАЛІЗАЦІЯ ДОДАТКА ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # Створюємо таблиці при запуску
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="inference/templates")

# Завантаження ML моделі
Base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(Base_dir, "..", "models", "flats.pkl")
model = joblib.load(model_path)

# --- 3. МАРШРУТИ (ENDPOINTS) ---

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("ezn_wroclaw.html", {"request": request})

@app.post("/predict")
async def predict(
    price_mounth: float = Form(...), 
    minutes_to_school: float = Form(...), 
    looks: float = Form(...),
    db: Session = Depends(get_db)
):
    def map_minutes(m): return 3 if m <= 10 else 2 if m <= 30 else 1
    X = np.array([[price_mounth, map_minutes(minutes_to_school), looks]])
    prediction = model.predict(X)[0]
    
    # Змінюємо текст на англійську
    result_text = "Good for EZN student 🟢" if prediction == 1 else "Bad for EZN student 🔴"

    new_log = Prediction(
        price_mounth=price_mounth,
        minutes_to_school=minutes_to_school,
        looks=looks,
        prediction_result=result_text,
        model_version="v1.0_rf"
    )
    db.add(new_log)
    db.commit()
    
    return {"FLAT": result_text}

@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    logs = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(10).all()
    # Змінюємо ключі на англійську: date, price, result
    return [
        {
            "price": l.price_mounth, 
            "minutes": l.minutes_to_school,
            "looks":l.looks,
            "result": l.prediction_result, 
            "date": l.created_at.strftime("%d.%m %H:%M")
            
        } for l in logs
    ]