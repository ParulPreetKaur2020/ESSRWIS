from database_connection import cursor



def get_clientcordinates(clientname):
      getting_client_coordinates = "SELECT * FROM public.client_latlong where client_latlong.client_name=%s"
      connectedclientname=[clientname]
      cursor.execute(getting_client_coordinates,connectedclientname)
      rows_coordinates = cursor.fetchall()
      return(rows_coordinates)


def get_clienttableinfo(clientname):
      getting_client_coordinates = "SELECT * FROM public.client_latlong where client_latlong.client_name=%s"
      connectedclientname=[clientname]
      cursor.execute(getting_client_coordinates,connectedclientname)
      rows_coordinates = cursor.fetchall()
      return(rows_coordinates)

def get_RSUcoordinates():
      getting_RSU_coordinates = "SELECT * FROM public.client_latlong where client_latlong.client_name=%s"
      connectedclientname=['RSU']
      cursor.execute(getting_RSU_coordinates, connectedclientname)
      rows_RSU_coordinates = cursor.fetchall()
      return(rows_RSU_coordinates)




