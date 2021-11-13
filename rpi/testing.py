from time import sleep
from random import randrange
import threading
import can
from tkinter import Frame, Tk

# Various functions and classes used for debugging

class TestingThread(threading.Thread):
    def __init__(self, bus: can.Bus):
        '''
        Creates a new testing thread that sends sample data over the provided bus
        
        :param bus: bus instance to send data over
        '''
        self.bus = bus
        self.error = {
            0x102: 0,
            0x104: 0,
            0x106: 0 
        }

        super().__init__(daemon=True, name="Testing Thread")

    def run(self):
        while True:
            # Send temperature data
            if self.error[0x102]:
                self.error[0x102] -= 1
            else:
                temp = randrange(0,100).to_bytes(8, 'big')
                msg = can.Message(arbitration_id=0x102, data=temp)
                self.bus.send(msg)
            
            # Send battery data
            if self.error[0x104]:
                self.error[0x104] -= 1
            else:
                batt = randrange(0,100).to_bytes(8, 'big')
                msg = can.Message(arbitration_id=0x104, data=batt)
                self.bus.send(msg)

            # Send speed data
            if self.error[0x106]:
                self.error[0x106] -= 1
            else:
                speed = randrange(0,100).to_bytes(8, 'big')
                msg = can.Message(arbitration_id=0x106, data=speed)
                self.bus.send(msg)
            


            sleep(0.5)

    def simulate_error(self, id):
        '''
        Simulates a communication error on the specified id for 20 packets
        
        :param id: arbitration id to simulate error on
        '''
        self.error[id] = 20

def debug_color(top: Tk):
    '''
    Recursively makes backgrounds of all frames green and widgets red for tkinter debugging

    :param top: top level widget to begin coloring
    '''
    for i in top.winfo_children():
        if type(i) is Frame:
            i.configure(bg="green")
            debug_color(i)
        else:
            i.configure(bg="red")