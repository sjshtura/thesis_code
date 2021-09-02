import pandas as pd
import matplotlib.pyplot as plt 
import datetime

df_data = pd.read_excel("when2heat_DE.xlsx",sheet_name='Sheet2',usecols = "A,B,C,J",skiprows=3)

df_data["Unnamed: 1"]= df_data["Unnamed: 1"].str.slice(start = 11)
df_data["unit"]= df_data["unit"].str.slice(stop = 10)
sum_column = df_data["MW"] + df_data["MW.7"]
df_data["heat_demand"] = sum_column


df_data = df_data.drop(['MW','MW.7'], axis = 1)
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