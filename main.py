import tkinter as tk

from VentanaControl import VentanaControl
from VentanaTableta import VentanaTableta


root = tk.Tk()
root.withdraw()

VentanaControl(root)
VentanaTableta(root)

root.mainloop()