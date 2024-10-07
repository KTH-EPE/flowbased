import pandapower as pp
from pandas import read_json
import io


# 380kV line data
EHV_data = {'c_nf_per_km': 11.5, 'r_ohm_per_km': 0.0328,
                 'x_ohm_per_km': 0.312, 'max_i_ka': 1.32,
                 'type': 'ol'}

# 220kV line data
HV_data = {'c_nf_per_km': 9.08, 'r_ohm_per_km': 0.0653,
                 'x_ohm_per_km': 0.398, 'max_i_ka': 1.14,
                 'type': 'ol'}


net = pp.create_empty_network()

pp.create_std_type(net, EHV_data, 'Line400kV', element='line')
pp.create_std_type(net, HV_data, 'Line220kV', element='line')

pp.create_bus(net,vn_kv=400, name = 'Torneå', zone = 'SE1')
pp.create_bus(net,vn_kv=400, name = 'Porjus', zone = 'SE1')
pp.create_bus(net,vn_kv=400, name = 'Luleå', zone = 'SE1')
pp.create_bus(net,vn_kv=400, name = 'Östersund', zone = 'SE2')
pp.create_bus(net,vn_kv=400, name = 'Ånge', zone = 'SE2')
pp.create_bus(net,vn_kv=400, name = 'Sundsvall', zone = 'SE2')
pp.create_bus(net,vn_kv=400, name = 'Karlstad', zone = 'SE3')
pp.create_bus(net,vn_kv=400, name = 'Stockholm', zone = 'SE3')
pp.create_bus(net,vn_kv=400, name = 'Göteborg', zone = 'SE3')
pp.create_bus(net,vn_kv=400, name = 'Oskarshamn', zone = 'SE3')
pp.create_bus(net,vn_kv=400, name = 'Malmö', zone = 'SE4')
pp.create_bus(net,vn_kv=400, name = 'Kalmar', zone = 'SE4')
pp.create_bus(net,vn_kv=400, name = 'Ystad', zone = 'SE4')
pp.create_bus(net,vn_kv=400, name = 'Norge', zone = 'NO')
pp.create_bus(net,vn_kv=400, name = 'Finland', zone = 'FI')

# One line along the production centers in SE1
pp.create_line(net, from_bus=0, to_bus=1, length_km = 200, std_type = 'Line220kV', name = "L0")
pp.create_line(net, from_bus=1, to_bus=2, length_km = 200, std_type = 'Line220kV', name = "L1")
#Two lines connecting SE1 and SE2
pp.create_line(net, from_bus=1, to_bus=4, length_km = 300, std_type = 'Line400kV', name = "L2")
pp.create_line(net, from_bus=2, to_bus=5, length_km = 300, std_type = 'Line400kV', name = "L3")
# One line along the production centers in SE2
pp.create_line(net, from_bus=3, to_bus=4, length_km = 200, std_type = 'Line220kV', name = "L4")
pp.create_line(net, from_bus=4, to_bus=5, length_km = 200, std_type = 'Line220kV', name = "L5")
#Two lines connecting SE2 and SE3
pp.create_line(net, from_bus=4, to_bus=6, length_km = 400, std_type = 'Line400kV', name = "L6")
pp.create_line(net, from_bus=5, to_bus=7, length_km = 400, std_type = 'Line400kV', name = "L7")
# 5 lines in a meshed config  in SE3, varying voltage levels
pp.create_line(net, from_bus=6, to_bus=7, length_km = 150, std_type = 'Line400kV', name = "L8")
pp.create_line(net, from_bus=7, to_bus=9, length_km = 150, std_type = 'Line220kV', name = "L9")
pp.create_line(net, from_bus=7, to_bus=8, length_km = 150, std_type = 'Line220kV', name = "L10")
pp.create_line(net, from_bus=6, to_bus=8, length_km = 150, std_type = 'Line220kV', name = "L11")
pp.create_line(net, from_bus=8, to_bus=9, length_km = 300, std_type = 'Line400kV', name = "L12")
# 2 lines connecting SE3 and SE4
pp.create_line(net, from_bus=8, to_bus=10, length_km = 200, std_type = 'Line400kV', name = "L13")
pp.create_line(net, from_bus=9, to_bus=11, length_km = 200, std_type = 'Line400kV', name = "L14")
# 3 lines in a meshed config  in SE4, varying voltage levels
pp.create_line(net, from_bus=10, to_bus=11, length_km = 150, std_type = 'Line220kV', name = "L15")
pp.create_line(net, from_bus=10, to_bus=12, length_km = 150, std_type = 'Line400kV', name = "L16")
pp.create_line(net, from_bus=11, to_bus=12, length_km = 150, std_type = 'Line220kV', name = "L17")
# Two lines connecting Finland to SE1 and SE3
pp.create_line(net, from_bus=7, to_bus=14, length_km = 300, std_type = 'Line220kV', name = "L18")
pp.create_line(net, from_bus=2, to_bus=14, length_km = 300, std_type = 'Line220kV', name = "L19")
# Two lines connecting Norway to SE2 and SE3
pp.create_line(net, from_bus=8, to_bus=13, length_km = 100, std_type = 'Line220kV', name = "L20")
pp.create_line(net, from_bus=3, to_bus=13, length_km = 200, std_type = 'Line220kV', name = "L21")



