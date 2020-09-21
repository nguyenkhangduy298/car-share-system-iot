import paho.mqtt.publish as publish

MQTT_SERVER = "10.133.38.193"
MQTT_PATH = "test_channel"

publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)
