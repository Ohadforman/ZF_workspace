import os
os.environ['KISYSMOD'] = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/modules/'
os.environ['KICAD_SYMBOL_DIR'] = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/'

from skidl import *

led = Part('Device', 'LED', footprint='LED_3MM')
led[1] += Net('BLINK')
led[2] += Net('GND')

generate_netlist()