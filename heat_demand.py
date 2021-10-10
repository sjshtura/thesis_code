import pandas as pd
import matplotlib.pyplot as plt 
import datetime

df_data = pd.read_excel("when2heat_DE.xlsx",sheet_name='Sheet2',usecols = "A,B,D,I",skiprows=3)

df_data["Unnamed: 1"]= df_data["Unnamed: 1"].str.slice(start = 11)
df_data["unit"]= df_data["unit"].str.slice(stop = 10)
sum_column = df_data["MW.1"] + df_data["MW.6"]
df_data["heat_demand"] = sum_column


df_data = df_data.drop(['MW.1','MW.6'], axis = 1)
df_data.unit =  pd.to_datetime(df_data.unit, errors='ignore')
df_data

df_data.columns = ["date", "hour", "heat_demand"]
# df_data['date'] = df_data['date'].dt.date
df_data.hour =  pd.to_datetime(df_data.hour, errors='ignore', format="%H:%M:%S").dt.time
df_data

df_data = df_data.drop_duplicates(['date', 'hour'])
df_data

heat_demand_pivot = df_data.pivot(index = 'date', columns = 'hour', values = 'heat_demand')
heat_demand_pivot = heat_demand_pivot*1000
print("heat demand\n")
print(heat_demand_pivot.head())


import numpy as np
heat_demand_pivot_plot = heat_demand_pivot[1:8]
heat_demand_pivot_plot.reset_index(drop=True, inplace=True)



fig = plt.figure(figsize=(20, 7), dpi=80)
plt.xticks(np.array(range(len(heat_demand_pivot_plot.columns))), heat_demand_pivot_plot.columns)
plt.xticks(rotation=90)
for i in range(6):
    plt.plot(np.array(range(len(heat_demand_pivot_plot.columns))), np.array(heat_demand_pivot_plot.iloc[i].values))
#plt.plot(np.array(range(len(heat_demand_pivot_plot.columns))), np.array(heat_demand_pivot_plot.iloc[1].values))
plt.show()

