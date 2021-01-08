from producer import API_LIST, LATITUDE_PARIS, LONGITUDE_PARIS
from kafka import KafkaConsumer
from producer import kafka_producer, publish
import json
import time
from datetime import datetime
import numpy as np


def IsVisible(position):
    dist_x = LATITUDE_PARIS - position["latitude"]
    dist_y = LONGITUDE_PARIS - position["longitude"]
    dist = np.sqrt(dist_x ** 2 + dist_y ** 2)
    if dist < 5.5:
        return True
    else:
        return False


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
                notification = {"Satellite": api["name"],
                                "Time": current_time,
                                "Position": position}
                print(notification)
                publish(producer, "NOTIFICATIONS", "Visibility", json.dumps(notification))
                producer.close()

        time.sleep(30)  # limit number of API calls per hour
