# Real-Time Satellite Tracking Using Kafka

##### Authors: Coldebella Davide, Rossetto Riccardo

The application we developed involves Kafka, Python, Flask, and Leaflet to produce a real-time map display of the positions of two satellites, the **ISS** (International Space Station) and the **NOAA-N Prime** (National Oceanic and Atmospheric Administration). 

### Architecture

In order to interface Kafka with Python we used the library *kafka-python* whose classes allowed us to instantiate producers and consumers; while, in order to show our results, we used Flask in conjunction with Leaflet, so that we could host an HTML page inside which we displayed our Leaflet map.

#### Producer

---

The producer requests from an API the positions of the two satellites every 30 seconds(due to API limit on the hourly requests), parses them in order to keep only the positions and finally publishes them to their respective topic, encoding them into bytes.

The two topics to which the producer publishes the messages are:

* **ISS**: topic containing the position of the International Space Station
* **NOAA 19**: topic containing the position of the NOAA-N Prime

Here are the topics and the messages they contain:

##### ISS:

![](https://github.com/RiccardoRossetto/kafka-satellite-tracking/blob/main/imgs/iss-topic.jpeg)

##### NOAA-19:

![](https://github.com/RiccardoRossetto/kafka-satellite-tracking/blob/main/imgs/noaa-topic.jpeg)

#### Consumer

---

The consumer uses Flask in order to route the messages published by the producer to a local web-server to print the real-time positions of the satellites in a Leaflet map. It's configured such that it always reads the latest message produced inside the two topics.

The JavaScript code for the Leaflet map can be found inside the *static* folder, while the HTML index is in the *template* folder.

Here's a snapshot of the map:

![](https://github.com/RiccardoRossetto/kafka-satellite-tracking/blob/main/imgs/map.jpeg)

As it can be seen, there are three objects in the map:

* Two markers, one for each satellite. A label appears when hovering over them with the mouse.
* One red circle, which represents the area inside which a visibility notification is triggered for an hypothetical observer in the center of the circle (of 500 Km radius).

#### Notifications

---

To implement a notifications system, we created another consumer which reads the messages produced and computes the distances between the satellites' positions and the observer's position (which in our case is set to Paris); then, given an arbitrary distance threshold (in our case 500 Km), a producer pushes a message inside the **NOTIFICATIONS** topic signaling if the satellites are visible or not (independently from each other).

##### NOTIFICATIONS:

![](https://github.com/RiccardoRossetto/kafka-satellite-tracking/blob/main/imgs/notif-topic.jpeg)

### Getting Started

---

In order to launch this application, first install all of the required dependencies with:

```bash
$ pip3 install -r requirements.txt
```

then, once both the zookeeper and the Kafka server are running, start the following:

* producer.py
* consumer.py
* notif_consumer.py

and let them run in background. They will provide log information about the retrieval and publishing of messages.

To access the web page containing the Leaflet map, connect to http://localhost:5001/.



