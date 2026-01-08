from fastapi import FastAPI
import os
from dotenv import load_dotenv
import requests
from backend.model import predict_tomorrow_aqi

# 1. Loading the secret key from .env file
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

@app.get("/")
def read_root():
  return {"status": "Smart Air Quality API is active"}

@app.get("/aqi/{lat}/{lon}")
def get_air_quality(lat: float, lon: float):
  url = f"http://api.openweathermap.org/data/2.5/air_pollution"
  params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key
  }
  
  response = requests.get(url, params=params)
  
  if response.status_code == 200:
    data = response.json()
    current_aqi = data['list'][0]['main']['aqi']
    simulated_wind = 1.5 #low wind
    simulated_humidity = 85 #high humidity
    
    prediction = predict_tomorrow_aqi(current_aqi, simulated_wind, simulated_humidity)
    
    return {
      "city_coords": {"lat":lat, "lon": lon},
      "current_aqi": current_aqi,
      "predicted_tomorrow_aqi": prediction,
      "recommendation": "Stay inside!" if prediction >= 4 else "Safe to go out"
    }
  
  return {"error": "Failed to fetch data"}
  