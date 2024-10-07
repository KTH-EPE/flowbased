import pandas as pd
import pandapower as pp

net = pp.from_json('./data/Grid_EQ.json')

# Read the output files from the pandapower timeseries powerflow

res_line_p_from_mw = pd.read_json('./temp/res_line/p_from_mw.json').T
res_line_p_to_mw = pd.read_json('./temp/res_line/p_to_mw.json').T
res_line_q_from_mvar = pd.read_json('./temp/res_line/q_from_mvar.json').T
res_line_loading_percent = pd.read_json('./temp/res_line/loading_percent.json').T
res_gen_p_mw = pd.read_json('./temp/res_gen/p_mw.json').T
res_gen_q_mvar = pd.read_json('./temp/res_gen/q_mvar.json').T
res_bus_vm_pu = pd.read_json('./temp/res_bus/vm_pu.json').T
res_bus_va_degree = pd.read_json('./temp/res_bus/va_degree.json').T
res_bus_p_mw = pd.read_json('./temp/res_bus/p_mw.json').T
gen_p_mw = pd.read_json('./temp/gen/p_mw.json').T
gen_q_mvar = pd.read_json('./temp/gen/q_mvar.json').T
sgen_p_mw = pd.read_json('./temp/sgen/p_mw.json').T
sgen_q_mvar = pd.read_json('./temp/sgen/q_mvar.json').T
load_p_mw = pd.read_json('./temp/load/p_mw.json').T
load_q_mvar = pd.read_json('./temp/load/q_mvar.json').T
res_ext_grid_p_mw = pd.read_json('./temp/res_ext_grid/p_mw.json').T

# Create a list to hold 24 complete net objects with the results of the powerflow simulation

IGM = []

for n in range (24):
    igm = pp.pandapowerNet(net)
    igm.res_gen['p_mw'] = res_gen_p_mw[n]
    igm.res_gen['q_mvar'] = res_gen_q_mvar[n]
    igm.res_bus['vm_pu'] = res_bus_vm_pu[n]
    igm.res_bus['p_mw'] = res_bus_p_mw[n]
    igm.res_bus['va_degree'] = res_bus_va_degree[n]
    igm.res_line['p_from_mw'] = res_line_p_from_mw[n]
    igm.res_line['p_to_mw'] = res_line_p_to_mw[n]   
    igm.res_line['q_from_mvar'] = res_line_q_from_mvar[n]
    igm.res_line['loading_percent'] = res_line_loading_percent[n]
    igm.gen['p_mw'] = gen_p_mw[n]
    igm.gen['q_mvar'] = gen_q_mvar[n]
    igm.sgen['p_mw'] = sgen_p_mw[n]
    igm.sgen['q_mvar'] = sgen_q_mvar[n]
    igm.load['p_mw'] = load_p_mw[n]
    igm.load['q_mvar'] = load_q_mvar[n]
    igm.res_ext_grid['p_mw'] = res_ext_grid_p_mw[n]
    pp.to_json(igm,'./data/IGM/D2_IGM_'+ str(n) +'.json')
    IGM.append(igm)