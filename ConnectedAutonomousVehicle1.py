import _thread
import time
import paho.mqtt.client as mqtt
import requests
from config import *
import json
import math
import csv
import random
from Collectingcoordinates import get_points_along_path,generate_polyline
from computeclientdist import get_clienttableinfo,get_clientcordinates,get_RSUcoordinates


cname = "VehicleV01"
connection_status_topic="sensors/connected/"+cname

def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)
    print(m)
    client.connected_flag=False

# Callback Function on Connection with MQTT Server
def on_connect( client, userdata, flags, rc):
 if rc == 0:
    print("Connected to RSU 417")
    #print("Connected  with Code :" + str(rc))
    # Subscribe Topic from here
    client.subscribe("emergency/#")
 else:
     print("Bad connection Returned code=", rc)
     client.bad_connection_flag = True
# Callback Function on Receiving the Subscribed Topic/Message
def on_message( client, userdata, msg):
    # print the message received from the subscribed topic
    print("Received safety message: {0} ".format(str(msg.payload.decode("utf-8"))))

mqtt.Client.connected_flag=False #create flags
mqtt.Client.bad_connection_flag=False #
mqtt.Client.retry_count=0 #

client = mqtt.Client(cname)    #create new instance
client.on_connect = on_connect
client.on_message = on_message
client.will_set(connection_status_topic,"VehicleV01:Disconnected",0,True)
client.connect(mqtt_server_host, mqtt_server_port, mqtt_keepalive)
client.loop_start()


time.sleep(1)
client.publish(connection_status_topic,"VehicleV01:Connected",0,True)#use retain flag


def updatingGPS(threadName,delay):
    points = get_points_along_path(api_key, "249+Craig+Henry", "333+Palladium+Drive",cname)
    #points = get_points_along_path(api_key, "1177+Belanger+Avenue", "333+Palladium+Drive", cname)
    polyline = generate_polyline(points)

def publishing_client1(threadName,delay):
    Data = {}
    Data1 = {}
    Data['accident'] = "accident on lane 12:Switch to lane 13"
    Data['direction'] = "North to South"
    Data1['traffic'] = " Congestion on lane 5"
    Data1['directions'] = "South to North"
    Data_json_data = json.dumps(Data)
    Data_json_data1 = json.dumps(Data1)
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
    origin = 'Ottawa'
    destination = 'Brampton'
    nav_request = 'origin={} &destination={} &key={}'.format(origin, destination, api_key)
    request = endpoint + nav_request
    r = requests.get(request)
    decodedRes = r.text
        ###converting json to dictionary
    json_object = json.loads(decodedRes)
    direction = json_object["routes"][0]["bounds"]
    cardirections = []
    carlatlong = []
    for key, value in direction.items():
       cardirections.append(key)
       carlatlong.append(value)

    client.publish("client1/direction", 'VehicleV01' + ':' + cardirections[0] + ' to ' + cardirections[1])
    time.sleep(10)
    client.publish("client1/accident", Data_json_data)
    time.sleep(10)
    client.publish("client1/traffic", Data_json_data1)


