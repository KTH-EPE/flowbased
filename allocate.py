'''
This script reads the CGMA forecast files and allocates  loads across the generators
in the bidding zone. The script respects the generation types HYdro, Wind and Thermal

A feature to be added in the future is to ignore allocation to some generators to reflect
the possibility that not all generators in the real grid are modelled in the systems.

If viewed from the CCC process, the role of this script is to create an SSH file with
P and Q values to be merged with the "EQ-file" consisting of grid data

The output from the script is a json file consisting of named units and their P & Q values

'''

import pandapower as pp
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
N = 24
tan_fi = 0.328 # representing a universal powerfactor of 0.95
bidzones = ['SE1','SE2','SE3','SE4']
gen_types = ['Hydro','Nuclear']

# First step is to read the EQ file to get the grid structure
net = pp.from_json('./data/Grid_EQ.json')

# Then determine the share for each generator for each generator type per bidzone
for area in bidzones:
    for generator in gen_types:
        units = net.gen.loc[net.gen.zone == area][net.gen['name'].str.contains(generator)] # All generators of gen_type in the area
        unit_base = units['sn_mva'].sum() # determine total installed base of generator type in the bidzone
        if unit_base > 0:
            units['p_mw'] = units['sn_mva']/unit_base # Using the p_mw key to temporarily store the generator share
        else:
            units['p_mw'] = 0
        net.gen.update(units)
    wind_units = net.sgen.loc[net.sgen.zone == area]
    wind_unit_base = wind_units['sn_mva'].sum()
    if wind_unit_base >0:
        wind_units['p_mw']=wind_units['sn_mva']/wind_unit_base
    else:
        wind_units['p_mw'] = 0
    net.sgen.update(wind_units)
    loads = net.load.loc[net.load.zone == area]
    loads['p_mw'] = 1/len(loads)
    loads['q_mvar'] = 1/len(loads)*tan_fi
    net.load.update(loads)


'''
Next we need to create the datastructure that will store the "SSH-file"
To match the Pandapower powerflow format, this should be a dataframe
with all generators (gen) and Static generators (sgen) as columns and
the time steps (0..23) as rows. Similarly all loads - both P and Q values
should be stored in a similar dataframe

We do this by looping through all generators and create a time series for each generator
append the series to the complete dataFrame and do this until all gen and sgen have been
added. Then do the same for the loads - for both P and Q
'''

generators = list(net.gen['name'].T)
SSH = pd.DataFrame(columns = generators)
for area in bidzones:
    plans = pd.read_json('./data/CGMA/CGMA_'+ area +'.json')
    for generator in generators:
        if (net.gen[net.gen.name == generator]['zone'].item() == area):
            share = net.gen.loc[net.gen.name == generator,'p_mw'].sum()
            values = [] # An empty list to store the coming 24 values
            for n in range (N):
                if ('Hydro' in generator):
                    values.append(plans['Hydro'][n]*share)
                if ('Nuclear' in generator):        
                    values.append(plans['Nuclear'][n]*share)
            SSH[generator] = pd.Series(values)

windfarms = list(net.sgen['name'].T)
SSH = pd.concat([SSH, pd.DataFrame(columns = windfarms)])
for area in bidzones:
    forecasts = pd.read_json('./data/CGMA/CGMA_'+ area +'.json')
    for windfarm in windfarms:
        if (net.sgen[net.sgen.name == windfarm]['zone'].item() == area):
            share = net.sgen.loc[net.sgen.name == windfarm,'p_mw'].sum()
            values = [] # An empty list to store the coming 24 values
            for n in range (N):
                values.append(forecasts['Wind'][n]*share)
            SSH[windfarm] = pd.Series(values)

loads = list(net.load['name'].T)
col = []
for load in loads:
    col.append(load+'_p')
    col.append(load+'_q')
SSH = pd.concat([SSH, pd.DataFrame(columns = col)])
for area in bidzones:
    load_forecasts = pd.read_json('./data/CGMA/CGMA_'+ area +'.json')
    for load in loads:
        if (net.load[net.load.name == load]['zone'].item() == area):
            share_p = net.load.loc[net.load.name == load,'p_mw'].sum()
            share_q = net.load.loc[net.load.name == load,'q_mvar'].sum()
            values_p = [] # An empty list to store the coming 24 values
            values_q = [] # An empty list to store the coming 24 values
            for n in range (N):
                values_p.append(load_forecasts['Load'][n]*share_p)
                values_q.append(load_forecasts['Load'][n]*share_q)
            SSH[load+'_p'] = pd.Series(values_p)
            SSH[load+'_q'] = pd.Series(values_q)           

SSH.to_json('./data/Grid_SSH.json',orient="records", indent=1)

