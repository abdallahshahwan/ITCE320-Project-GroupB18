import json, threading, socket, urllib.request, sys

# main function with try and except and create a thread to handle the client
airport_code = input('Enter the ICAO of airport -> ')


def flight_info(airport_code):
    while True:
        key = '316ce124f307821e3edb5a24098435f8'

        data = urllib.request.urlopen(
            "http://api.aviationstack.com/v1/flights?access_key=316ce124f307821e3edb5a24098435f8&arr_icao=" + airport_code).read()
        response = json.loads(data)
        if 'error' in response:
            print("Error in Retrieving Information. Retrying...")
            continue
        else:
            print('\nInformation retrieved successfully.')
            print("\nWaiting for client requests...")
            return response


# function Store the all flight information data in a json file
def store_flight_info(flight_info):
    # open the json file
    with open('retrieved_flights.json', 'w') as file:
        # store the flight information in json file
        json.dump(flight_info, file, indent=4)


table = flight_info(airport_code)
# call the function store the flight information in json file
store_flight_info(table)  # function to retrieve flight information


def main():
    try:

        # Accept a connection
        (active_socket, client_address) = accept_connection(s)
        # create a thread to handle the client
        t = threading.Thread(target=handle_client_request, args=(active_socket, client_address))
        t.start()
    except Exception as e:
        print(e)
        return False


# function to store the flight arrive (flight information: flight number and estimated time of arrival and  terminal number) in json object
def arrive_flight_info(flight_info):
    flight_arrive_info = {'IATA': [], 'airport': [], 'estimated': [], 'terminal': [], 'gate': []}
    # loop through the flight information
    for flight in flight_info['data']:
        # if the flight is arrived
        if flight['flight_status'] == 'landed':
            # store the flight information in json object
            flight_arrive_info['IATA'].append(flight['flight']['iata'])
            flight_arrive_info['airport'].append(flight['departure']['airport'])
            flight_arrive_info['estimated'].append(flight['arrival']['estimated'])
            flight_arrive_info['terminal'].append(flight['arrival']['terminal'])
            flight_arrive_info['gate'].append(flight['arrival']['gate'])

    return flight_arrive_info


# function to store the delayed flight (flight information: flight number and estimated time of arrival and  terminal
# number) in json object
def delayed_flight_info(flight_info):
    flight_delayed_info = {'IATA': [], 'airport': [], 'estimated': [], 'terminal': [], 'delay': [], 'gate': []}
    # loop through the flight information
    for flight in flight_info['data']:
        # if the flight is delayed
        if flight['arrival']['delay'] != 'null':
            # store the flight information in json object
            flight_delayed_info['IATA'].append(flight['flight']['iata'])
            flight_delayed_info['airport'].append(flight['departure']['airport'])
            flight_delayed_info['estimated'].append(flight['arrival']['estimated'])
            flight_delayed_info['terminal'].append(flight['arrival']['terminal'])
            flight_delayed_info['delay'].append(flight['arrival']['delay'])
            flight_delayed_info['gate'].append(flight['arrival']['gate'])
    return flight_delayed_info


# function to store the for specific city  flights  (flight information: flight number and original time of arrival and  status) in json object
def city_flight_info(flight_info, city):
    flight_city_info = {'IATA': [], 'airport': [], 'estimated': [], 'terminal': [], 'dgate': [], 'gate': [],
                        'status': []}
    # loop through the flight information
    for flight in flight_info['data']:
        # if the flight is arrived
        if city in flight['departure']['timezone']:
            # store the flight information in json object
            flight_city_info['IATA'].append(flight['flight']['iata'])
            flight_city_info['airport'].append(flight['departure']['airport'])
            flight_city_info['estimated'].append(flight['arrival']['estimated'])
            flight_city_info['terminal'].append(flight['arrival']['terminal'])
            flight_city_info['dgate'].append(flight['departure']['airport'])
            flight_city_info['gate'].append(flight['arrival']['gate'])
            flight_city_info['status'].append(flight['flight_status'])

    return flight_city_info


