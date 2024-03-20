from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

MyProject_code_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'datasheet':'~', 'keywords':'R res resistor', '_match_pin_regex':False, '_name':'R', 'description':'Resistor', 'value_str':'1K', 'tool_version':'kicad_v6', '_aliases':Alias({'R'}), 'ref_prefix':'R', 'num_units':2, 'fplist':[], 'do_erc':True, 'aliases':Alias({'R'}), 'pin':None, 'footprint':'Resistor_SMD:R_0805_2012Metric', 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])