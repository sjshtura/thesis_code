import pandas as pd
import matplotlib.pyplot as plt 
import datetime

df_data = pd.read_excel("Wholesale_Electricity_Prices_2020.xlsx")
# print(df_data)

# df_data = df_data.set_index("Gewerbe allgemein")
df_data
#df.index =  pd.to_datetime(df.index, errors='ignore')
#df
df_data

df_data = df_data[['dtDate', 'intHour','dblPrice']]
df_data



df_data.intHour = pd.to_timedelta(df_data.intHour, unit='h')

df_data

df_data.intHour = df_data.intHour.astype(str)
df_data["intHour"]= df_data["intHour"].str.slice(start = 7)
df_data.intHour =  pd.to_datetime(df_data.intHour, errors='ignore', format="%H:%M:%S").dt.time
df_data.dblPrice = df_data.dblPrice * 0.1
df_data
# df_data.dtypes

df_data.dtDate.duplicated(keep = 'last')

df_data.dtypes

Electricity_price_pivot0 = df_data.pivot(index = 'dtDate', columns = 'intHour', values = 'dblPrice')
Electricity_price_pivot0