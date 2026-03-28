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
import sqlite3
import time
import requests

API_KEY = 'AIzaSyDxTk6XGncvu7gwfO-vCj6-5PW-7-I4dDw'

# --- 1. НАЛАШТУВАННЯ БАЗИ ТА МОДЕЛІ ---
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./local_flat.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="inference/templates")

# Завантаження ML моделі
Base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(Base_dir, "..", "models", "flats.pkl")
model = joblib.load(model_path)
BAZA_PATH=os.path.join(Base_dir,'..','data','uczelnie.db')

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    price_mounth = Column(Float)
    flat_address =Column(String)
    school_choice =Column(String)
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

def pobierz_koordynaty(nazwa_uczelni):
    """Wyciąga lat i lng z bazy danych dla podanej nazwy."""
    if not os.path.exists(BAZA_PATH):
        print(f"❌ ПОМИЛКА: Файл бази не знайдено за шляхом: {os.path.abspath(BAZA_PATH)}")
    conn = sqlite3.connect(BAZA_PATH)
    c = conn.cursor()
    # Szukamy nazwy (pamiętaj o .upper() wcześniej)
    c.execute("SELECT lat, lng FROM punkty WHERE nazwa = ?", (nazwa_uczelni,))
    wynik = c.fetchone()
    conn.close()
    return wynik

def sprawdz_czas_dojazdu(start, cel_coords, api_key):
    """Pyta Google Maps o czas dojazdu (tranzytem/autem)."""
    lat, lng = cel_coords
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start}&destinations={lat},{lng}&mode=transit&key={api_key}"
    response = requests.get(url).json()

    if response['status'] == 'OK':
        return response['rows'][0]['elements'][0]['duration']['value']
    else:
        raise Exception("Błąd API")

# --- 2. ІНІЦІАЛІЗАЦІЯ ДОДАТКА ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() # Створюємо таблиці при запуску
    yield



# --- 3. МАРШРУТИ (ENDPOINTS) ---

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("ezn_wroclaw.html", {"request": request})

@app.post("/predict")
async def predict(
    price_mounth: float = Form(...), 
    flat_address:str=Form(...),
    school_choice:str=Form(...),
    looks: float = Form(...),
    db: Session = Depends(get_db)
):
    school_cord=pobierz_koordynaty(school_choice)
    minutes_to_school=sprawdz_czas_dojazdu(flat_address,school_cord,API_KEY)
    minutes_to_school=round(minutes_to_school/60,2)
    X = np.array([[price_mounth,(minutes_to_school), looks]])
    prediction = model.predict(X)[0]
    
    # Змінюємо текст на англійську
    result_text = "Good for student 🟢" if prediction == 1 else "Bad for student 🔴"

    new_log = Prediction(
        price_mounth=price_mounth,
        flat_address=flat_address,
        school_choice=school_choice,
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