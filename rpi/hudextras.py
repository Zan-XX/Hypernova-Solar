#!/usr/bin/env python3


from tkinter import Tk, Frame, Canvas, IntVar
from tkinter.constants import HIDDEN, LAST, NORMAL, SW, SE
from math import sin, cos, pi


class Gauge(Canvas):
    """
    Gauge display using Tk.Canvas
    """

    def __init__(self, master, ticks, max, **kw):
        """
        Create new Gauge instance

        :param master: Tk parent object (e.g. root)
        :param ticks: Number of ticks on gauge
        :type ticks: int
        :param max: Max value on gauge
        :type max: int
        """

        # Discard passed height, height will always be half the width
        if "height" in kw:
            del kw["height"]

        # If no width is passed, default to 200
        if "width" not in kw:
            kw["width"] = 200

        # If no IntVar is passed, create an empty one
        if "variable" in kw:
            self.var = kw["variable"]
            del kw["variable"]
        else:
            self.var = IntVar()

        self.width = kw["width"]
        self.height = self.width / 2
        self.max = max

        # Create Canvas for Gauge
        super().__init__(master, height=self.height, highlightthickness=0, **kw)

        # Create Gauge Outline Arc
        self.outline = self.create_arc(
            0,
            0,
            self.width,
            self.height * 2,
            start=0,
            extent=180,
            fill="white",
        )

        # Iterate through tickmarks
        if ticks > 0:
            for i in range(ticks):
                a = (i + 1) / (ticks + 1)
                self.create_line(
                    self.width / 2 + self.width / 2 * cos(pi * (a + 1)),
                    self.height + self.height * sin(pi * (a + 1)),
                    self.width / 2 + (self.width / 2 * cos(pi * (a + 1))) * 0.90,
                    self.height + (self.height * sin(pi * (a + 1))) * 0.90,
                )
                self.create_text(
                    self.width / 2 + (self.width / 2 * cos(pi * (a + 1))) * 0.80,
                    self.height + (self.height * sin(pi * (a + 1))) * 0.80,
                    text=str(int(a * max)),
                    font=("", int(20 * (self.width / 400))),
                )

        # Create Gauge Pointer
        self.arrow = self.create_line(
            self.width / 2,
            self.height,
            0,
            self.height,
            arrow=LAST,
            arrowshape=(16, 20, 6),
            width=15,
        )

        # Update Pointer on IntVar()
        self.var.trace_add("write", self.updateArrow)

    # Update pointer position
    def updateArrow(self, name1, name2, op):
        a = self.var.get() / self.max
        self.coords(
            self.arrow,
            self.width / 2,
            self.height,
            self.width / 2 + self.width / 2 * cos(pi * (a + 1)),
            self.height + self.height * sin(pi * (a + 1)),
        )


class Battery(Canvas):
    """
    Create new Battery instance

    :param master: Tk parent object (e.g. root)
    :param warning: level at which bar will turn yellow
    :type warning: int
    :param low: level at which bar will turn red
    :type low: int
    """

    def __init__(self, master, warning, low, **kw):
        """
        docstring
        """
        if not (0 < warning < 100):
            raise ValueError("warning must be between 0 and 100")

        if not (0 < low < 100):
            raise ValueError("low must be between 0 and 100")

        if warning <= low:
            raise ValueError("warning value must be greater than low")

        self.warning = warning
        self.low = low

        # Discard passed height, height will always be half the width
        if "height" in kw:
            del kw["height"]

        # If no width is passed, default to 200
        if "width" not in kw:
            kw["width"] = 200

        # If no IntVar is passed, create an empty one
        if "variable" in kw:
            self.var = kw["variable"]
            del kw["variable"]
        else:
            self.var = IntVar()

        self.width = kw["width"]
        self.height = self.width / 2

        super().__init__(master, height=self.height, highlightthickness=0, **kw)

        # Battery filling
        self.fill = self.create_rectangle(
            0,
            self.height / 3,
            self.width,
            self.height - 4,
            fill="green",
            outline="",
        )

        # Battery Outline
        self.outline = self.create_rectangle(
            2,
            self.height / 3,
            self.width - 2,
            self.height - 4, 
            width=4
        )

        # Minimum text
        self.create_text(
            2,
            self.height / 3,
            anchor=SW,
            text=0,
            font=("", int(40 * (self.width / 400))),
        )

        # Maximum text
        self.create_text(
            self.width,
            self.height / 3,
            anchor=SE,
            text=100,
            font=("", int(40 * (self.width / 400))),
        )

        # Error text
        self.error = self.create_text(
            self.width / 2,
            self.height * 2/3,
            font=("", int(40 * (self.width / 400))),
            text="ERROR",
            state=HIDDEN
        )

        self.var.trace_add("write", self.__update_level)

    def __update_level(self, name1, name2, op):
        """
        Updates the battery to display the new variable value
        """
        a = self.var.get()

        # Display error text if there is an error and return immediately
        if a == -1:
            self.coords(self.fill, 0, self.height / 3, self.width, self.height - 4)
            self.itemconfigure(self.fill, fill = "red")
            self.itemconfigure(self.error, state=NORMAL)
            return

        # Hide error text if visible
        if self.itemcget(self.error, "state") == NORMAL:
            self.itemconfigure(self.error, state=HIDDEN)

        # Change Color based on level
        if a <= self.low:
            self.itemconfigure(self.fill, fill="red")
        elif a <= self.warning:
            self.itemconfigure(self.fill, fill="goldenrod")
        else:
            self.itemconfigure(self.fill, fill="green")

        a /= 100
        self.coords(self.fill, 0, self.height / 3, self.width * a, self.height - 4)


# Example code (will not run if imported)
if __name__ == "__main__":
    from tkinter import Frame, Scale
    from tkinter.constants import HORIZONTAL, LEFT, X, RIDGE

    root = Tk()

    # Create left frame with a RIDGE border
    frame1 = Frame(root, bd=4, relief=RIDGE)
    frame1.pack(side=LEFT)

    # Iterate through widths and create 4 different gauges with the same variable
    value = IntVar()
    for x in range(100, 500, 100):
        d = Gauge(frame1, 9, 100, width=x, variable=value)
        d.pack(pady=10)
    scale = Scale(frame1, variable=value, orient=HORIZONTAL)
    scale.pack(fill=X)

    # Create right frame with RIDGE border
    frame2 = Frame(root, bd=4, relief=RIDGE)
    frame2.pack(side=LEFT)

    # Create gauge and slider in right frame with max value of 200
    value2 = IntVar()
    gauge2 = Gauge(frame2, 9, 200, width=400, variable=value2)
    gauge2.pack()
    scale2 = Scale(frame2, variable=value2, orient=HORIZONTAL, to=200)
    scale2.pack(fill=X)

    # Create gauge and slider in right frame with max value of 50
    value3 = IntVar()
    
    gauge3 = Gauge(frame2, 9, 50, width=400, variable=value3)
    gauge3.pack()
    
    scale3 = Scale(frame2, variable=value3, orient=HORIZONTAL, to=50)
    scale3.pack(fill=X)

    # Create Battery in root frame with slider
    value4 = IntVar()
    
    battery = Battery(root, 50, 25, width=400, variable=value4)
    battery.pack()
    
    scale4 = Scale(root, variable=value4, orient=HORIZONTAL, from_=-1)
    scale4.pack(fill=X)


    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()