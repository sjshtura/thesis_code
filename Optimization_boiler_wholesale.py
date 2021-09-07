# %%

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:02:03 2021

@author: Christian
"""
import numpy as np
import pandas as pd
from mip import Model, xsum, maximize, BINARY, CBC

from Co2_price import df_data
from electricity_demand import electricity_demand
from Electricity_Price0 import Electricity_price_pivot0
from Electricity_Price1 import Electricity_price_pivot1
from gas_price import gas_p
from heat_demand import heat_demand_pivot
from heat_price import heat_p
from elec_effciency import elec_eff
from electricity_capacity import elec_capacity
from heat_capacity import heat_capacity
from heat_boiler_capacity import heat_cap
from heat_boiler_efficiency1 import heat_eff

elec_demand = electricity_demand.values.tolist()
elec_price_wholesale = Electricity_price_pivot0
elec_price_household_32_05 = Electricity_price_pivot1
co2_price = df_data
gas_price = gas_p
heat_demand_1 = heat_demand_pivot
heat_demand_1 = heat_demand_1.interpolate(method='linear', limit_direction='forward')
heat_price_1 = heat_p

el_price1 = elec_price_wholesale.interpolate(method='linear', limit_direction='forward')
el_price = el_price1.stack().tolist()  # Electricity price
del_t = 1  # duration of time step
el_demand = electricity_demand.stack().tolist()  # Electicity demand

gas_pp = gas_price["Preis"].values.tolist()  # Gas price for different plants
em_fc = 0.2  # emission factor
co2_p = co2_price["mean_CO2_tax"].values.tolist()  # CO2 Price
capacity_el = elec_capacity.stack().tolist()  # maximum capacity of electricity for the power plants
capacity_ht = heat_capacity.stack().tolist()  # maximum capacity of heat for the power plants
heat_demand = heat_demand_1.stack().tolist()  # heat demand
heat_price = heat_price_1.stack().tolist()  # heat price
heat_ratio = 400 / 385  # heat ratio
eff_plants = elec_eff.stack().tolist()  # the efficiency of the power plants

capacity_ht_boiler = heat_cap.stack().tolist()
eff_boiler = heat_eff.stack().tolist()

T = range(8784)

J = range(1)  # J: boiler in set of boilers J
# K = range(1)  # k: CHP in set of CHP plants K

I = range(1)  # CHP

m = Model("Maximizing profit", sense=maximize, solver_name=CBC)

# variable
y_t = [[m.add_var(lb=0) for i in I] for t in T]  # Electricity generation
el_sold = [m.add_var(lb=0) for t in T]  # electricity sold
el_bought = [m.add_var(lb=0) for t in T]  # electricity bought
x_t = [[m.add_var(lb=0) for i in I] for t in T]  # Fuel consumption by CHP
z_t = [[m.add_var(lb=0) for i in I] for t in T]  # Heat generation by CHP
x_tb = [[m.add_var(lb=0) for j in J] for t in T]  # Fuel consumption by Boiler
z_tb = [[m.add_var(lb=0) for j in J] for t in T]  # Heat generation by Boiler
# objective function

# Revenue = Electricity price * demand/generation
# Cost = Fuel price = gas price + emission_factor * co2 price

# Max Proft = Revenue - Cost
heat_demand_norm = [((element / max(heat_demand)) * 385) for element in heat_demand]
heat_demand = heat_demand_norm

print(len(co2_price))
print(len(el_demand))
print(len(gas_pp))
print(len(co2_p))
print(len(capacity_el))
print(len(capacity_ht))
print(len(heat_demand))
print(len(heat_price))
print(len(eff_plants))
print(len(capacity_ht_boiler))
print(len(eff_boiler))

print(type(el_demand))
print(type(gas_pp))
print(type(co2_p))
print(type(capacity_el))
print(type(capacity_ht))
print(type(heat_demand))
print(type(heat_price))
print(type(eff_plants))
print(type(heat_demand_norm))
print(type(el_price))

m.objective = xsum(
    el_price[t] * del_t * (el_sold[t] - el_bought[t]) - (x_t[t][i] * (gas_pp[t] * del_t + (em_fc * co2_p[t] * del_t)))
    for i in I for t in T) - xsum((x_tb[t][j] * (gas_pp[t] * del_t + (em_fc * co2_p[t] * del_t)))
                                  for j in J for t in T) + xsum((heat_demand[t] * heat_price[t]) for t in T)

# constraints

for t in T:

    m += heat_demand[t] <= xsum(z_t[t][i] for i in I) + xsum(z_tb[t][j] for j in J)  # heat demand >= Heat generation
    m += xsum(y_t[t][i] for i in I) + el_bought[t] == el_sold[t] + el_demand[
        t]  # electricity generation + bought electricity = sold electricity + electricity demand

    for j in J:
        m += z_tb[t][j] <= capacity_ht_boiler[j]  # heat generation <= maximum capacity of heat of the plant
        m += x_tb[t][j] == z_tb[t][j] / eff_boiler[j]  # fuel consumption = Heat generation / efficiency of the plants
    for i in I:
        m += y_t[t][i] <= capacity_el[i]  # electricity generation <= maximum capacity of electricity of the plant
        m += z_t[t][i] <= capacity_ht[i]  # heat generation <= maximum capacity of heat of the plant
        m += x_t[t][i] == y_t[t][i] / eff_plants[
            i]  # fuel consumption = Electricity generation / efficiency of the plants
        m += y_t[t][i] == heat_ratio * z_t[t][i]  # electricity generation >= heat ratio * heat generation

status = m.optimize()
obj = m.objective_value

status
