#!/usr/bin/env python3


from tkinter import Tk, Frame, Button, Canvas, Scale, IntVar
from tkinter.constants import LAST, HORIZONTAL
from math import sin, cos, pi


class Gauge(Canvas):
    """
    Gauge display

    :param master: Tk parent object (e.g. root)
    :param ticks: Number of ticks on gauge
    :type ticks: int
    """

    def __init__(self, master, ticks, **kw):

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
        self.var.trace_add('write', self.updateArrow)

    # Update pointer position
    def updateArrow(self, name1, name2, op):
        a = self.var.get() / 100
        self.coords(
            self.arrow,
            self.width / 2,
            self.height,
            self.width / 2 + self.width / 2 * cos(pi * (a + 1)),
            self.height + self.height * sin(pi * (a + 1)),
        )


# Example code (will not run if imported)
if __name__ == "__main__":
    root = Tk()

    value = IntVar()

    for x in range(100, 500, 100):
        d = Gauge(root, 10, width=x, variable=value)
        d.pack(pady=10)
    scale = Scale(root, variable=value, orient=HORIZONTAL)
    scale.pack()

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()