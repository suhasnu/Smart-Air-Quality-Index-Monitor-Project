def predict_tomorrow_aqi(current_aqi, wind_speed, humidity):
  """
  Logic: High humidity and low wind usually increase pollution.
  """
  
  prediction = current_aqi
  
  if wind_speed < 2.0:
    prediction += 1
    
  if humidity > 80:
    prediction += 0.5
    
  return min(5, round(prediction))