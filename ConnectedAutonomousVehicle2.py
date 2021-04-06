import _thread
import time
import paho.mqtt.client as mqtt
import requests
from config import *
import json
import math
import random
from Collectingcoordinates import get_points_along_path,generate_polyline
from computeclientdist import get_clienttableinfo,get_clientcordinates,get_RSUcoordinates

cname = "VehicleV02"
connection_status_topic="sensors/connected/"+cname

def on_disconnect(client, userdata, flags, rc=0):
    m="DisConnected flags"+"result code "+str(rc)
    print(m)
    client.connected_flag=False

# Callback Function on Connection with MQTT Server
def on_connect( client, userdata, flags, rc):
 if rc == 0:
    print("Connected to RSU 417")
    #print("Connected to RSU 417 with Code :" +str(rc))
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
client.will_set(connection_status_topic,"VehicleV02:Disconnected",0,True)
client.connect(mqtt_server_host, mqtt_server_port, mqtt_keepalive)
client.loop_start()


time.sleep(1)
client.publish(connection_status_topic,"VehicleV02:Connected",0,True)#use retain flag

def updatingGPS(threadName,delay):
    points = get_points_along_path(api_key, "230+Woodridge+Crescent", "7+Saxton+Private",cname)
    polyline = generate_polyline(points)

def publishing_client2(threadName,delay):
    Data_client2 = {}
    Data1_client2 = {}
    Data_client2['accident'] = "accident on lane 88:Switch to lane 63"
    Data_client2['direction'] = "West to East"
    Data1_client2['traffic'] = " Avoid highway 461"
    Data1_client2['directions'] = "West to East"
    Data_json_data_client2 = json.dumps(Data_client2)
    Data_json_data1_client2 = json.dumps(Data1_client2)
    endpoint2 = "https://maps.googleapis.com/maps/api/directions/json?"
    origin2 = '230+Woodridge+Crescent'
    destination2 = '1177+Belanger+Avenue'
    nav_request2 = 'origin={} &destination={} &key={}'.format(origin2, destination2, api_key)
    request2 = endpoint2 + nav_request2
    r2 = requests.get(request2)
    decodedRes2 = r2.text
    ###converting json to dictionary
    json_object2 = json.loads(decodedRes2)
    direction2 = json_object2["routes"][0]["bounds"]
    car2directions = []
    car2latlong = []
    for key, value in direction2.items():
        car2directions.append(key)
        car2latlong.append(value)
    client.publish("client1/direction", 'VehicleV01' + ':' + car2directions[0] + ' to ' + car2directions[1])
    time.sleep(10)
    client.publish("client1/accident", Data_json_data_client2)
    time.sleep(10)
    client.publish("client1/traffic", Data_json_data1_client2)
    time.sleep(10)

