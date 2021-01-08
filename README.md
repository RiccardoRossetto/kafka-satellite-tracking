# Real-Time Satellite Tracking Using Kafka

##### Authors: Coldebella Davide, Rossetto Riccardo

The application we developed, involves Kafka, Python, Flask, and Leaflet to produce a real-time map displaying the position of two satellites, the **ISS** (International Space Station) and the **NOAA-N Prime** (National Oceanic and Atmospheric Administration). 

### Architecture

In order to interface Kafka and Python we used the library *kafka-python*, its classes allowed us to instantiate producers and consumers; instead, in order to show our results, we used Flask in conjunction with Leaflet, so that we could host an HTML page, inside which we displayed our Leaflet map.

#### Producer

---

The producer, requests from an API the positions of the two satellites every 30 seconds, parses them in order to keep only the position, which is what we are interested in, and finally published them to their respective topic, encoding them into bytes.

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

The consumer uses Flask, in order to route the messages published by the producer to a local web-server to print the real-time positions of the satellites in a Leaflet map. It's configured such that it always read the latest message produced inside the two topics.

The JavaScript code for the Leaflet map can be found inside the *static* folder, while the HTML index is in the *template* folder.

Here's a snapshot of the map:

![](https://github.com/RiccardoRossetto/kafka-satellite-tracking/blob/main/imgs/map.jpeg)

As it can be seen, there are three objects in the map:

* Two markers, one for each satellite. A label appears when hovering on them with the mouse.
* One red circle, which represents the area inside which a visibility notification is triggered for an observer in the center of the circle (500 Km radius).

#### Notifications

---

To implement a notifications system, we created another consumer which reads the messages produced, and computes the distances between the satellites' position and the observer's position (which in our case we set it to Paris), and given a distance threshold (500 Km) produces a message inside the **NOTIFICATIONS** topic signaling if the satellites are visible or not (independently).

##### NOTIFICATIONS:

![](https://github.com/RiccardoRossetto/kafka-satellite-tracking/blob/main/imgs/notif-topic.jpeg)



