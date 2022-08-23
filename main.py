import dht
import machine
from machine import Pin
import urequests
import json
from umqttsimple import MQTTClient
import ubinascii
import math

# Setup DHT Sensor
d = dht.DHT22(Pin(5))

# Setup IFTTT service
# hook_url = "http://maker.ifttt.com/trigger/sensor_reading/with/key/{}".format(config.ifttt_key)
# device_location = "office"

# SETUP MQTT service details and assign unique client ID
mqtt_server = '192.168.1.65'
client_id = ubinascii.hexlify(machine.unique_id())
topic = '/home/living'


# Connects to MQTT Broker
def connect():
  print('Connecting to MQTT Broker...')
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  client.user = config.mqttUser
  client.pswd = config.mqttPass
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def get_readings():

  d.measure()
  print("Temperature = {}".format(d.temperature()))
  print("Humidity = {}%".format(d.humidity()))
  return round(d.temperature(),1), round(d.humidity(),1)
 
# # Posts data to IFTTT service for Google Sheets integration.
# def post_IFTTT_data(temp, humid):
#   data = "?value1=Office&value2={}&value3={}".format(temp, humid)
#   print("Making post to " + hook_url + data)
#   response = urequests.post(hook_url + data)
#   if response.status_code != 200:
#     print("Failed to post data, device will reset and try again.")
#     machine.reset()
#   print(response.text)
#   print("Posting humidity data")
#   print("Posting temp data")
#   
#   return

# Posts data to MQTT service
def post_MQTT_data(temp, humid):
    json_data = '{{"temperature" : {0}, "humidity" : {1} }}'.format(float(temp), float(humid))
    client.publish(topic,json_data)

try:
  client = connect()
except OSError as e:
  restart_and_reconnect()


while True:    
    temp, humidity = get_readings()
    post_MQTT_data(temp, humidity)
    sleep(30)


# deepsleep(270000)







