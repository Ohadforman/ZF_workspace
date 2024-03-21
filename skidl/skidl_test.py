import os
# Set the KiCad symbol directory environment variable
os.environ['KICAD_SYMBOL_DIR'] = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/"

from skidl import *

#print(search('opamp "high performance"'))
print(show('Transistor_BJT', 'BC847'))
print(search_footprints('QFN-48'))
print((search('opamp')))
# Define the footprints for each part type
resistor_footprint = 'Resistor_SMD:R_0805_2012Metric'
transistor_footprint = 'Package_TO_SOT_SMD:SOT-23'

# Define components with footprints

resistor = Part('Device', 'R', value='1k', footprint=resistor_footprint)
transistor = Part('Transistor_BJT', 'BC847', footprint=transistor_footprint)


# Run electrical rule check and generate the netlist
#ERC()
generate_netlist()
