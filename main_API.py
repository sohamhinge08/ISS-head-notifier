import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()

my_gmail = os.getenv("GMAIL_USER")
password = os.getenv("GMAIL_PASSWORD")
my_lat=40.706001
my_long=-74.008804
def iss_at_my_loc():    
    response=requests.get(url="https://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data=response.json()
    # if response.status_code==404:
    #     raise Exception("the resourse does not exist")
    # elif response.status_code==401:
    #     raise Exception("You are not authorized to access data")
    # response.raise_for_status()
    longitude=float(data["iss_position"]["longitude"])
    latitude=float(data["iss_position"]["latitude"])
    # position=(longitude,latitude)
    if my_lat-5<=latitude<=my_lat+5 and my_long<=longitude<=my_long+5:
        return True

def is_night():
    params={
        "lat":my_lat,
        "lng":my_long,
        "formatted":0
    }
    response=requests.get(url="https://api.sunrise-sunset.org/json",params=params)
    response.raise_for_status()
    data=response.json()
    sunrise=int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset=int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time=datetime.now()
    if time>=sunset or time<=sunrise:
        return True

while True:
    time.sleep(60)
    if iss_at_my_loc() and is_night():
        connection= smtplib.SMTP("smtp.gmail.com",port=587)
        connection.starttls()
        connection.login(user=my_gmail,password=password)
        connection.sendmail(from_addr=my_gmail,to_addrs="tojifushiguro4469@yahoo.com",msg="subject:look up\n\n the iss is above you")
        connection.close()
