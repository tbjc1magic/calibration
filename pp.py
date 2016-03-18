#!/usr/bin/env python

import pylab
from pylab import *
import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

root = Tkinter.Tk()
root.wm_title("Extended Realtime Plotter")

xAchse=pylab.arange(0,100,1)
yAchse=pylab.array([0]*100)

fig = pylab.figure(1)
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_title("Realtime Waveform Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
#ax.axis([0,100,-1.5,1.5])
line1=ax.plot(xAchse,yAchse,'-')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg( canvas, root )
toolbar.update()
canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

canvas.show()
Tkinter.mainloop()
