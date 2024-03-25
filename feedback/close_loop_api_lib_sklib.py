from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

close_loop_api_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, '_aliases':Alias({'R'}), 'tool_version':'kicad_v6', 'value_str':'1K', 'keywords':'R res resistor', '_name':'R', 'datasheet':'~', 'description':'Resistor', '_match_pin_regex':False, 'ref_prefix':'R', 'num_units':2, 'fplist':[], 'do_erc':True, 'aliases':Alias({'R'}), 'pin':None, 'footprint':'Resistor_SMD:R_0805_2012Metric', 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] })])