"""
This script detects connected displays using `xrandr` 
and creates Tkinter windows on each display.

The main window is placed on the primary display, 
and additional windows are created for each secondary display. 
The windows are positioned near the center of their respective 
displays and display the name of the display.
"""

import re
import sys
from subprocess import run
from dataclasses import dataclass
from tkinter import Tk, Toplevel, Label

XrandrDisplay = tuple[str, str, str, str]


@dataclass
class WindowGeometry:
    """The geometry of a window.

    Attributes:
        width: The width of the window in pixels.
        height: The height of the window in pixels.
        x: The x-coordinate of the top-left corner.
        y: The y-coordinate of the top-left corner.
    """
    width: int
    height: int
    x: int
    y: int

    def __str__(self) -> str:
        """
        Returns a string representation 
        suitable for Tkinter's geometry method.
        """
        return f"{self.width}x{self.height}+{self.x}+{self.y}"


def create_window(geometry: WindowGeometry,
                  title: str = "", message: str = "") -> None:
    """Creates a Toplevel window.

    Args:
        geometry (WindowGeometry): 
            Defining the window's size and position.
        title (str, optional): 
            The title of the window. Defaults to "".
        message (str, optional): 
            The message to be displayed in the window. Defaults to "".
    """
    window = Toplevel()
    window.title(title)
    window.geometry(str(geometry))
    font_size = int(geometry.width/geometry.height * 20)
    label = Label(window, text=message, font=("Arial", font_size))
    label.place(relx=0.5, rely=0.5, anchor="center")


def main():
    """
    Main function to get display information and create windows.
    """
    root = Tk()
    xrandr_cmd = run(["xrandr"], check=True, capture_output=True, text=True)
    regex = r"(.+)\s(?:connected)(.*)\s(\d+x\d+)\+(\d+\+\d+)\s"
    xrandr_output: list[XrandrDisplay] = re.findall(regex, xrandr_cmd.stdout)

    if not xrandr_output:
        sys.exit("No connected displays found")

    for i in xrandr_output:
        display_name = i[0]
        is_primary = bool(i[1])
        w, h = map(int, i[2].split("x"))
        x, y = map(int, i[3].split("+"))
        geometry = WindowGeometry(w//2, h//2, x+w//4, y+h//4)

        if is_primary:
            root.title(f"{display_name} [Main Window]")
            root.geometry(str(geometry))
            Label(root, font=("Arial", int(geometry.width/geometry.height * 20)),
                  text=display_name).place(relx=0.5, rely=0.5, anchor="center")
        else:
            create_window(geometry, display_name, display_name)
    root.mainloop()


if __name__ == "__main__":
    main()
