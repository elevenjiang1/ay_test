#!/usr/bin/python
#\file    button02.py
#\brief   certain python script
#\author  Akihiko Yamaguchi, info@akihikoy.net
#\version 0.1
#\date    Dec.14, 2016

import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *

# Create a window
app = QApplication(sys.argv)
w = QWidget()
w.resize(320, 240)
w.setWindowTitle("Hello World!")

# Add a button
btn = QPushButton('Hello World!', w)
btn.setToolTip('Click me!')
btn.resize(btn.sizeHint())
btn.move(100, 80)

# Create the actions
@pyqtSlot()
def on_click():
    print('clicked')

@pyqtSlot()
def on_press():
    print('pressed')

@pyqtSlot()
def on_release():
    print('released')

# connect the signals to the slots
btn.clicked.connect(on_click)
btn.pressed.connect(on_press)
btn.released.connect(on_release)

# Show window
w.show()
app.exec_()
