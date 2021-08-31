import pandas as pd
import matplotlib.pyplot as plt 
import datetime

df_data = pd.read_excel("NaturalGas2020.xlsx",usecols = "A,D",skiprows=4, nrows = 332)

df_data.Datum = pd.to_datetime(df_data.Datum).dt.date

df_data = df_data.set_index("Datum")
df_data = df_data.asfreq('D')
# is_NaN = df_data.isnull()

df_data = df_data.interpolate(method ='linear', limit_direction ='forward')

gas_p = df_data
gas_p
