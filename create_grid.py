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

# One line along the production centers in SE1
pp.create_line(net, from_bus=0, to_bus=1, length_km = 200, std_type = 'Line220kV', name = "T-P")
pp.create_line(net, from_bus=1, to_bus=2, length_km = 200, std_type = 'Line220kV', name = "P-L")
#Two lines connecting SE1 and SE2
pp.create_line(net, from_bus=1, to_bus=4, length_km = 300, std_type = 'Line400kV', name = "P-Å")
pp.create_line(net, from_bus=2, to_bus=5, length_km = 300, std_type = 'Line400kV', name = "L-S")
# One line along the production centers in SE2
pp.create_line(net, from_bus=3, to_bus=4, length_km = 200, std_type = 'Line220kV', name = "Ö-Å")
pp.create_line(net, from_bus=4, to_bus=5, length_km = 200, std_type = 'Line220kV', name = "Å-S")
#Two lines connecting SE2 and SE3
pp.create_line(net, from_bus=4, to_bus=6, length_km = 400, std_type = 'Line400kV', name = "Å-K")
pp.create_line(net, from_bus=5, to_bus=7, length_km = 400, std_type = 'Line400kV', name = "S-S")
# 5 lines in a meshed config  in SE3, varying voltage levels
pp.create_line(net, from_bus=6, to_bus=7, length_km = 150, std_type = 'Line400kV', name = "K-S")
pp.create_line(net, from_bus=7, to_bus=9, length_km = 150, std_type = 'Line400kV', name = "S-O")
pp.create_line(net, from_bus=7, to_bus=8, length_km = 150, std_type = 'Line220kV', name = "S-G")
pp.create_line(net, from_bus=6, to_bus=8, length_km = 150, std_type = 'Line400kV', name = "K-G")
pp.create_line(net, from_bus=8, to_bus=9, length_km = 300, std_type = 'Line220kV', name = "G-O")
# 2 lines connecting SE3 and SE4
pp.create_line(net, from_bus=8, to_bus=10, length_km = 200, std_type = 'Line400kV', name = "G-M")
pp.create_line(net, from_bus=9, to_bus=11, length_km = 200, std_type = 'Line400kV', name = "O-K")
# 3 lines in a meshed config  in SE4, varying voltage levels
pp.create_line(net, from_bus=10, to_bus=11, length_km = 150, std_type = 'Line400kV', name = "M-K")
pp.create_line(net, from_bus=10, to_bus=12, length_km = 150, std_type = 'Line220kV', name = "M-Y")
pp.create_line(net, from_bus=11, to_bus=12, length_km = 150, std_type = 'Line220kV', name = "K-Y")
# External grid connection at bus 7 in SE3 representing Forsmark
pp.create_ext_grid(net, bus = 7, name = "Nuclear1")
# Hydropower production in SE1 and SE2
pp.create_gen(net, bus = 0, p_mw = 400, sn_mva = 600, vm_pu=1.0, name = "Hydro1", zone = 'SE1')
pp.create_gen(net, bus = 1, p_mw = 300, sn_mva = 400, vm_pu=1.0, name = "Hydro2", zone = 'SE1')
pp.create_gen(net, bus = 3, p_mw = 300, sn_mva = 400, vm_pu=1.0, name = "Hydro3", zone = 'SE2')
pp.create_gen(net, bus = 4, p_mw = 300, sn_mva = 400, vm_pu=1.0, name = "Hydro4", zone = 'SE2')
# Nuclear & Hydro production in SE3
pp.create_gen(net, bus = 9, p_mw = 450, sn_mva = 700, vm_pu=1.0, name = "Nuclear2", zone = 'SE3')
pp.create_gen(net, bus = 6, p_mw = 200, sn_mva = 300, vm_pu=1.0, name = "Hydro5", zone = 'SE3')
pp.create_gen(net, bus = 8, p_mw = 450, sn_mva = 700, vm_pu=1.0, name = "Nuclear3" , zone = 'SE3')
# Wind production in SE1, SE2 and SE3
pp.create_sgen(net, bus = 1, p_mw = 200, sn_mva = 300, name = "Wind1", zone = 'SE1')
pp.create_sgen(net, bus = 4, p_mw = 160, sn_mva = 200, name = "Wind2", zone = 'SE2')
pp.create_sgen(net, bus = 8, p_mw = 70, sn_mva = 100, name = "Wind3", zone = 'SE3')
# Loads along coast in SE1 and SE2
pp.create_load(net, bus = 2, p_mw = 150, q_mvar= 1, name = "Load1", zone = 'SE1')
pp.create_load(net, bus = 5, p_mw = 150, q_mvar= 1, name = "Load2", zone = 'SE2')
# Loads all over SE3
pp.create_load(net, bus = 6, p_mw = 300, q_mvar= 1, name = "Load3", zone = 'SE3')
pp.create_load(net, bus = 7, p_mw = 300, q_mvar= 1, name = "Load4", zone = 'SE3')
pp.create_load(net, bus = 8, p_mw = 300, q_mvar= 1, name = "Load5", zone = 'SE3')
pp.create_load(net, bus = 9, p_mw = 300, q_mvar= 1, name = "Load6", zone = 'SE3')
# Loads all over SE4
pp.create_load(net, bus = 10, p_mw = 300, q_mvar= 1, name = "Load7", zone = 'SE4')
pp.create_load(net, bus = 11, p_mw = 300, q_mvar= 1, name = "Load8", zone = 'SE4')
pp.create_load(net, bus = 12, p_mw = 150, q_mvar= 1, name = "Load9", zone = 'SE4')

geodata = io.StringIO(u"""{"x":{"0":1,"1":5,"2":8,"3":1,"4":5,"5":8,"6":4,"7":8,"8":4,"9":8,"10":4,"11":6,"12":4},
        "y":{"0":13.0,"1":12.0,"2":11.0,"3":10.0,"4":9.0,"5":8.0,"6":6.0,"7":6.0,"8":4.0,"9":4.0,"10":2.0,"11":2.0,"12":0.5},
        "coords":{"0":NaN,"1":NaN,"2":NaN,"3":NaN,"4":NaN,"5":NaN,"6":NaN,"7":NaN,"8":NaN,
        "9":NaN,"10":NaN,"11":NaN,"12":NaN}}""")

net.bus_geodata = read_json(geodata)

pp.to_json(net,'./Grid_EQ.json')