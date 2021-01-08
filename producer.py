import json
import time
import requests
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

LATITUDE_PARIS = 48.864
LONGITUDE_PARIS = 2.349
API_LIST = [
    {
        "url": "https://api.n2yo.com/rest/v1/satellite/positions/25544/{0}/{1}/0/1/&apiKey=75ZZ82-5JR6FC-FK7HQH-4M1X".format(
            LATITUDE_PARIS, LONGITUDE_PARIS), "name": "ISS"},
    {
        "url": "https://api.n2yo.com/rest/v1/satellite/positions/33591/{0}/{1}/0/1/&apiKey=75ZZ82-5JR6FC-FK7HQH-4M1X".format(
            LATITUDE_PARIS, LONGITUDE_PARIS), "name": "NOAA_19"}
]

# get_raw_data returns the raw JSON data contained in the requests to the
# provided urls.

def get_raw_data(url):
    data = None
    now = datetime.utcnow()
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}] - Request Sent to...{url}")
    try:
        req = requests.get(url)
        if req.status_code == 200:
            data = req.json()
    except Exception as ex:
        print("Exception in the Request:")
        print(str(ex))
    finally:
        return data


# kafka_proucer instantiate a producer.

def kafka_producer():
    try:
        producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    except KafkaError as ex:
        print("Exception Connecting to Kafka:")
        print(str(ex))
        raise ex
    else:
        return producer

# publish encodes the messages into bytes and publishes the messages to the
# provided topic

def publish(producer, topic, key, value):
    try:
        bKey = bytes(key, encoding="utf-8")
        bValue = bytes(value, encoding="utf-8")
        producer.send(topic, key=bKey, value=bValue)
        producer.flush()
        print(f"Message Published in Topic: {topic}")
    except Exception as ex:
        print("Exception Publishing the Message")
        print(str(ex))
    except KafkaError as ex:
        print("KafkaError in Publishing the Message")
        print(str(ex))

# GetPosition retrieves the position of the satellite from the message.

def GetPosition(message):
    latitude = message['positions'][0]['satlatitude']
    longitude = message['positions'][0]['satlongitude']
    position = {"latitude": latitude, "longitude": longitude}
    return position


if __name__ == "__main__":
    while True:
        for api in API_LIST:
            message = get_raw_data(api["url"])
            position = GetPosition(message)
            producer = kafka_producer()
            publish(producer, api["name"], "Position", json.dumps(position))
            producer.close()
        time.sleep(30) # limit number of API calls per hour