def subscribing_client2(threadName, delay):
    number = random.uniform(0, 1)
    if (number <= 0.25):
        # print(number)
        client.subscribe("SouthtoNorth/weather/#")
        client.subscribe("SouthtoNorth/minoraccident1")
        client.subscribe("SouthtoNorth/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client2lat = latlonginfo[0][1]
            client2lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client2 = 6373.0
            Distance_client2 = []
            lat1_client2 = math.radians(float(client2lat))
            long1_client2 = math.radians(float(client2lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client2 = long2_RSU - long1_client2
            dlat_client2 = lat2_RSU - lat1_client2
            a_client2 = math.sin(dlat_client2 / 2) ** 2 + math.cos(lat1_client2) * math.cos(lat2_RSU) * math.sin(
                dlon_client2 / 2) ** 2
            c_client2 = 2 * math.atan2(math.sqrt(a_client2), math.sqrt(1 - a_client2))
            distance_client2 = R_client2 * c_client2
            Distance_client2.append(distance_client2)
            if (distance_client2 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/SouthtoNorth/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/SouthtoNorth/#")


            elif (2 < distance_client2 <= 5):
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
        # print(number)
        client.subscribe("NorthtoSouth/weather/#")
        client.subscribe("NorthtoSouth/minoraccident1")
        client.subscribe("NorthtoSouth/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client2lat = latlonginfo[0][1]
            client2lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client2 = 6373.0
            Distance_client2 = []
            lat1_client2 = math.radians(float(client2lat))
            long1_client2 = math.radians(float(client2lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client2 = long2_RSU - long1_client2
            dlat_client2 = lat2_RSU - lat1_client2
            a_client2 = math.sin(dlat_client2 / 2) ** 2 + math.cos(lat1_client2) * math.cos(lat2_RSU) * math.sin(
                dlon_client2 / 2) ** 2
            c_client2 = 2 * math.atan2(math.sqrt(a_client2), math.sqrt(1 - a_client2))
            distance_client2 = R_client2 * c_client2
            Distance_client2.append(distance_client2)
            if (distance_client2 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/NorthtoSouth/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/NorthtoSouth/#")

            elif (2 < distance_client2 <= 5):
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
            client2lat = latlonginfo[0][1]
            client2lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client2 = 6373.0
            Distance_client2 = []
            lat1_client2 = math.radians(float(client2lat))
            long1_client2 = math.radians(float(client2lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client2 = long2_RSU - long1_client2
            dlat_client2 = lat2_RSU - lat1_client2
            a_client2 = math.sin(dlat_client2 / 2) ** 2 + math.cos(lat1_client2) * math.cos(lat2_RSU) * math.sin(
                dlon_client2 / 2) ** 2
            c_client2 = 2 * math.atan2(math.sqrt(a_client2), math.sqrt(1 - a_client2))
            distance_client2 = R_client2 * c_client2
            Distance_client2.append(distance_client2)

            if (distance_client2 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/WesttoEast/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/WesttoEast/#")

            elif (2 < distance_client2 <= 5):
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
        # print(number)
        client.subscribe("EasttoWest/weather/#")
        client.subscribe("EasttoWest/minoraccident1")
        client.subscribe("EasttoWest/minortraffic")
        rows_clientlatlong = len(get_clienttableinfo(cname))
        while (rows_clientlatlong):
            latlonginfo = get_clientcordinates(cname)
            latlong_RSU = get_RSUcoordinates()
            client2lat = latlonginfo[0][1]
            client2lng = latlonginfo[0][2]
            RSU_lat = latlong_RSU[0][1]
            RSU_lng = latlong_RSU[0][2]
            R_client2 = 6373.0
            Distance_client2 = []
            lat1_client2 = math.radians(float(client2lat))
            long1_client2 = math.radians(float(client2lng))
            lat2_RSU = math.radians(float(RSU_lat))
            long2_RSU = math.radians(float(RSU_lng))
            dlon_client2 = long2_RSU - long1_client2
            dlat_client2 = lat2_RSU - lat1_client2
            a_client2 = math.sin(dlat_client2 / 2) ** 2 + math.cos(lat1_client2) * math.cos(lat2_RSU) * math.sin(
                dlon_client2 / 2) ** 2
            c_client2 = 2 * math.atan2(math.sqrt(a_client2), math.sqrt(1 - a_client2))
            distance_client2 = R_client2 * c_client2
            Distance_client2.append(distance_client2)

            if (distance_client2 <= 2):
                print("You are in Critical Zone")
                client.subscribe("client/critical_zone/EasttoWest/#")
                time.sleep(20)
                client.unsubscribe("client/critical_zone/EasttoWest/#")

            elif(2<distance_client2 <= 5):
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
   _thread.start_new_thread( publishing_client2, ("PubThread-1", 2, ) )
   _thread.start_new_thread( subscribing_client2, ("SubThread-2", 4, ) )
   _thread.start_new_thread(updatingGPS, ("GpsThread-3", 0,))
except:
   print ("Error: unable to start thread")

while 1:
   pass

client.loop_stop()
print("updating status and disconnecting")
client.publish(connection_status_topic,"Client 2 Disconnnected",0,True)
client.disconnect()



