import socket,threading,json,requests,sys

icao= input('Enter the ICAO of the airport:')

def get_info(airport_icao):
 
 while True: 
    parameters={
    'access_key':"316ce124f307821e3edb5a24098435f8",
    'arr_icao':icao,
    'limit':100
        }
    url = "http://api.aviationstack.com/v1/flights"

    data= requests.get(url,parameters)
    response= json.dumps(data)

    if "error" not in response: 
      print("Received!")
      