# External grid connection at bus 7 in SE3 representing Forsmark
pp.create_ext_grid(net, bus = 13, name = "FCR-N")
# Hydropower production in SE1 and SE2
pp.create_gen(net, bus = 0, p_mw = 400, sn_mva = 600, vm_pu=1.0, name = "Hydro1", zone = 'SE1')
pp.create_gen(net, bus = 1, p_mw = 300, sn_mva = 400, vm_pu=1.0, name = "Hydro2", zone = 'SE1')
pp.create_gen(net, bus = 2, p_mw = 300, sn_mva = 200, vm_pu=1.0, name = "Hydro3", zone = 'SE1')
pp.create_gen(net, bus = 3, p_mw = 150, sn_mva = 400, vm_pu=1.0, name = "Hydro4", zone = 'SE2')
pp.create_gen(net, bus = 4, p_mw = 300, sn_mva = 400, vm_pu=1.0, name = "Hydro5", zone = 'SE2')
pp.create_gen(net, bus = 5, p_mw = 150, sn_mva = 200, vm_pu=1.0, name = "Hydro6", zone = 'SE2')

# Nuclear & Hydro production in SE3
pp.create_gen(net, bus = 7, p_mw = 400, sn_mva = 600, vm_pu=1.0, name = "Nuclear2", zone = 'SE3')
pp.create_gen(net, bus = 6, p_mw = 200, sn_mva = 300, vm_pu=1.0, name = "Hydro7", zone = 'SE3')
pp.create_gen(net, bus = 8, p_mw = 400, sn_mva = 600, vm_pu=1.0, name = "Nuclear3" , zone = 'SE3')

# Voltage controlling units in Norway and Finland
# pp.create_gen(net, bus = 13, p_mw = 0, sn_mva = 1, vm_pu=1.0, name = "Control", zone = 'NO')
# pp.create_gen(net, bus = 14, p_mw = 0, sn_mva = 1, vm_pu=1.0, name = "Control", zone = 'FI')

# Wind production in SE1, SE2 and SE3
pp.create_sgen(net, bus = 1, p_mw = 200, sn_mva = 300, name = "Wind1", zone = 'SE1')
pp.create_sgen(net, bus = 4, p_mw = 160, sn_mva = 200, name = "Wind2", zone = 'SE2')
pp.create_sgen(net, bus = 8, p_mw = 70, sn_mva = 100, name = "Wind3", zone = 'SE3')


# Loads in SE1
pp.create_load(net, bus = 0, p_mw = 1, q_mvar= 1, sn_mva = 50, name = "Load1", zone = 'SE1')
pp.create_load(net, bus = 1, p_mw = 1, q_mvar= 1, sn_mva = 50, name = "Load2", zone = 'SE1')
pp.create_load(net, bus = 2, p_mw = 1, q_mvar= 1, sn_mva = 200, name = "Load3", zone = 'SE1')

# Loads in SE2
pp.create_load(net, bus = 3, p_mw = 1, q_mvar= 1, sn_mva = 100, name = "Load4", zone = 'SE2')
pp.create_load(net, bus = 4, p_mw = 1, q_mvar= 1, sn_mva = 50, name = "Load5", zone = 'SE2')
pp.create_load(net, bus = 5, p_mw = 1, q_mvar= 1, sn_mva = 250, name = "Load6", zone = 'SE2')

# Loads all over SE3
pp.create_load(net, bus = 6, p_mw = 1, q_mvar= 1, sn_mva = 300, name = "Load7", zone = 'SE3')
pp.create_load(net, bus = 7, p_mw = 1, q_mvar= 1, sn_mva = 500, name = "Load8", zone = 'SE3')
pp.create_load(net, bus = 8, p_mw = 1, q_mvar= 1, sn_mva = 500, name = "Load9", zone = 'SE3')
pp.create_load(net, bus = 9, p_mw = 1, q_mvar= 1, sn_mva = 300, name = "Load10", zone = 'SE3')


# Loads all over SE4
pp.create_load(net, bus = 10, p_mw = 1, q_mvar= 1, sn_mva = 300, name = "Load11", zone = 'SE4')
pp.create_load(net, bus = 11, p_mw = 1, q_mvar= 1, sn_mva = 200, name = "Load12", zone = 'SE4')
pp.create_load(net, bus = 12, p_mw = 1, q_mvar= 1, sn_mva = 200, name = "Load13", zone = 'SE4')


geodata = io.StringIO(u"""{"x":{"0":1,"1":5,"2":8,"3":1,"4":5,"5":8,"6":4,"7":8,"8":4,"9":8,"10":4,"11":6,"12":4,"13":-4,"14":10},
        "y":{"0":13.0,"1":12.0,"2":11.0,"3":10.0,"4":9.0,"5":8.0,"6":6.0,"7":6.0,"8":4.0,"9":4.0,"10":2.0,"11":2.0,"12":0.5,"13":7,"14":7},
        "coords":{"0":NaN,"1":NaN,"2":NaN,"3":NaN,"4":NaN,"5":NaN,"6":NaN,"7":NaN,"8":NaN,
        "9":NaN,"10":NaN,"11":NaN,"12":NaN,"13":NaN,"14":NaN}}""")

net.bus_geodata = read_json(geodata)

pp.to_json(net,'./data/Grid_EQ.json')