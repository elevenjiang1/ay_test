#!/usr/bin/python
#Disable motors.

from dxl_cranex7 import *

#Setup the device
crane= TCraneX7()
crane.Setup()
crane.DisableTorque()
crane.Quit()
