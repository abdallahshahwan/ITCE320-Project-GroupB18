import socket
import json
import tkinter as tk
import time
from tabulate import tabulate

hostname = '127.0.0.1'
portNumber = 2003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
    cs.connect((hostname, portNumber))


    # sending the name and airport NO
    def information():
        name = input('Enter your name please -> ')
        cs.send(name.encode('ascii'))


    # function of arrival flights
    def arrival_flight():
        # creating variable a dictionary to send the data with the option number and the value of the search
        choice = {"option": 1, "value_search": None}
        choice1 = json.dumps(choice)
        cs.sendall(choice1.encode())
        data = cs.recv(19999)
        data = data.decode()
        data = json.loads(data)

        headers = ['IATA', 'Airport', 'Arrival', 'Terminal', 'Gate']
        return data, headers


    # function of delayed flights
    def delayed():
        choice = {"option": 2, "value_search": None}
        choice = json.dumps(choice)
        cs.send(choice.encode())
        data = cs.recv(19999)
        data = json.loads(data)

        headers = ['IATA', 'Airport', 'Arrival', 'Terminal', 'Delay', 'Gate']

        return data, headers


    # function of city information
    def City_info():
        City_name = input("Enter the name of the city you are looking for: ")
        choice = {"option": 3, "value_search": City_name}
        choice = json.dumps(choice)
        cs.send(choice.encode())
        data = cs.recv(19999)
        data = json.loads(data)

        headers = ['IATA', 'Departure', 'Arrival', 'Terminal', 'Departure Gate', 'Arrival Gate', 'Status']

        return data, headers


    # function of flight details
    def specific_flight():
        flight_NO = input("Enter the flight number: ")
        choice = {"option": 4, "value_search": flight_NO}
        choice = json.dumps(choice)
        cs.send(choice.encode())
        data = cs.recv(19999)
        data = json.loads(data)

        headers = ['IATA', 'Airport', 'Departure Gate', 'Departure Terminal', 'Arrival Airport', 'Gate', 'Terminal',
                   'Status', 'Departure Time', 'Scheduled']

        return data, headers


    # function of exit
    def function_exit():
        choice = {"option": 'exit', "value_search": None}
        choice = json.dumps(choice)
        cs.send(choice.encode())


    # function main menu
    def main_menu():
        information()

        while True:
            print("[1] View all arrived flights")
            print("[2] View all delayed flights")
            print("[3] View all flights from a specific city")
            print("[4] View details of a particular flight")
            print("[5] Exit")

            choice = input("\nEnter your choice: ")
            if choice == '1':
                data, headers = arrival_flight()
            elif choice == '2':
                data, headers = delayed()
            elif choice == '3':
                data, headers = City_info()
            elif choice == '4':
                data, headers = specific_flight()
            elif choice == '5':
                function_exit()
                break
            else:
                print("Invalid choice")

            # print the data type dictionary in a nice table format
            print(tabulate(data, headers=headers, tablefmt='pretty'))


    main_menu()
