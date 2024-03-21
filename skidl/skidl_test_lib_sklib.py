from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

skidl_test_lib = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'value_str':'1k', 'datasheet':'~', '_aliases':Alias({'R'}), 'description':'Resistor', 'keywords':'R res resistor', '_name':'R', '_match_pin_regex':False, 'tool_version':'kicad_v6', 'ref_prefix':'R', 'num_units':2, 'fplist':[], 'do_erc':True, 'aliases':Alias({'R'}), 'pin':None, 'footprint':'Resistor_SMD:R_0805_2012Metric', 'pins':[
            Pin(num='1',name='~',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='2',name='~',func=Pin.types.PASSIVE,do_erc=True)] }),
        Part(**{ 'name':'BC817', 'dest':TEMPLATE, 'tool':SKIDL, 'value_str':'BC817', 'datasheet':'https://www.onsemi.com/pub/Collateral/BC818-D.pdf', '_aliases':Alias({'BC847', 'BC817'}), 'description':'0.8A Ic, 45V Vce, NPN Transistor, SOT-23', 'keywords':'NPN Transistor', '_name':'BC817', '_match_pin_regex':False, 'tool_version':'kicad_v6', 'ref_prefix':'Q', 'num_units':2, 'fplist':[], 'do_erc':True, 'aliases':Alias({'BC847', 'BC817'}), 'pin':None, 'footprint':'Package_TO_SOT_SMD:SOT-23', 'pins':[
            Pin(num='1',name='B',func=Pin.types.INPUT,do_erc=True),
            Pin(num='2',name='E',func=Pin.types.PASSIVE,do_erc=True),
            Pin(num='3',name='C',func=Pin.types.PASSIVE,do_erc=True)] })])