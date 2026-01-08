import streamlit as st 
import requests
import pandas as pd

st.set_page_config(page_title = "Smart AQI Monitor", layout = "wide")

st.title("Smart Air Quality Monitor")
st.subheader("Helping you to breath easier")

#Input for location
city = st.selectbox("Select a city", ["Frankfurt", "Berlin", "Hamburg", "Munich", "Stuttgart", "London", "Bengaluru"])

#Coordinate Map
coordinates = {
  "Frankfurt": {"lat": 50.1109, "lon": 8.6821},
  "Berlin": {"lat": 52.5200, "lon": 13.4050},
  "Hamburg": {"lat": 53.5511, "lon": 9.9937},
  "Munich": {"lat": 48.1351, "lon": 11.5820},
  "Stuttgart": {"lat": 48.7758, "lon": 9.1829},
  "London": {"lat": 51.5074, "lon": -0.1278},
  "Bengaluru": {"lat": 12.9716, "lon": 77.5946}
}

lat = coordinates[city]["lat"]
lon = coordinates[city]["lon"]

#call api
if st.button("Get air quality forecast"):
  response = requests.get(f"http://127.0.0.1:8000/aqi/{lat}/{lon}")
  
  if response.status_code == 200:
    data = response.json()
    
    col1, col2 = st.columns(2)
    col1.metric("Current AQI", data["current_aqi"])
    col2.metric("Predicted Tomorrow", data["predicted_tomorrow_aqi"])
    
    st.info(f"Recommendation: {data['recommendation']}")
    
    neighborhood_data = pd.DataFrame({
            'lat': [lat, lat + 0.005, lat - 0.005, lat + 0.008, lat - 0.008],
            'lon': [lon, lon + 0.005, lon - 0.005, lon + 0.002, lon - 0.002],
            'aqi': [data["current_aqi"], 2, 3, 1, 5] # These are example values for now
    })
    st.subheader(f"HeatMap of {city}")
    st.map(neighborhood_data)
  else:
    st.error("Failed to connect Backend API")
    