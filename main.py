import requests
import os
from twilio.rest import Client

#------------- Keys -------------
API_KEY = os.environ.get("API_KEY")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

#------------ Weather API Directions & Parameters ------------
url_forecast = "https://api.openweathermap.org/data/2.5/forecast"

parameters = {
    "lat": -24.94528,
    "lon": -53.48139,
    "cnt": 6,
    "units": "metric",
    "lang": "pt_br",
    "appid": API_KEY
}
#------------------- Requesting API Data -----------------
try:
    response = requests.get(url=url_forecast, params=parameters)
    response.raise_for_status()
    weather_data = response.json()

except Exception as exception:
    print(f"Error: {exception}")

#------------------ Checking If Will Rain ----------------------
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

#---------------- Sending SMS If Will Rain ---------------------
if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body="It's going to rain today. Bring an umbrella.",
        from_="+14472134114",
        to="+5545999319098")
    print(message.status)
