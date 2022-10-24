import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 6.695070
MY_LONG = -1.615800

response = requests.get(url="https://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# MY_LAT = iss_latitude - float(4) for code testing
# MY_LONG = iss_longitude + float(4)

# Your position is within +5 or -5 degrees of the ISS position.


def iss_overhead():
    if (iss_latitude - 5) <= MY_LAT <= (iss_latitude + 5) and (iss_longitude - 5) <= MY_LONG <= (iss_longitude + 5):
        return True


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
hour_now = time_now.hour
# If the ISS is close to my current position,
# and it is currently dark
# Then email me to tell me to look up.
# BONUS: run the code every 60 seconds.

# insert your email and password.
if iss_overhead():
    if hour_now <= sunrise or hour_now >= sunset:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user="leom59152@gmail.com", password="abcd12345()")
            connection.sendmail(from_addr="leom59152@gmail.com", to_addrs="leom59152@gmail.com",
                                msg="Subject: ISS TRACKER\n\nLook Up. You should see the ISS now")
            print("Success")
