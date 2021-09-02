import pandas as pd
import matplotlib.pyplot as plt 
import datetime
from numpy import nan as Nan

df_data = pd.read_excel("CO22020.xlsx",usecols = "A,B,C",skiprows=4, nrows = 253)


df_data.loc[-1] = ['01.01.2020', Nan, Nan]
df_data.index = df_data.index + 1  # shifting index
df_data.sort_index(inplace=True) 

df_data.Datum = pd.to_datetime(df_data.Datum).dt.date

df_data = df_data.set_index("Datum")
df_data = df_data.asfreq('D')
# is_NaN = df_data.isnull()

df_data = df_data.interpolate(method ='linear', limit_direction ='backward')
df_data['mean_CO2_tax'] = df_data[['Bid', 'Bid']].mean(axis=1)
df_data = df_data[["mean_CO2_tax"]]
print("Co2 Price\n")
print(df_data.head())
