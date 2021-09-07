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


elec_demand = electricity_demand.stack().tolist()
#elec_price_wholesale = Electricity_price_pivot0
elec_price_household_32_05 = Electricity_price_pivot1
co2_price = df_data
gas_price = gas_p
heat_demand_1 = heat_demand_pivot
heat_demand_1 = heat_demand_1.interpolate(method='linear', limit_direction='forward')
heat_price_1 = heat_p

el_price1 = elec_price_household_32_05.interpolate(method='linear', limit_direction='forward')
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

T = range(8784)
I = range(1)

m = Model("Maximizing profit", sense=maximize, solver_name=CBC)

# variable
y_t = [[m.add_var(lb=0) for i in I] for t in T]  # Electricity generation
el_sold = [m.add_var(lb=0) for t in T]  # electricity sold
el_bought = [m.add_var(lb=0) for t in T]  # electricity bought
x_t = [[m.add_var(lb=0) for i in I] for t in T]  # Fuel consumption
z_t = [[m.add_var(lb=0) for i in I] for t in T]  # Heat generation
# objective function

# Revenue = Electricity price * demand/generation
# Cost = Fuel price = gas price + emission_factor * co2 price

# Max Proft = Revenue - Cost


len(gas_pp)
len(co2_p)



heat_demand_1


# heat_demand_1.isnull()


# heat_demand_1.interpolate(method ='linear', limit_direction ='forward')


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
print(len(heat_demand_norm))
print(len(el_price))


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


# ls = [type(item) for item in el_price]
# print(ls)
# ls = [type(item) for item in el_price]
# print(ls)

# m.objective = xsum((el_price[t] * del_t * el_sold[t]) - ( x_t[t][i] * ( gas_p[i] * del_t + (em_fc * co2_p[t]*del_t))) for t in T for i in I) + ((heat_demand[t] * heat_price[t]) for t in T)



len(heat_price)


m.objective = xsum(el_price[t] * del_t * (el_sold[t]-el_bought[t]) - (x_t[t][i] * (gas_pp[t] * del_t + (em_fc * co2_p[t] * del_t)))
                   for t in T for i in I) + xsum((heat_demand[t] * heat_price[t]) for t in T)


#m.objective = xsum(
#    (el_price[t] * del_t * el_sold[t]) - (x_t[t][i] * (gas_p[i] * del_t + (em_fc * co2_p[t] * del_t))) for t in T for i
#    in I) + ((heat_demand[t] * heat_price[t]) for t in T)

# constraints

for t in T:
    #m += xsum(y_t[t][i] for i in I) == el_demand[t]

    for i in I:
        m += y_t[t][i] <= capacity_el[i]  # electricity generation <= maximum capacity of electricity of the plant

        m += z_t[t][i] <= capacity_ht[i]  # heat generation <= maximum capacity of heat of the plant

        m += x_t[t][i] == y_t[t][i] / eff_plants[i]  # fuel consumption = Electricity generation / efficiency of the plants

        m += heat_demand[t] == z_t[t][i]  # heat demand == Heat generation

        m += y_t[t][i] == heat_ratio * z_t[t][i]  # electricity generation = heat ratio * heat generation

        m += y_t[t][i] +el_bought[t] == el_sold[t] + el_demand[t] # electricity generation = sold electricity + electricity demand

status = m.optimize()
obj = m.objective_value


status

electricity_generation = []# y_t
electricity_sold = [] # el_sold
electricity_bought = [] # el_bought
fuel_consumption = [] # x_t
heat_generation = [] # z_t
if m.num_solutions:
    for t in T:
        electricity_sold.append(el_sold[t].x)
        electricity_bought.append(el_bought[t].x)
        for i in I:
            electricity_generation.append(y_t[t][i].x)
            fuel_consumption.append(x_t[t][i].x)
            heat_generation.append(z_t[t][i].x)


import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10,5)
xx_data = [electricity_generation[:100], electricity_sold[:100], electricity_bought[:100], fuel_consumption[:100], heat_generation[:100]]
xx_label = ["electricity\_generation[:100]", "electricity\_sold[:100]", "electricity\_bought[:100]", "fuel\_consumption[:100]", "heat\_generation[:100]"]

fig = plt.figure()
fig.suptitle("CHP with households price")
ax = plt.subplot(111)


for i,j in zip(xx_data,xx_label):
    ax.plot(i, label='$%s$'%j)

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
