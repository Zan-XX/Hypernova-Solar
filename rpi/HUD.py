import threading
from time import time
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

    # Current time
    curtime = int(time())

    # If a sensor has not been heard in 3 seconds from, report an error
    if curtime - sensors[0x102]['timestamp'] > 3:
        temp_label_var.set("TEMPERATURE ERROR!")
    else:
        temp = int.from_bytes(sensors[0x102]['data'], 'big')
        temp_label_var.set(f"Voltage 100V\nTemperature: {temp} C")

    if curtime - sensors[0x104]['timestamp'] > 3:
        batt_var.set(-1)
    else:
        level = int.from_bytes(sensors[0x104]['data'], 'big')
        batt_var.set(level)

    if curtime - sensors[0x106]['timestamp'] > 3:
        mph_label_var.set("SPEED ERROR!")
        mph_var.set(0)
    else:
        speed = int.from_bytes(sensors[0x106]['data'], 'big')
        mph_var.set(speed)
        mph_label_var.set(f"{speed} MPH")
    

# TODO Add proper sensor IDs

def can_handler():

    bus = can.Bus('can0', bustype='virtual', bitrate='500000')

    # Dictionary for last data recieved and missed packet tally
    sensors = {
        # Temperature Sensor
        0x102: {
            'data': b'\x00',
            'timestamp': 0
        },

        # Battery Sensor
        0x104: {
            'data': b'\x00',
            'timestamp': 0
        },

        # Speed Sensor
        0x106: {
            'data': b'\x00',
            'timestamp': 0
        }
    }

    while True:
        # Recieve a packet
        msg = bus.recv()

        id = msg.arbitration_id
        data = msg.data

        # If the sensor is in the list
        if id in sensors:
            # Set last packet timestamp
            sensors[id]['timestamp'] = int(time())
        else:
            # Don't do anything else if it isn't in the list
            continue

        # Update the sensor data field in the dictionary
        sensors[id]['data'] = data

        # Pass updates to tkinter
        update_display(sensors)


# Start the can bus thread as a daemon so it is killed when the window is closed
backend = threading.Thread(target=can_handler, daemon=True, name='Backend Thread')


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
        powerlabel = Label(frame, font=Font(size=20), height=2, textvariable=temp_label_var)

        power.grid(column=0, row=0, padx=10, pady=10)
        powerlabel.grid(column=0, row=1)

        speed = Gauge(frame, 9, 100, width=400, variable=self.speed)
        speedlabel = Label(frame, font=Font(size=40), textvariable=mph_label_var)

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

# Force minimum window size once widgets are laid out
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

# Start backend thread after tkinter window starts
root.after_idle(backend.start)

#region ----------------TESTING FUNCTIONS-----------------
import testing

# TESTING: Start thread that provides test data over virtual can bus
testdata = testing.TestingThread(can.Bus('can0', bustype='virtual', bitrate=500000))
testdata.start()

# TESTING: Simulate errors on various arbitration IDs
root.after(5000, testdata.simulate_error, 0x102)
root.after(10000, testdata.simulate_error, 0x104)
root.after(15000, testdata.simulate_error, 0x106)

# TESTING: Recursively makes all backgrounds of frames green and widgets red for tkinter debugging
# testing.debug_color(root)

#endregion -----------------------------------------------

root.mainloop()