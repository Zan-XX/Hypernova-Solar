#!/usr/bin/env python3


from tkinter import Tk, Frame, Button, Canvas, Scale
from tkinter.constants import LAST
from math import sin, cos, pi


class Gauge(Canvas):
    """
    Gauge display

    :param master: Tk parent object (e.g. root)
    :param ticks: Number of ticks on gauge
    :type ticks: int
    """

    def __init__(self, master, ticks, **kw):

        if "height" in kw:
            del kw["height"]

        if "width" not in kw:
            kw["width"] = 200

        width = kw["width"]
        height = width / 2

        # Create Canvas for Gauge
        super().__init__(master, height=height, highlightthickness=0, **kw)

        # Create Gauge Outline Arc
        self.outline = self.create_arc(
            0,
            0,
            width,
            height * 2,
            start=0,
            extent=180,
            fill="white",
        )

        # Iterate through tickmarks
        if ticks > 0:
            for i in range(ticks):
                a = (i + 1) / (ticks + 1)
                self.create_line(
                    width / 2 + width / 2 * cos(pi * (a + 1)),
                    height + height * sin(pi * (a + 1)),
                    width / 2 + (width / 2 * cos(pi * (a + 1))) * 0.90,
                    height + (height * sin(pi * (a + 1))) * 0.90,
                )

        # Create Gauge Pointer
        self.arrow = self.create_line(
            width / 2,
            height,
            0,
            height,
            arrow=LAST,
            arrowshape=(16, 20, 6),
            width=15,
        )


# Example code (will not run if imported)
if __name__ == "__main__":
    root = Tk()

    for x in range(100, 500, 100):
        d = Gauge(root, 10, width=x)
        d.pack(pady=10)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    root.mainloop()