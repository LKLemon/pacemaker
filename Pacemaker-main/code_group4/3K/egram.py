import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from pyqtgraph.Point import Point
import re, time, os, sys



def egram():
    #connect()
    win = pg.GraphicsLayoutWidget(show =True)
    win.setWindowTitle('HeartView')
    p2 = win.addPlot()
    data1 = np.random.normal(size=300)
    curve2 = p2.plot(data1)
    ptr1 = 0

    def updata1():
        global data1,ptr1
        data1[:-1] = data1[1:]
        data1[-1]=np.random.normal()
        ptr1+=1
        curve2.setData(updata1)
        curve2.setPos(ptr1,0)

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(updata1)
    timer.start(50)

    if name == 'main':
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec()

egram()