import numpy as np
# gas-turbine CHP plant = (O&M) costs are approximately $40/kWe. /  32.88 EUR
# gas-engine CHP plan = (O&M) costs are approximately $250/kWe /  205.47 EUR
o_and_m_cost = [32.88, 205.47]

discount_rate = 0.10 # discount rate

t = 25 # Time in years

# for i in range(len(el_demand)):
#     revenue = revenue + (el_price[i] * el_demand[i])
# print(revenue)
#obj_value_CHP_households = -60390.867027
obj_value_CHP_boiler_households = -111973.814621
obj_value_boiler_households = -298032.965737

#obj_value_CHP_wholesale = 3863.946646
obj_value_CHP_boiler_wholesale = 1571.975079
obj_value_boiler_wholesale = -4651.8844947

#revenue = obj_value_CHP_households - obj_value_CHP_boiler_households
revenue0 = obj_value_CHP_boiler_households - obj_value_boiler_households
revenue1 = obj_value_CHP_boiler_wholesale - obj_value_CHP_boiler_wholesale

invest = 1000

for i in range(len(o_and_m_cost)):
    NPV = -invest + (revenue1 - o_and_m_cost[i])/((1 + discount_rate)**t) # will get positive value

        # investment value - NPV -> if
        #NPV = (obj_CHP_boiler - obj_boiler) - O&M_cost).... -> NPV CHP

    print(f"For operation cost {o_and_m_cost[i]} net present value is: {NPV}")


