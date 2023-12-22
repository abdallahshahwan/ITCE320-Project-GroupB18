import socket
import json
from urllib.request import urlopen
import urllib.error
from urllib.parse import urlparse, urlunparse
import requests

# Initialize socket
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 2003))
ss.listen(3)

# Retrieve data from aviationstack.com API
def retrieve_data(icao):
    parameters={
   'access_key':"316ce124f307821e3edb5a24098435f8",
   'arr_icao':icao,
   'limit':100
    }
    url = "http://api.aviationstack.com/v1/flights"
    api_response = requests.get(url,parameters)
    json_result= json.dumps(api_response.json(), indent=3)
    return json_result

# Save data to JSON file
def save_data(data, icao):
    with open(f"group_{icao}.json", "w") as json_file:
        json.dump(data, json_file)

# Handle client requests
class server_thread(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def run(self):
        print(f"Connection received from {self.connection.address} on port {self.connection.getpeercert()[1]}")
        print("Welcome, to Avigate!\nEnter ICAO code:")
        arr_icao = self.connection.recv(1024).decode("ascii")
        icao_data = retrieve_data(arr_icao)
        save_data(icao_data, arr_icao)

        while True:
            request = self.connection.recv(1024).decode("ascii")
            if request == "QUIT":
                break

            elif request.startswith("ARRIVED FLIGHTS"):
                arrive_flights = []
                for flight in icao_data["response"]["flights"]:
                    if flight["flight_status"] == "landed":
                        arrive_flights.append((flight["iata"], flight["departure_airport"], flight["arrival_time"], flight["terminal"], flight["gate"]))
                self.connection.sendall(bytes(arrive_flights, "utf-8"))

            elif request.startswith("DELAYED FLIGHTS"):
                delayed_flights = []
                for flight in icao_data["response"]["flights"]:
                    if flight["flight_status"] == "delayed":
                        delayed_flights.append((flight["iata"], flight["departure_airport"], flight["original_departure_time"], flight["estimated_arrival_time"], flight["terminal"], flight["gate"], flight["delay"]))
                self.connection.sendall(bytes(delayed_flights, "utf-8"))

            elif request.startswith("FLIGHTS FROM"):
                origin_icao = request.split(" ")[1]
                flights = []
                for flight in icao_data["response"]["flights"]:
                    if flight["origin_icao"] == origin_icao:
                        flights.append((flight["iata"], flight["departure_airport"], flight["original_departure_time"], flight["estimated_arrival_time"], flight["terminal"], flight["gate"], flight["status"]))
                self.connection.sendall(bytes(flights, "utf-8"))

            elif request.startswith("Flight "):
                flight_iata = request.split(" ")[1]
                flight_data = None
                for flight in icao_data["response"]["flights"]:
                    if flight["iata"] == flight_iata:
                        flight_data = flight
                        break
                if flight_data is None:
                    self.connection.sendall(bytes("No such flight", "utf-8"))
                else:
                    self.connection.sendall(bytes(flight_data, "utf-8"))

            else:
                self.connection.sendall(bytes("Invalid request", "utf-8"))