def subscribing_client(threadName, delay):
    number = random.uniform(0, 1)
    if (number <= 0.25):
        client.subscribe("SouthtoNorth/weather/#")
        client.subscribe("SouthtoNorth/minoraccident1")
        client.subscribe("SouthtoNorth/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client1lat = latlonginfo[0][1]
            client1lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client1 = 6373.0
            Distance_client1 = []
            lat1_client1 = math.radians(float(client1lat))
            long1_client1 = math.radians(float(client1lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client1 = long2_RSU - long1_client1
            dlat_client1 = lat2_RSU - lat1_client1
            a_client1 = math.sin(dlat_client1 / 2) ** 2 + math.cos(lat1_client1) * math.cos(lat2_RSU) * math.sin(dlon_client1 / 2) ** 2
            c_client1 = 2 * math.atan2(math.sqrt(a_client1), math.sqrt(1 - a_client1))
            distance_client1 = R_client1 * c_client1
            Distance_client1.append(distance_client1)
            if (distance_client1 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/SouthtoNorth/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/SouthtoNorth/#")
            elif (2 < distance_client1 <= 5):
                print("You are in Safe Zone")
                client.subscribe("client/safe_zone/SouthtoNorth/#")
                time.sleep(20)
                client.unsubscribe("client/safe_zone/SouthtoNorth/#")
            else:
                client.unsubscribe("SouthtoNorth/weather/#")
                client.unsubscribe("SouthtoNorth/minoraccident1")
                client.unsubscribe("SouthtoNorth/minortraffic")
        time.sleep(300)
        client.unsubscribe("SouthtoNorth/weather/#")
        client.unsubscribe("SouthtoNorth/minoraccident1")
        client.unsubscribe("SouthtoNorth/minortraffic")
    elif (number > 0.25 and number <= 0.5):
        client.subscribe("NorthtoSouth/weather/#")
        client.subscribe("NorthtoSouth/minoraccident1")
        client.subscribe("NorthtoSouth/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client1lat = latlonginfo[0][1]
            client1lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client1 = 6373.0
            Distance_client1 = []
            lat1_client1 = math.radians(float(client1lat))
            long1_client1 = math.radians(float(client1lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client1 = long2_RSU - long1_client1
            dlat_client1 = lat2_RSU - lat1_client1
            a_client1 = math.sin(dlat_client1 / 2) ** 2 + math.cos(lat1_client1) * math.cos(lat2_RSU) * math.sin(dlon_client1 / 2) ** 2
            c_client1 = 2 * math.atan2(math.sqrt(a_client1), math.sqrt(1 - a_client1))
            distance_client1 = R_client1 * c_client1
            Distance_client1.append(distance_client1)
            if (distance_client1 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/NorthtoSouth/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/NorthtoSouth/#")
            elif (2 < distance_client1 <= 5):
                print("You are in Safe Zone")
                client.subscribe("client/safe_zone/NorthtoSouth/#")
                time.sleep(20)
                client.unsubscribe("client/safe_zone/NorthtoSouth/#")
            else:
                client.unsubscribe("NorthtoSouth/minoraccident1")
                client.unsubscribe("NorthtoSouth/minortraffic")
                client.unsubscribe("NorthtoSouth/weather/#")

        time.sleep(300)
        client.unsubscribe("NorthtoSouth/minoraccident1")
        client.unsubscribe("NorthtoSouth/minortraffic")
        client.unsubscribe("NorthtoSouth/weather/#")
    elif (number > 0.5 and number <= 0.75):
        client.subscribe("WesttoEast/weather/#")
        client.subscribe("WesttoEast/minoraccident1")
        client.subscribe("WesttoEast/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client1lat = latlonginfo[0][1]
            client1lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client1 = 6373.0
            Distance_client1 = []
            lat1_client1 = math.radians(float(client1lat))
            long1_client1 = math.radians(float(client1lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client1 = long2_RSU - long1_client1
            dlat_client1 = lat2_RSU - lat1_client1
            a_client1 = math.sin(dlat_client1 / 2) ** 2 + math.cos(lat1_client1) * math.cos(lat2_RSU) * math.sin(dlon_client1 / 2) ** 2
            c_client1 = 2 * math.atan2(math.sqrt(a_client1), math.sqrt(1 - a_client1))
            distance_client1 = R_client1 * c_client1
            Distance_client1.append(distance_client1)

            if (distance_client1 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/WesttoEast/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/WesttoEast/#")


            elif (2 < distance_client1 <= 5):
                print("You are in Safe Zone")
                client.subscribe("client/safe_zone/WesttoEast/#")
                time.sleep(20)
                client.unsubscribe("client/safe_zone/WesttoEast/#")
            else:
                client.unsubscribe("WesttoEast/weather/#")
                client.unsubscribe("WesttoEast/minoraccident1")
                client.unsubscribe("WesttoEast/minortraffic")
        time.sleep(300)
        client.unsubscribe("WesttoEast/weather/#")
        client.unsubscribe("WesttoEast/minoraccident1")
        client.unsubscribe("WesttoEast/minortraffic")

    else:

        client.subscribe("EasttoWest/weather/#")
        client.subscribe("EasttoWest/minoraccident1")
        client.subscribe("EasttoWest/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client1lat = latlonginfo[0][1]
            client1lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client1 = 6373.0
            Distance_client1 = []
            lat1_client1 = math.radians(float(client1lat))
            long1_client1 = math.radians(float(client1lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client1 = long2_RSU - long1_client1
            dlat_client1 = lat2_RSU - lat1_client1
            a_client1 = math.sin(dlat_client1 / 2) ** 2 + math.cos(lat1_client1) * math.cos(lat2_RSU) * math.sin(dlon_client1 / 2) ** 2
            c_client1 = 2 * math.atan2(math.sqrt(a_client1), math.sqrt(1 - a_client1))
            distance_client1 = R_client1 * c_client1
            Distance_client1.append(distance_client1)

            if (distance_client1 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/EasttoWest/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/EasttoWest/#")

            elif (2 < distance_client1 <= 5):
                print("You are in Safe Zone")
                client.subscribe("client/safe_zone/EasttoWest/#")
                time.sleep(20)
                client.unsubscribe("client/safe_zone/EasttoWest/#")
            else:
                client.unsubscribe("EasttoWest/weather/#")
                client.unsubscribe("EasttoWest/minoraccident1")
                client.unsubscribe("EasttoWest/minortraffic")
        time.sleep(300)
        client.unsubscribe("EasttoWest/weather/#")
        client.unsubscribe("EasttoWest/minoraccident1")
        client.unsubscribe("EasttoWest/minortraffic")

try:
   _thread.start_new_thread( publishing_client1, ("PubThread-1", 2, ) )
   _thread.start_new_thread( subscribing_client, ("SubThread-2", 4, ) )
   _thread.start_new_thread(updatingGPS, ("GpsThread-3", 0,))
except:
   print ("Error: unable to start thread")

while 1:
   pass

client.loop_stop()
print("updating status and disconnecting")
client.publish(connection_status_topic,"Client 1 Disconnnected",0,True)
client.disconnect()


