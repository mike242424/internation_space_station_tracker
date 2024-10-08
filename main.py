import requests
import datetime as dt
import smtplib
import time
from dotenv import load_dotenv
import os

load_dotenv()

MY_LAT = os.getenv('MY_LAT')
MY_LNG = os.getenv('MY_LNG')
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
current_time = dt.datetime.now()


def is_iss_overhead():
    iss_now_response = requests.get(url='http://api.open-notify.org/iss-now.json')
    iss_now_response.raise_for_status()
    iss_lat = float(iss_now_response.json()['iss_position']['latitude'])
    iss_lng = float(iss_now_response.json()['iss_position']['longitude'])

    if (iss_lat - 5) <= float(MY_LAT) <= (iss_lat + 5) and (iss_lng - 5) <= float(MY_LNG) <= (iss_lng + 5):
        return True
    else:
        return False


def is_night():
    parameters = {"lat": MY_LAT, "lng": MY_LNG, "formatted": 0}
    sunrise_sunset_response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    sunrise_sunset_response.raise_for_status()
    sunset_hour = sunrise_sunset_response.json()['results']['sunset'].split('T')[1].split(':')[0]
    sunrise_hour = sunrise_sunset_response.json()['results']['sunrise'].split('T')[1].split(':')[0]
    current_time_hour = current_time.hour

    if int(sunset_hour) < current_time_hour < int(sunrise_hour):
        return True
    else:
        return False


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs='mikebyers24@gmail.com',
                msg=f'Subject: ISS Overhead!\n\nLook up for the ISS overhead!')

    else:
        print('ISS currently not overhead')
