from producer import API_LIST, LATITUDE_PARIS, LONGITUDE_PARIS
from kafka import KafkaConsumer
from producer import kafka_producer, publish
from geopy.distance import distance
import json
import time
from datetime import datetime
import numpy as np


def IsVisible(position):
    PARIS_POSITION = (LATITUDE_PARIS, LONGITUDE_PARIS)
    pos = position['latitude'], position['longitude']
    d = distance(PARIS_POSITION, pos).m
    if d < 500000:
        return True, d
    else:
        return False, d


if __name__ == "__main__":
    while True:
        for api in API_LIST:
            # Initialize consumer variable
            consumer = KafkaConsumer(
                api["name"],
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='latest',
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode('ascii'))
            )
            # Read message from consumer
            position = None
            for msg in consumer:
                position = msg.value
                consumer.close()

            if True: #True for debug, set IsVibile(position) when ready
                producer = kafka_producer()
                now = datetime.utcnow()
                current_time = now.strftime("%H:%M:%S")
                visible, dist = IsVisible(position)
                notification = {"Satellite": api["name"],
                                "Time": current_time,
                                "Position": position,
                                "Visibility": "Visible" if visible else "Not Visible",
                                "Distance": dist}
                print(notification)
                publish(producer, "NOTIFICATIONS", "Visibility", json.dumps(notification))
                producer.close()

        time.sleep(30)  # limit number of API calls per hour
