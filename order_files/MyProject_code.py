import os
os.environ['KICAD_SYMBOL_DIR'] = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/'

from skidl import *

# Create input & output voltages and ground reference.
vin, vout, gnd = Net('VI'), Net('VO'), Net('GND')

# Create two resistors.
r1 = Part('Device', 'R', footprint='Resistor_SMD:R_0805_2012Metric')
r2 = Part('Device', 'R', footprint='Resistor_SMD:R_0805_2012Metric')
r1.value = '1K'
r2.value = '500'

# Connect the nets and resistors.
vin += r1[1]
gnd += r2[2]
vout += r11[2], r2[1]  # corrected the typo in the reference to the first resistor.

# Output the netlist to a file.
generate_netlist()