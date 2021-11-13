import threading
from tkinter import *
from tkinter.font import Font
import can
from hudextras import Gauge, Battery

root = Tk()

mph_var = IntVar()
mph_label_var = StringVar()

batt_var = IntVar()
temp_label_var = StringVar()


# TODO Rewrite this whole function its not that great
# * Avoid updating unchanged fields?
# * Possibly offload IntVar setting to function in tkinter event loop to avoid spam?

def update_display(sensors):

    # If a sensor has not been heard from, report an error
    if sensors[0x102].missed > 10:
        temp_label_var.set("TEMPERATURE ERROR!")

    if sensors[0x104].missed > 10:
        # TODO Add battery error action
        pass

    if sensors[0x106].missed > 10:
        mph_label_var.set("SPEED ERROR!")
        mph_var.set(0)

    # Update tkinter variables with new data
    temp = int.from_bytes(sensors[0x102].data, 'big')
    temp_label_var.set(f"Temp: {temp} F")

    level = int.from_bytes(sensors[0x104].data, 'big')
    batt_var.set(level)

    speed = int.from_bytes(sensors[0x106], 'big')
    mph_var.set(speed)
    mph_label_var.set(f"{speed} MPH")


# TODO Add proper sensor IDs

def can_handler():

    bus = can.Bus('can0', bustype='virtual', bitrate='500000')

    # Dictionary for last data recieved and missed packet tally
    sensors = {
        # Temperature Sensor
        0x102: {
            'data': 0,
            'missed': 0
        },

        # Battery Sensor
        0x104: {
            'data': 0,
            'missed': 0
        },

        # Speed Sensor
        0x106: {
            'data': 0,
            'missed': 0
        }
    }

    while True:
        # Recieve a packet
        msg = bus.recv()

        id = msg.arbitration_id
        data = msg.data

        # If the sensor is in the list
        if id in sensors:
            # Set that sensor missed count to 0
            sensors[id].missed = 0
        else:
            # Don't do anything else if it isn't in the list
            continue

        # Increase the missed count for all sensors by 1
        for i in sensors:
            sensors[i].missed += 1

        # Update the sensor data field in the dictionary
        sensors[id].data = data

        # Pass updates to tkinter
        update_display(sensors)


# Start the can bus thread as a daemon so it is killed when the window is closed
backend = threading.Thread(target=can_handler, daemon=True, )
backend.start()


# TODO Write button callback handlers
# * Impliment StringVars for various labels

class GUI:
    def __init__(self, master: Tk, speed: IntVar, battery: IntVar) -> None:
        '''
        Create new instance of the Hypernova Solar GUI

        :param master: Tk instance to add GUI to
        :param speed: IntVar used for the speed gauge
        :param battery: IntVar used for the battery level
        '''
        self.master = master
        self.speed = speed
        self.battery = battery

        self.top = Frame(root, relief=SUNKEN, borderwidth=5)
        self.__create_top_widgets(self.top)
        self.top.pack(fill=BOTH)

        self.bottom = Frame(root, relief=SUNKEN, borderwidth=5)
        self.__create_bottom_widgets(self.bottom)
        self.bottom.pack(expand=TRUE, fill=BOTH)

    def __create_top_widgets(self, frame: Frame):
        '''
        Create and arrange the widgets for the top frame

        :param frame: The top frame instance
        '''
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        power = Battery(frame, 50, 25, width=400, variable=self.battery)
        powerlabel = Label(
            frame, text="Voltage 100 V\nTemperature: 30 C", font=Font(size=20))

        power.grid(column=0, row=0, padx=10, pady=10)
        powerlabel.grid(column=0, row=1)

        speed = Gauge(frame, 9, 100, width=400, variable=self.speed)
        speedlabel = Label(frame, text="0 MPH", font=Font(size=40))

        speed.grid(column=1, row=0, padx=10, pady=10)
        speedlabel.grid(column=1, row=1)

    def __create_bottom_widgets(self, frame: Frame):
        '''
        Create and arrange the widgets for the bottom frame

        :param frame: The bottom frame instance
        '''
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        button1 = Button(frame, text="Button 1", font=Font(size=20))
        button2 = Button(frame, text="Button 2", font=Font(size=20))
        button3 = Button(frame, text="Button 3", font=Font(size=20))
        button4 = Button(frame, text="Button 4", font=Font(size=20))

        button1.grid(column=0, row=0, padx=10, pady=10, sticky=NSEW)
        button2.grid(column=1, row=0, padx=10, pady=10, sticky=NSEW)
        button3.grid(column=0, row=1, padx=10, pady=10, sticky=NSEW)
        button4.grid(column=1, row=1, padx=10, pady=10, sticky=NSEW)

# Start app fullscreen
# root.attributes('-fullscreen', True)


interface = GUI(root, mph_var, batt_var)

# Recursively makes all backgrounds of frames green and widgets red for tkinter debugging
# def debugcolor(top):
#     for i in top.winfo_children():
#         if type(i) is Frame:
#             i.configure(bg="green")
#             debugcolor(i)
#         else:
#             i.configure(bg="red")

# debugcolor(root)

# Force minimum window size once widgets are laid out
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()