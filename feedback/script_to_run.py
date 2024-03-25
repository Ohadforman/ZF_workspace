import os
os.environ['KICAD_SYMBOL_DIR'] = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/'

from skidl import *

# Create a new circuit
reset()

# Define the components
led = Part('Device', 'LED')
resistor = Part('Device', 'R', value='330 R')
voltage_source = Part('Device', 'v', dc_value=3.3)

# Connect the components
V = Net('3.3V')
GND = Net('GND')

voltage_source['p'] += V, GND
led['a'] += V
led['k'] += GND

# Add the blinking functionality
led['a'] += Net('BLINK')
led['k'] += GND

# Generate the netlist and draw the circuit
generate_netlist()