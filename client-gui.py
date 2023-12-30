from tkinter import *
from tkinter import messagebox
import socket
import json, threading , os, sys
from tabulate import tabulate

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cs:
    cs.connect(('127.0.0.1', 2003))
    def create_rounded_button(frame, x, y, width, height, text, command, stroke=True):
        button = Button(frame, text=text, command=command, bd=0 if not stroke else 2,
                        relief="solid" if stroke else "flat", font=("Arial", 12, "bold"), bg="#FFFFFF",
                        fg="#38B6FF" if stroke else "#38B6FF")
        button.place(x=x, y=y, width=width, height=height)
        return button
    
    def restart_program():
     python = sys.executable
     os.execl(python, python, *sys.argv)

    def on_button_click(menu, clicked_button):
        for button in menu:
            if button == clicked_button:
                button.config(bg=button.cget("fg"), fg="#FFFFFF")
                selection = 1
                if clicked_button == button1:
                  threading.Thread(target=arrived_flights).start()
                elif clicked_button == button2:
                  threading.Thread(target=delayed_flights).start()
                elif clicked_button == button3:
        # Destroy all existing buttons in the menu
                    for button in menu:
                     button.destroy()
                    
                    city_label = Label(root, text="Enter City Name:", font=("Poppins", 15, "italic", "bold"), fg="#000000")
                    city_label.place(x=canvas_width / 2 - 60 ,y=470)
                    city_frame = Frame(root)
                    global city_entry
                    city_entry = Entry(city_frame)
                    city_entry.place(x=canvas_width / 2 - 120, y=logo_y + logo_image.height() + 20, width=300, height=50)
                    city_frame.place(x=canvas_width / 2 - 120, y=logo_y + logo_image.height() + 20, width=300, height=50)
                    city_entry_label = Label(city_frame, text="City:")
                    city_entry_label.pack(side=LEFT, padx=10)
                    city_entry.pack(side=LEFT, padx=10)
                    city_entry_button = Button(city_frame, text="Search", command=city_flight)
                    city_entry_button.pack(side=LEFT, padx=10)
                    back_button = create_rounded_button(root, canvas_width / 2 - 100, tagline_y + 190,
                                                         button_width, button_height, "Start again",
                                                         lambda: restart_program(), stroke=False)
                    

                elif clicked_button == button4:
                    for button in menu:
                      button.destroy()  
                    flight_label = Label(root, text="Enter Flight Number:", font=("Poppins", 15, "italic", "bold"), fg="#000000")
                    flight_label.place(x=canvas_width / 2 - 60 ,y=470)
                    flight_frame = Frame(root)
                    global flight_entry
                    flight_entry = Entry(flight_frame)
                    flight_entry.place(x=canvas_width / 2 - 120, y=logo_y + logo_image.height() + 20, width=300, height=50)
                    flight_frame.place(x=canvas_width / 2 - 120, y=logo_y + logo_image.height() + 20, width=300, height=50)
                    flight_entry_label = Label(flight_frame, text="Flight:")
                    flight_entry_label.pack(side=LEFT, padx=10)
                    flight_entry.pack(side=LEFT, padx=10)
                    flight_entry_button = Button(flight_frame, text="Search", command=specific_flight)
                    flight_entry_button.pack(side=LEFT, padx=10)
                    back_button = create_rounded_button(root, canvas_width / 2 - 100, tagline_y + 190,
                                                            button_width, button_height, "Start again",
                                                            lambda: restart_program(), stroke=False)

   
            else:
                button.config(bg="#FFFFFF", fg="#38B6FF")
        show_continue(selection)


    def display_arrived_flights(cs):
    
     try:
        
        choice = {"option": 1, "value_search": None}
        choice1 = json.dumps(choice)
        cs.sendall(choice1.encode())
        data = cs.recv(19999)
        data = data.decode()
        data = json.loads(data)
        headers = ['IATA', 'Airport', 'Arrival', 'Terminal', 'Gate']
        return data, headers
     
     except Exception as e:
            print(f"Error in displaying arrived flights: {e}")
            return display_arrived_flights(cs)



    def arrived_flights():
          
            choice = {"option": 1, "value_search": None}
            choice1 = json.dumps(choice)
            cs.sendall(choice1.encode())
            top = Toplevel(root)
            top.title("Arrived Flights")

            data, headers= display_arrived_flights(cs)
            formatted_table = tabulate(data, headers=headers, tablefmt='pretty')
            # Create a Text widget in the new window
            text_widget = Text(top, wrap=WORD, width=200, height=100)
            text_widget.pack(pady=20)
            # Insert the formatted table string into the Text widget

            text_widget.insert("1.0", formatted_table)
            
            # Make the Text widget read-only
            text_widget.config(state="disabled")
            back_button = create_rounded_button(top, 1130, 50, 150, 30, "Back to Menu", top.destroy)
           
        
    def display_delayed_flights(cs):
     try:
        choice = {"option": 2, "value_search": None}
        choice2 = json.dumps(choice)
        cs.sendall(choice2.encode())
        data = cs.recv(19999)
        data = data.decode()
        data = json.loads(data)
        headers = ['IATA', 'Airport', 'Arrival', 'Terminal', 'Delay', 'Gate']
        return data, headers
     
     except Exception as e:
            print(f"Error in displaying delayed flights: {e}")
            return display_delayed_flights(cs)

    def delayed_flights():
            
            choice = {"option": 2, "value_search": None}
            choice2 = json.dumps(choice)
            cs.sendall(choice2.encode())
            data, headers = display_delayed_flights(cs)
            print("Data:", data)
            print("Headers:", headers)
            top = Toplevel(root)
            top.title("Delayed Flights")

            data, headers= display_delayed_flights(cs)
            formatted_table = tabulate(data, headers=headers, tablefmt='pretty')
            # Create a Text widget in the new window
            text_widget = Text(top, wrap=WORD, width=200, height=100)
            text_widget.pack(pady=20)
            # Insert the formatted table string into the Text widget

            text_widget.insert("1.0", formatted_table)
            
            # Make the Text widget read-only
            text_widget.config(state="disabled")
            back_button = create_rounded_button(top, 1130, 50, 150, 30, "Back to Menu", top.destroy)

    def display_city_flight():
        try:
            choice = {"option": 3, "value_":city_entry.get()}
            choice3 = json.dumps(choice)
            cs.sendall(choice3.encode())
            data = cs.recv(19999)
            data = data.decode()
            data = json.loads(data)
            headers = ['IATA', 'Departure', 'Arrival', 'Terminal', 'Departure Gate', 'Arrival Gate', 'Status']
            return data, headers
        
        except Exception as e:
            print(f"Error in displaying flight: {e}")
            return display_city_flight

    def city_flight():
            choice = {"option": 3, "value_search": city_entry.get()}
            choice= json.dumps(choice)
            cs.sendall(choice.encode())
            top = Toplevel(root)
            top.title(f"{city_entry.get()} Flights")

            data, headers= display_city_flight()
            formatted_table = tabulate(data, headers=headers, tablefmt='pretty')
            # Create a Text widget in the new window
            text_widget = Text(top, wrap=WORD, width=200, height=100)
            text_widget.pack(pady=20)
            # Insert the formatted table string into the Text widget

            text_widget.insert("1.0", formatted_table)
            
            # Make the Text widget read-only
            text_widget.config(state="disabled")

            back_button = create_rounded_button(top, 1130, 50, 150, 30, "Back to Menu", top.destroy)


    def display_specific_flight():
         try:
            choice = {"option": 4, "value_":flight_entry.get()}
            choice4 = json.dumps(choice)
            cs.sendall(choice4.encode())
            data = cs.recv(19999)
            data = data.decode()
            data = json.loads(data)
            headers = ['IATA', 'Departure', 'Arrival', 'Terminal', 'Departure Gate', 'Arrival Gate', 'Status']
            return data, headers
        
         except Exception as e:
            print(f"Error in displaying flight: {e}")
            return display_specific_flight()

    def specific_flight():
        choice = {"option": 4, "value_search": flight_entry.get()}
        choice4 = json.dumps(choice)
        cs.sendall(choice4.encode())
        top = Toplevel(root)
        top.title(f"{flight_entry.get()} Flights")

        data, headers = display_specific_flight()
        formatted_table = tabulate(data, headers=headers, tablefmt='pretty')
        text_widget = Text(top, wrap=WORD, width=200, height=100)
        text_widget.pack(pady=20)
        text_widget.insert("1.0", formatted_table)
        text_widget.config(state="disabled")

        back_button = create_rounded_button(top, 1122, 20, 150, 30, "Back to Menu", top.destroy)

        

    root = Tk()
    root.title("Flight Information System")


    # Set up a canvas
    canvas_width = 1000
    canvas_height = 800
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#FFFFFF")
    canvas.pack()

    # Load logo image (replace with the path to your logo)
    logo_image = PhotoImage(file="logo.png")
    logo_x = (canvas_width - logo_image.width()) / 2
    logo_y = 20
    canvas.create_image(logo_x, logo_y, anchor="nw", image=logo_image)

    # Tagline text
    tagline_text = "Your gateway to global flight information."
    tagline_x = canvas_width / 2
    tagline_y = logo_y + 400
    canvas.create_text(tagline_x, tagline_y, text=tagline_text, font=("Poppins", 18, "italic", "bold"), fill="#38B6FF")

    # Name Entry Frame
    name_entry_frame = Frame(root)
    name_entry_frame.place(x=canvas_width / 2 - 120, y=logo_y + logo_image.height() + 20, width=300, height=50)

    # Welcome Label
    welcome_label = Label(root, text="Enter your name to get started:", font=("Poppins", 15, "italic", "bold"), fg="#000000")
    welcome_label.place(x=canvas_width / 2 - 140, y=470)

    def show_options():
        global name
        name= name_entry.get()
        cs.send(name.encode('ascii'))
        welcome_user = Label(root, text=f"Welcome {name_entry.get()}", font=("Poppins", 15, "italic", "bold"), fg="#000000")
        welcome_user.place(x=20, y=20)  
        name_entry_frame.pack_forget()
        name_entry_label.destroy()
        name_entry.destroy()
        name_entry_button.destroy()
        name_entry_frame.destroy()
        welcome_label.destroy()
        buttons()

    button_width = 200
    button_height = 50
    button_spacing = 20
    center_x = canvas_width / 2

    def buttons():
        
        # Top right corner for "Quit" button
        quit_button_x = canvas_width - button_width - 20
        quit_button_y = 50
        quit_button = create_rounded_button(canvas, quit_button_x, quit_button_y, button_width, button_height, "Quit",
                                            lambda: root.destroy(), stroke=False)
        # First row of buttons
        button_y_row1 = tagline_y + 60  # Adjusted position
        global button1 
        button1= create_rounded_button(canvas, center_x -200 , button_y_row1, button_width, button_height,
                                        "View All Arrived Flights", lambda: on_button_click(menu,button1))
        global button2
        button2 = create_rounded_button(canvas, center_x + 20, button_y_row1, button_width, button_height,
                                        "View All Delayed Flights", lambda: on_button_click(menu,button2))

        # Second row of buttons
        button_y_row2 = button_y_row1 + button_height + button_spacing
        global button3
        button3 = create_rounded_button(canvas, center_x - 200, button_y_row2, button_width, button_height,
                                        "View Flights from a City", lambda: on_button_click(menu,button3))
        global button4
        button4 = create_rounded_button(canvas, center_x + 20, button_y_row2, button_width, button_height,
                                        "View Specific Flight", lambda: on_button_click(menu,button4))
        
        global menu
        menu= [button1,button2,button3,button4]
        

    def show_continue(state):
        if state==1:
         continue_button = create_rounded_button(canvas, center_x - 100, tagline_y + 190, button_width, button_height, "Continue",
                                            lambda: print("Continue button clicked"), stroke=False)
    # Name Entry
    name_entry_label = Label(name_entry_frame, text="Name:")
    name_entry_label.pack(side=LEFT, padx=10)
    name_entry = Entry(name_entry_frame)
    name_entry.pack(side=LEFT, padx=10)
    name_entry_button = Button(name_entry_frame, text="Submit", command=show_options)
    name_entry_button.pack(side=LEFT, padx=10)
    root.mainloop()