# function to store all details about particular flight  (flight information: flight number and original time of arrival and  status and  estimated time and  terminal number)
# in json object
def flight_details(flight_info, flight_number):
    flight_city_info = {'IATA': [], 'airport': [], 'departure_gate': [], 'departure_terminal': [],
                        'arrival_airport': [], 'gate': [], 'terminal': [], 'status': [], 'departure_time': [],
                        'scheduled': []}
    # loop through the flight information
    for flight in flight_info['data']:
        # if the flight is arrived
        if flight['flight']['iata'] == flight_number:
            # store the flight information in json object
            flight_city_info['IATA'].append(flight['flight']['iata'])
            flight_city_info['airport'].append(flight['departure']['airport'])
            flight_city_info['departure_gate'].append(flight['departure']['gate'])
            flight_city_info['departure_terminal'].append(flight['departure']['terminal'])
            flight_city_info['arrival_airport'].append(flight['arrival']['airport'])
            flight_city_info['gate'].append(flight['arrival']['gate'])
            flight_city_info['terminal'].append(flight['arrival']['terminal'])
            flight_city_info['status'].append(flight['flight_status'])
            flight_city_info['departure_time'].append(flight['departure']['scheduled'])
            flight_city_info['scheduled'].append(flight['arrival']['scheduled'])

    return flight_city_info


# function search if the option is 1 or 2 or 3 or 4 then call the function to store the flight information in json object
def search_flight(client, option, value_search, flight_info):
    print(client + ' selected option ' + str(option))
    if option == 1:
        print('sending landed flights data to ' + client)
        re_flight_info = arrive_flight_info(flight_info)
    elif option == 2:
        print('sending delayed flights data to ' + client)
        re_flight_info = delayed_flight_info(flight_info)
    elif option == 3:
        print('sending flight data to ' + client)
        re_flight_info = city_flight_info(flight_info, value_search)
    elif option == 4:
        print('sending landed flights data to ' + client)
        re_flight_info = flight_details(flight_info, value_search)
    return re_flight_info


# create a list to store the online clients
online_clients = []


# function to handle the client request Wait for clients' requests to connect (should be able to accept three connections simultaneously).Accept the connection and Store the client’s name and display it on the terminal.
def handle_client_request(active_socket, id_number):
    try:

        # Receive the client's name
        client_name = active_socket.recv(1024).decode('utf-8')
        # create a json object to store the client information his name and id number
        client_info = {
            'name': client_name,
            'id': id_number
        }
        online_clients.append(client_info)
        # Display the client's name and id with the message "has connected"
        print(f'client {client_name} with id {id_number} has been connected')
        if online_clients.count != 1:
            print('Current connected clients:', *online_clients)
        flight_info_i = table

        while True:
            # Receive the client's option with value_search in json object
            client_option = active_socket.recv(1024).decode('utf-8')
            # print(client_info.get('name')+' selected option '+client_option)
            # convert the json object to python dictionary
            client_option = json.loads(client_option)
            # if the client enter exit option then break the loop
            if client_option['option'] == 'exit':
                break
            # call the function to search the flight information
            flight_info_in = search_flight(client_name, client_option['option'], client_option['value_search'],
                                           flight_info_i)
            # convert the flight information to json object  to send it to the client
            flight_info_in = json.dumps(flight_info_in)
            # Send the flight information to the client
            active_socket.sendall(flight_info_in.encode())
        # Display the client's name and id with the message "has disconnected"
        print(f'client {client_name} with id {id_number} has been disconnected')
        # remove the client from the online clients list
        online_clients.remove(client_info)
    except Exception as e:
        # print the error message
        print(e)
        print(f'client {client_name} with id {id_number} has been disconnected')
        # remove the client from the online clients list
        online_clients.remove(client_info)


def create_passive_socket(listen_limit):
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a port
    s.bind(('127.0.0.1', 2003))
    # Listen for connections
    s.listen(listen_limit)
    # Return the socket and the port number
    return s


# function to accept a connection
def accept_connection(s):
    # Accept a connection
    (active_socket, client_address) = s.accept()
    # Return the socket and the client address

    return (active_socket, client_address)


# Create a passive socket
s = create_passive_socket(3)

# if you want it secure remove the comment from the next line and comment the previous line
# create secure passive socket
# s = secure_create_passive_socket(3)

# call the main function in while loop
while True:
    # if the main function return false break the loop
    if main() == False:
        break

# close socket
s.close()