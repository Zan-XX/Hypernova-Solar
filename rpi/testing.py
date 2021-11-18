from time import sleep
from cmd import Cmd
from textwrap import dedent
from random import randrange
import threading
import can
from tkinter import Frame, Tk

# Various functions and classes used for debugging

class _DebugConsole(threading.Thread, Cmd):
    intro = " Debug Console ".center(50, '=') + "\n"
    intro += " Type help or ? to list commands. ".center(50, '=')
    prompt = "> "

    def __init__(self, tester):
        self.tester = tester
        threading.Thread.__init__(self, daemon=True, name="Debug Console")
        Cmd.__init__(self)

    def run(self):
        self.cmdloop()
    
    def emptyline(self):
        pass

    def parse(self, args, types):
        args = args.split(' ')

        if not args[0]:
            return args

        if len(args) != len(types):
            print(f"This command takes {len(types)} arguments\n")
            return

        for i, j in enumerate(args):
            try:
                if types[i] == 'str':
                    continue

                elif types[i] == 'ID':
                    args[i] = int(j, 16)
                    continue

                args[i] = int(j)
            except:
                if types[i] == 'int':
                    print(f"Argument {i+1} must be a whole number\n")
                    return
                elif types[i] == 'ID':
                    print(f"Argument {i+1} must be a hexadecimal ID\n")
                    return

        return args

    def do_rate(self, args):
        '\nGet or set packet send rate: rate | rate <packet/sec>\n'

        args = self.parse(args, ('int',))
        
        if not args:
            return

        if not args[0]:
            print(f"Current rate is {self.tester.rate} packet/sec\n")
            return

        self.tester.rate = args[0]
        print(f"New rate set to {args[0]} packet/sec\n")

    def do_error(self, args):
        '\nSimulate an error on a device ID: error <ID> <Seconds>\n'

        args = self.parse(args, ('ID', 'int'))

        if not args:
            return

        if not args[0]:
            print("This command takes 2 arguments\n")

        self.tester.simulate_error(args[0], args[1])


class TestingThread(threading.Thread):
    def __init__(self, bus: can.Bus, rate=2):
        '''
        Creates a new testing thread that sends sample data over the provided bus
        
        :param bus: bus instance to send data over
        :param rate: packets to be sent per second
        '''
        self.bus = bus
        self.rate = rate
        self.error = {
            0x102: 0,
            0x104: 0,
            0x106: 0 
        }

        super().__init__(daemon=True, name="Testing Thread")

    def run(self):
        
        # Start interactive debug console
        _DebugConsole(self).start()

        while True:
            # Send temperature data
            if self.error[0x102]:
                self.error[0x102] -= 1
                if not self.error[0x102]:
                    print("Finished simulating error on 0x102")
            else:
                temp = randrange(0,100).to_bytes(8, 'big')
                msg = can.Message(arbitration_id=0x102, data=temp)
                self.bus.send(msg)
            
            # Send battery data
            if self.error[0x104]:
                self.error[0x104] -= 1
                if not self.error[0x104]:
                    print("Finished simulating error on 0x104")
            else:
                batt = randrange(0,100).to_bytes(8, 'big')
                msg = can.Message(arbitration_id=0x104, data=batt)
                self.bus.send(msg)

            # Send speed data
            if self.error[0x106]:
                self.error[0x106] -= 1
                if not self.error[0x106]:
                    print("Finished simulating error on 0x106")
            else:
                speed = randrange(0,100).to_bytes(8, 'big')
                msg = can.Message(arbitration_id=0x106, data=speed)
                self.bus.send(msg)
            
            sleep(1 / self.rate)

    def simulate_error(self, id, seconds):
        '''
        Simulates a communication error on the specified id for a certain amount of time
        
        :param id: arbitration id to simulate error on
        :param seconds: number of seconds to simulate error for
        '''
        if self.error[id]:
            print(f"Already simulating error on {hex(id)}!")
            return

        self.error[id] = seconds * self.rate
        print(f"Simulating error on {hex(id)} for {seconds} seconds")
            

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