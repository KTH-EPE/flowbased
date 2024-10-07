'''
This script creates two dataFrames

The first consisting of forecasts for the coming
24 hours per production type and load for each bidding zone
This DataFrame is stored as a json file to be read by the main notebook

The second dataframe consists of NP ber bidding zone and border flows
resulting from the typed forecasts in the previous dataframe
This DataFrame is stored as a json file to be read by the main notebook
'''

import pandas as pd
import os
N = 24
types = ['Hydro','Wind','Nuclear','Load','NP']
bz = {'SE1':[6/12,1/2,0,1/8],
      'SE2':[5/12,1/3,0,1/8],
      'SE3':[1/12,1/6,1,1/2],
      'SE4':[0,0,0,1/4],
      'NO':[0,0,0,0],
      'FI':[0,0,0,0]}

wind = pd.Series    ([100,100,100,100,100,0,0,100,200,200,200,400,400,600,600,400,300,300,300,300,300,300,100,100])
nuclear = pd.Series ([500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500])
load = pd.Series    ([600,600,900,900,900,900,1600,2000,2600,2900,2900,3000,3000,3000,2900,2700,2500,2900,2700,2300,1500,1300,1100,900])
hydro_list = []
for n in range (N):
    if (load[n]-nuclear[n]-wind[n] > 0):
        hydro_list.append(load[n]-nuclear[n]-wind[n])
    else:
        hydro_list.append(0)

hydro = pd.Series(hydro_list)

# break the total numbers down into data per bidding zone and determine NPs ber bz
CGMA ={}
if not os.path.exists('./data/CGMA'):
    os.mkdir('./data/CGMA')
for area,share in bz.items():
    np = (hydro*share[0]).round()+(wind*share[1]).round()+(nuclear*share[2]).round()-(load*share[3]).round()
    CGMA[area] = pd.concat([(hydro*share[0]).round(),(wind*share[1]).round(),(nuclear*share[2]).round(),(load*share[3]).round(),np],axis= 1)
    CGMA[area].columns = types
    CGMA[area].to_json('./data/CGMA/CGMA_' + area +'.json')

