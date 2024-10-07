
import pandapower as pp
import json


with open('./temp/GLSK_strategies.json','r') as file:
    strategy = json.load(file)


GLSK = []
for n in range (24):
    net = pp.from_json('./data/IGM/D2_IGM_'+ str(n) +'.json')
    glsk = []
    for area in strategy:     # Loop through areas from the strategy
        if (strategy[area] == 0):
            print ('Strategy not implemented')
    
        elif (strategy[area] == 1):
            print ('Strategy not implemented')
    
        elif (strategy[area] == 2):
            print ('Strategy not implemented')
   
        elif (strategy[area] == 3):
            # GSK factors dependent on installed capacity
            units = net.gen.loc[(net.gen['zone'] == area) & (net.gen['name'].str.contains('Hydro'))].name.to_list()
            shift_keys = []
            total_SN = net.gen.loc[(net.gen['zone'] == area) & (net.gen['name'].str.contains('Hydro')),'sn_mva'].sum()
            for unit in units:
                shift_keys.append(net.gen.loc[(net.gen['name'] == unit),'sn_mva'].item()/total_SN)
            glsk.append(dict(zip(units,shift_keys)))
   
        elif (strategy[area] == 4):
            #Flat GSK factors for all generators independently of size of generator
            units = net.gen.loc[(net.gen['zone'] == area) & (net.gen['name'].str.contains('Hydro'))].name.to_list()
            shift_keys = []
            for unit in units:
                shift_keys.append(1/len(units))
            glsk.append(dict(zip(units,shift_keys)))
    
        elif (strategy[area] == 5):
            # GSK factors dependent on current production capacity
            units = net.gen.loc[(net.gen['zone'] == area) & (net.gen['name'].str.contains('Hydro'))].name.to_list()
            shift_keys = []
            total_P = net.gen.loc[(net.gen['zone'] == area) & (net.gen['name'].str.contains('Hydro')),'p_mw'].sum()
            for unit in units:
                if total_P > 0:
                    shift_keys.append(net.gen.loc[(net.gen['name'] == unit),'p_mw'].item()/total_P)
                else:
                    shift_keys.append(1/len(units)) # If total production is 0, units share equally (defaults to Strategy 4)
            glsk.append(dict(zip(units,shift_keys)))
    
        elif (strategy[area] == 6):
            print ('Strategy not implemented')
    
        elif (strategy[area] == 7):
            # GSK factors dependent on current load capacity
            loads = net.load.loc[(net.load['zone'] == area)].name.to_list()
            shift_keys = []
            total_Pl = net.load.loc[(net.load['zone'] == area),'p_mw'].sum()
            for load in loads:
                if total_Pl > 0:
                    shift_keys.append(net.load.loc[(net.load['name'] == load),'p_mw'].item()/total_Pl)
                else:
                    shift_keys.append(1/len(loads)) # If total load is 0, units share equally (defaults to Strategy 8)
            glsk.append(dict(zip(loads,shift_keys)))
    
        elif (strategy[area] == 8):
            #Flat GSK factors for all loads independently of size of load
            loads = net.load.loc[(net.load['zone'] == area)].name.to_list()
            shift_keys = []
            for load in loads:
                shift_keys.append(1/len(loads))
            glsk.append(dict(zip(loads,shift_keys)))
        elif (strategy[area] == 9):
            print ('Strategy not implemented')

    GLSK.append(dict(zip(strategy.keys(),glsk)))
    
    with open('./data/ToRCC/IG-103.json','w') as file:
        json.dump(GLSK, file)