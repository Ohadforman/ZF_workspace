from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

MyProject_code_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'LED', 'dest':TEMPLATE, 'tool':SKIDL, 'tool_version':'kicad_v6', 'value_str':'LED', '_name':'LED', 'datasheet':'~', '_aliases':Alias({'LED'}), '_match_pin_regex':False, 'description':'Light emitting diode', 'keywords':'LED diode', 'ref_prefix':'D', 'num_units':2, 'fplist':[], 'do_erc':True, 'aliases':Alias({'LED'}), 'pin':None, 'footprint':'LED_0805', 'pins':[
            Pin(num='1',name='K',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='A',func=Pin.types.PASSIVE,do_erc=True)] }),
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'tool_version':'kicad_v6', 'value_str':'1K', '_name':'R', 'datasheet':'~', '_aliases':Alias({'R'}), '_match_pin_regex':False, 'description':'Resistor', 'keywords':'R res resistor', 'ref_prefix':'R', 'num_units':2, 'fplist':[], 'do_erc':True, 'aliases':Alias({'R'}), 'pin':None, 'footprint':'Resistor_SMD:R_0805', 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])