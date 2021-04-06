import googlemaps
from googlemaps.convert import decode_polyline, encode_polyline
import time
from datetime import datetime
import math
import numpy
from collections import OrderedDict
import paho.mqtt.client as mqtt


def on_connect( client, userdata, flags, rc):
 if rc == 0:
    print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    client.subscribe("emergency/#")
    #client.subscribe("client1/latlong")
 else:
     print("Bad connection Returned code=", rc)
     client.bad_connection_flag = True
# Callback Function on Receiving the Subscribed Topic/Message
def on_message( client, userdata, msg):
    # print the message received from the subscribed topic
    print("Received message payload: {0}".format(str(msg.payload)))
    message_testing = msg.payload.decode("utf-8")
    #if (msg.topic =="client1/latlong"):
     #    sensor_clientlatlong_from_Client1(msg.topic, message_testing)

mqtt.Client.connected_flag=False #create flags
mqtt.Client.bad_connection_flag=False #
mqtt.Client.retry_count=0 #

client = mqtt.Client()    #create new instance
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_start()


def _compute_distance(origins, destinations):
    """
    Calculate the Haversine distance.

    """
    lattitude1, longitude1 = origins['lat'], origins['lng']
    lattitude2, longitude2 = destinations['lat'], destinations['lng']
    radius = 6371000  # metres

    dlatitude = math.radians(lattitude2 - lattitude1)
    dlongitude = math.radians(longitude2 - longitude1)
    a = (math.sin(dlatitude / 2) * math.sin(dlongitude / 2) +
         math.cos(math.radians(lattitude1)) * math.cos(math.radians(lattitude2)) *
         math.sin(dlongitude / 2) * math.sin(dlongitude / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def _rounditup_time(time, period):

    # If time is an exact multiple of period, don't round up
    if time % period == 0:
        return time

    time = round(time)
    return time + period - (time % period)


def _filling_missing_times(times, lats, lngs, period):
    starting_time = times[0]
    ending_time = times[-1]

    new_times = range(starting_time, ending_time + 1, period)
    new_lattitudes = numpy.interp(new_times, times, lats).tolist()
    new_longitudes = numpy.interp(new_times, times, lngs).tolist()

    return new_times, new_lattitudes, new_longitudes


def get_points_along_path(maps_api_key, _from, _to,cname, departure_time=None, period=5):

    if not departure_time:
        departure_time = datetime.now()

    gmaps = googlemaps.Client(key=maps_api_key)
    directions = gmaps.directions(_from, _to, departure_time=departure_time)
    clientName=cname
    steps = directions[0]['legs'][0]['steps']
    all_latitudes = []
    all_lngitudes = []
    all_times = []

    step_start_duration = 0
    step_end_duration = 0

    for step in steps:
        step_end_duration += step['duration']['value']
        points = decode_polyline(step['polyline']['points'])
        distances = []
        lats = []
        lngs = []
        start = None
        for point in points:
            client.publish("client1/latlong", clientName + ':' + str(point['lat']) + ':' + str(point['lng']))
            if not start:
                start = point
                distance = 0
            else:
                distance = _compute_distance(start, point)
            distances.append(distance)
            lats.append(point['lat'])
            lngs.append(point['lng'])
            time.sleep(40)

        missing_times = numpy.interp(distances[1:-1], [distances[0], distances[-1]],
                                     [step_start_duration, step_end_duration]).tolist()
        times = [step_start_duration] + missing_times + [step_end_duration]
        times = [_rounditup_time(t, period) for t in times]

        times, lats, lngs = _filling_missing_times(times, lats, lngs, period)

        all_latitudes += lats
        all_lngitudes += lngs
        all_times += times

        step_start_duration = step_end_duration

    points = OrderedDict()
    for p in zip(all_times, all_latitudes, all_lngitudes):
        points[p[0]] = (round(p[1], 5), round(p[2], 5))

    return points


def generate_polyline(points):
    return encode_polyline(points.values())






