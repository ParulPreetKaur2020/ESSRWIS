from database_connection import cursor, connection
import json
from datetime import datetime
import psycopg2

def get_weatherdetails():
  try:
    postgreSQL_select_Query="SELECT * FROM project_weather"
    cursor.execute(postgreSQL_select_Query)
    tuple1 = {}
    weatherdetails = cursor.fetchall()
    return(weatherdetails)


  finally:
    print("data fetched successfully")

def get_roadinfo():
  try:
    postgreSQL_select_Query="SELECT * FROM project_roadinfo"
    cursor.execute(postgreSQL_select_Query)
    rows_roadinfo = cursor.fetchall()
    return(rows_roadinfo)

  finally:
    print("Data fetched from roadinfo table")

def get_clientdirectionfromdb():
  try:
    postgreSQL_clientdirection="SELECT * FROM client_directions"
    cursor.execute(postgreSQL_clientdirection)
    clientdirectioninfo = cursor.fetchall()
    return(clientdirectioninfo)

  finally:
    print("Data fetched from client_directions table")

def get_V2ISafety():
  try:
    select_Query_V2I="SELECT * FROM project_intersectionwarning"
    cursor.execute(select_Query_V2I)
    rows_intersectionwarning = cursor.fetchall()
    return(rows_intersectionwarning)

  finally:
    print("Data fetched from intersectionwarning table")


def get_minoraccidents():
  try:
    postgreSQL_select_Query="SELECT * FROM project_minoraccident"
    cursor.execute(postgreSQL_select_Query)
    rows_minoraccident = cursor.fetchall()
    return(rows_minoraccident)

  finally:
    print("Data fetched from minoraccident table")

def get_minortraffic():
  try:
    postgreSQL_minortraffic="SELECT * FROM project_minortraffic"
    cursor.execute(postgreSQL_minortraffic)
    rows_minortraffic = cursor.fetchall()
    return(rows_minortraffic)

  finally:
    print("Data fetched from minortraffic table")

def get_emergencyinfo():
  try:
    emergencyquery='SELECT * FROM "Emergency communication"'
    cursor.execute(emergencyquery)
    rows_emeregency = cursor.fetchall()
    return(rows_emeregency)

  finally:
    print("Data fetched from emergency table")


def get_latlonginfo():
    try:
        postgreSQL_latlonginfo = "SELECT * FROM client_latlong"
        cursor.execute(postgreSQL_latlonginfo)
        rows_latlong = cursor.fetchall()
        return (rows_latlong)


    finally:
        print("Data fetched from minoraccident table")


def sensor_clientlocation_from_Client1(Topic, client_loc):
      try:
          client_info=client_loc.split(':')
          select_clientdirectioninfo = 'select "Name" from client_directions'
          cursor.execute(select_clientdirectioninfo)
          directioninfo = cursor.fetchall()
          if (client_info[0]==directioninfo[0][0]):
              print(client_info[0]+"Row already present")
          elif(client_info[0]==directioninfo[1][0]):
              print(client_info[0]+"Row already present")
          else:
             postgres_insert_query1 = """ INSERT INTO client_directions ("Name" , client_direction) VALUES (%s,%s)"""
             record1_to_insert = (client_info[0], client_info[1])
             cursor.execute(postgres_insert_query1, record1_to_insert)
             connection.commit()
             count = cursor.rowcount
             print(count, "Record inserted successfully into client_directions table")
      finally:
          print("Inserted successfully")
          return(directioninfo[0][0])


