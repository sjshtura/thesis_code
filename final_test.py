# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:02:03 2021

@author: Christian
"""

from mip import Model, xsum, maximize, BINARY

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


# elec_demand = electricity_demand
# elec_price_wholesale = Electricity_price_pivot0
# elec_price_household_32_05 = Electricity_price_pivot1
# co2_price = df_data
# gas_price = gas_p
# heat_demand_1 = heat_demand_pivot
# heat_price_1 = heat_p


# el_price = elec_price_wholesale # Electricity price
# del_t = .25 # duration of time step
# el_demand = electricity_demand # Electicity demand


# gas_p = gas_price # Gas price for different plants
# em_fc = 0.2 # emission factor
# co2_p = co2_price # CO2 Price
# capacity_el = elec_capacity # maximum capacity of electricity for the power plants
# capacity_ht = heat_capacity # maximum capacity of heat for the power plants
# heat_demand = heat_demand_1 # heat demand
# heat_price = heat_price_1 # heat price
# heat_ratio = 400/385 # heat ratio


# eff_plants = elec_eff # the efficiency of the power plants
