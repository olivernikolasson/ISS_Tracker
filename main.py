import requests
from datetime import datetime
import smtplib
import time

TO_MAIL = "MAILADRESS"
FROM_MAIL ""
FROM_MAIL_PASSWORD = ""

MY_LAT = 57.786612 # Your latitude
MY_LONG = 14.128225 # Your longitude

def iss_pos():
    global MY_LAT, MY_LONG
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True



def time_check():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    now_hour = time_now.hour
    if now_hour >= sunset or now_hour <= sunrise:
        return True



def send():
    print("Log for sending")
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    my_email = FROM_MAIL
    password =     my_email = FROM_MAIL_PASSWORD
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password,)

        connection.sendmail(from_addr=my_email,
                           to_addrs=TO_MAIL,
                           msg=f"Subject:ISS Is Above you!\n\nHello! The ISS is/was above you\n the pos was\n"
                               f"LONG: {iss_longitude}\nLAT:{iss_latitude}")



while True:
    time.sleep(60)
    if iss_pos() and time_check():
        print("Send Log")
        send()
