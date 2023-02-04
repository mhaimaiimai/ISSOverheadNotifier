import requests
from datetime import datetime
import time
import smtplib

MY_LATITUDE = 13.981891215313697
MY_LONGITUDE = 100.5555275877521
ACCEPT_DIFF_DEGREE = 5
MY_EMAIL = ""
MY_PASSWORD = ""
RECIPIENT = ""

parameters = {
    "lat" : MY_LATITUDE, 
    "long" : MY_LONGITUDE,
    "formatted" : 0
}

def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    current_hour = datetime.now().hour
    
    return current_hour>=sunset or current_hour<=sunrise


def is_iss_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()
    iss_long = float(data["iss_position"]["longitude"])
    iss_lat = float(data["iss_position"]["longitude"])

    return (abs(MY_LATITUDE-iss_lat) <= ACCEPT_DIFF_DEGREE 
        and abs(MY_LONGITUDE-iss_long) <= ACCEPT_DIFF_DEGREE)


while(True):
    if is_iss_near() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=RECIPIENT,
            msg="Subject:Look up!\n\nThe ISS is above you in the sky.")
    time.sleep(60)