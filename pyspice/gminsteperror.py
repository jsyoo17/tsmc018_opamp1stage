'''
gmin step errror solution for pyspice
2022 Junsang Yoo
'''


## imports
import numpy as np
import matplotlib.pyplot as plt
import os

# pyspice import
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Spice.Library import SpiceLibrary

# os.chdir(os.path.dirname(__file__))     # change directory to where current file is
spice_library = SpiceLibrary('./')      # use TSMC 180nm library file (measured)

## OPAMP design
'''
  --------------------------------
  |                |             |
  |                s             s
  |               M3 g---------g M4
  |                d      |      d
{ibais}            |      |      |
  |                |-----(3)     |-----OUT
 \ /               |             |
  |                d             d
  |              g M1           M2 g
  |                s             s
  |                |             |
  |                ------(2)------
  |------------           |
  |           |           |
  d           |           d
 M6 g--------(1)--------g M5
  s                       s
  |                       |
  -------------------------

This uses TSMC 180nm device
For 180nm devices, the working voltage should be 1.8V
minimum Length: 180nm
minimum width: 220nm
constraints for differential pair: W1=W2, W3=W4
'''

# error occuring size:
VDD=1.8; VSS=0
ibias=20e-6
Lmin=180e-9; Wmin=220e-9
W_samp=np.array([1e-6,1e-6,0.5e-6,0.5e-6,2e-6,4e-6])    # sample W1~W6
L_samp=np.array([Lmin,Lmin,Lmin,Lmin,0.5e-6,0.5e-6])    # sample L1~L6
MOScnt=6  # total number of MOSFET

## Circuit definition
opamp = Circuit('opamp')
opamp.include(spice_library['nch'])   # this includes library file that has nch in it

# OPAMP
opamp.I(1,'DD',3,ibias)     # current source
M1=opamp.M(1,1,'INP',2,2,model='nch',l=L_samp[0],w=W_samp[0])          # differential pair
M2=opamp.M(2,'OUT','INN',2,2,model='nch',l=L_samp[1],w=W_samp[1])      # differential pair
M3=opamp.M(3,1,1,'DD','DD',model='pch',l=L_samp[2],w=W_samp[2])        # active load
M4=opamp.M(4,'OUT',1,'DD','DD',model='pch',l=L_samp[3],w=W_samp[3])    # active load
M5=opamp.M(5,2,3,'SS','SS',model='nch',l=L_samp[4],w=W_samp[4])        # current source
M6=opamp.M(6,3,3,'SS','SS',model='nch',l=L_samp[5],w=W_samp[5])        # current mirror
opamp.C(1,'OUT',0,100e-15)  # loading cap

## simulation
# Voltage Sources
opamp.V(1,'DD',0,VDD)       # VDD
opamp.V(2,'SS',0,0)         # VSS

# Input Voltage
opamp.R(1,'DD','INP',50@u_kOhm)
opamp.R(2,'INN','SS',50@u_kOhm)
opamp.R(3,'INP','INN',0@u_Ohm)     # added to regard nodes INP and INN as same node

simulator= opamp.simulator(temperature = 25, nominal_temperature =25)
op_sim=simulator.operating_point()


