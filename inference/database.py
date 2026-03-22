from sqlalchemy import create_all_engines, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# База даних: беремо URL з налаштувань Render (через змінні оточення)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db") # sqlite як запасний варіант

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    price_mounth = Column(Float)
    minutes_to_school = Column(Float)
    looks = Column(Float)
    prediction_result = Column(String) # Текст: "Mieszkanie jest dobre..."
    model_version = Column(String)     # Версія: наприклад "v1.0"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Налаштування підключення
# (ми додамо цей код у flatapp.py пізніше)