def sensor_clientlatlong_from_Client1(Topic, client_latlong):
    try:
        now = datetime.now()
        client_latlong = client_latlong.split(':')
        clientinfo = "select client_name from client_latlong"
        cursor.execute(clientinfo)
        client_nameinfo = cursor.fetchall()
        client_namelist = [item for t in client_nameinfo for item in t]
        if(client_latlong[0] in client_namelist):
            postgres_update_client_latlong = """update public.client_latlong set latitude= %s, longitude =%s ,created_time= %s where client_name=%s"""
            cursor.execute(postgres_update_client_latlong, (client_latlong[1], client_latlong[2],now ,client_latlong[0]))

        else:
          insert_client_latlong = """ INSERT INTO public.client_latlong (client_name,latitude,longitude,created_time) VALUES (%s,%s,%s,%s)"""
          recordclientlatlong_to_insert = (client_latlong[0], client_latlong[1], client_latlong[2],now)
          cursor.execute(insert_client_latlong, recordclientlatlong_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into client_latlong table")
    finally:
        print("Inserted successfully")


def sensor_traffic_Handler_from_Client1(Topic, jsonData):
      try:
        json_Dict = json.loads(jsonData)
        traffic = json_Dict['traffic']
        directions = json_Dict['directions']
        select_minortraffic ="select direction from project_minortraffic"
        cursor.execute(select_minortraffic)
        trafficinfo = cursor.fetchall()
        if(trafficinfo[0][0] == directions) :
             postgres_insert_queryupdate="""update project_minortraffic set traffic= %s where direction =%s"""
             cursor.execute(postgres_insert_queryupdate, (traffic,trafficinfo[0][0]))
        elif(trafficinfo[2][0] == directions):
            postgres_insert_queryupdate2 = """update project_minortraffic set traffic= %s where direction =%s"""
            cursor.execute(postgres_insert_queryupdate2, (traffic, trafficinfo[2][0]))
        elif(trafficinfo[3][0] == directions):
            postgres_insert_queryupdate3 = """update project_minortraffic set traffic= %s where direction =%s"""
            cursor.execute(postgres_insert_queryupdate3, (traffic, trafficinfo[3][0]))
        else :
             postgres_insert_queryupdate3 = """update project_minortraffic set traffic= %s where direction =%s"""
             cursor.execute(postgres_insert_queryupdate3, (traffic, trafficinfo[1][0]))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into minortraffic table")
        return(directions)


      finally:
        print("Inserted successfully")


def sensor_accident_Handler_from_Client1(Topic, jsonData):
  try:
     json_Dict = json.loads(jsonData)
     accident = json_Dict['accident']
     Direction = json_Dict['direction']
     select_minoraccident = "select direction from project_minoraccident"
     cursor.execute(select_minoraccident)
     accidentinfo = cursor.fetchall()

     if (accidentinfo[0][0] == Direction):
         postgres_queryupdate_accident = """update project_minoraccident set minor_accident= %s where direction =%s"""
         cursor.execute(postgres_queryupdate_accident, (accident, accidentinfo[0][0]))
     elif(accidentinfo[2][0] == Direction):
         postgres_queryupdate2_accident = """update project_minoraccident set minor_accident= %s where direction =%s"""
         cursor.execute(postgres_queryupdate2_accident, (accident, accidentinfo[2][0]))
     elif (accidentinfo[3][0] == Direction):
         postgres_queryupdate3_accident = """update project_minoraccident set minor_accident= %s where direction =%s"""
         cursor.execute(postgres_queryupdate3_accident, (accident, accidentinfo[3][0]))
     else:
         postgres_queryupdate4_accident = """update project_minoraccident set minor_accident= %s where direction =%s"""
         cursor.execute(postgres_queryupdate4_accident, (accident, accidentinfo[1][0]))
     connection.commit()
     count = cursor.rowcount
     print(count, "Record inserted successfully in table")
     return(Direction)


  finally:
    print("Insert into minor accident table")


def roadcond():
    postgreSQL_select_Query_roadcond = 'SELECT "Alert Message", "Road_Condition" FROM public."RoadConditions";'
    cursor.execute(postgreSQL_select_Query_roadcond)
    rows_surface = cursor.fetchall()
    return(rows_surface)




def get_surfacedata():
  try:
    postgreSQL_select_Query_surface='SELECT "Surface_Condition", "Surface_temp" FROM public."RWIS"'
    cursor.execute(postgreSQL_select_Query_surface)
    rows_surface = cursor.fetchall()
    return(rows_surface)

  finally:
    print("Data fetched from minoraccident table")
