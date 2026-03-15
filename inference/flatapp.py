from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles 
import uvicorn
import joblib
import numpy as np
import os
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates = Jinja2Templates(directory="flat_project/inference/templates")

def map_minutes(minutes):
    if minutes <= 10: return 3
    elif minutes <= 30: return 2
    else: return 1

Base_dir=os.path.dirname(os.path.abspath(__file__))
model_dir=os.path.join(Base_dir,"..","models","flats.pkl")

model=joblib.load(model_dir)

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("ezn_wroclaw.html", {"request": request})

@app.post("/predict")
async def predict(price_mounth: float=Form(...), minutes_to_school: float=Form(...), looks: float=Form(...)):
    # Перетворюємо хвилини в категорію ПЕРЕД тим, як дати моделі
    minutes_score = map_minutes(minutes_to_school)
    
    # Створюємо масив з новими даними
    X = np.array([[price_mounth, minutes_score, looks]])
    result=model.predict(X)[0]
    if result==1:
        y="Mieszkanie jest dobre dla ucznia EZN🟢"
    else:
        y="Mieszkanie jest źle dla ucznia EZN🔴"
    return {"FLAT":y}
    
    



if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)