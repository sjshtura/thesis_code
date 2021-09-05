import pandas as pd
import matplotlib.pyplot as plt 

df_data = pd.read_excel("Representative Profile VDEW.xls", sheet_name = 'G0')
df_data

df_data = df_data.set_index("Gewerbe allgemein")
df_data
#df.index =  pd.to_datetime(df.index, errors='ignore')
#df
df_data
df_winter = df_data.iloc[:,0:3]
df_winter
df_winter = df_winter[1:98]
df_winter
df_winter.columns = df_winter.iloc[0]
df_winter = df_winter.drop(df_winter.index[0])
df_winter

df_winter.index = df_winter.index.astype(str)
df_winter.index = pd.to_datetime(df_winter.index, errors='ignore')
df_winter = df_winter.astype(float)
df_winter = df_winter.resample('60T').mean()
df_winter.index = df_winter.index.astype(str)
df_winter.head()

# fig = plt.figure(figsize=(20, 6), dpi=80)
# fig.suptitle('Gewerbe Winter', fontsize=20)
# plt.plot(df_winter["Samstag"], label = "Samstag")
# plt.plot(df_winter["Sonntag"], label = "Sonntag")
# plt.plot(df_winter["Werktag"], label = "Werktag")
# plt.xticks(rotation=90)
# plt.legend(loc='upper right')

#df_winter.plot(figsize=(15, 4))

df_data
df_sommer = df_data.iloc[:,3:6]
df_sommer
df_sommer = df_sommer[1:98]
df_sommer.columns = df_sommer.iloc[0]
df_sommer = df_sommer.drop(df_sommer.index[0])
df_sommer.index = df_sommer.index.astype(str)
df_sommer.index =  pd.to_datetime(df_sommer.index, errors='ignore')
df_sommer = df_sommer.astype(float)
df_sommer = df_sommer.resample('60T').mean()
df_sommer.index = df_sommer.index.astype(str)
df_sommer.head()

# fig = plt.figure(figsize=(20, 6), dpi=80)
# fig.suptitle('Gewerbe Sommer', fontsize=20)
# plt.plot(df_sommer["Samstag"], label = "Samstag")
# plt.plot(df_sommer["Sonntag"], label = "Sonntag")
# plt.plot(df_sommer["Werktag"], label = "Werktag")
# plt.xticks(rotation=90)
# plt.legend(loc='upper right')

df_data
df_ubergangszeit = df_data.iloc[:,6:9]
df_ubergangszeit
df_ubergangszeit = df_ubergangszeit[1:98]
df_ubergangszeit.columns = df_ubergangszeit.iloc[0]
df_ubergangszeit = df_ubergangszeit.drop(df_ubergangszeit.index[0])

df_ubergangszeit.index = df_ubergangszeit.index.astype(str)
df_ubergangszeit.index =  pd.to_datetime(df_ubergangszeit.index, errors='ignore')
df_ubergangszeit = df_ubergangszeit.astype(float)
df_ubergangszeit = df_ubergangszeit.resample('60T').mean()
df_ubergangszeit.index = df_ubergangszeit.index.astype(str)
df_ubergangszeit.head()



# fig = plt.figure(figsize=(20, 6), dpi=80)
# fig.suptitle('Gewerbe Übergangszeit', fontsize=20)
# plt.plot(df_ubergangszeit["Samstag"], label = "Samstag")
# plt.plot(df_ubergangszeit["Sonntag"], label = "Sonntag")
# plt.plot(df_ubergangszeit["Werktag"], label = "Werktag")
# plt.xticks(rotation=90)
# plt.legend(loc='upper right')


# https://stackoverflow.com/questions/47150709/how-to-create-a-calendar-table-date-dimension-in-pandas

def create_date_table(start='2020-01-01', end='2020-12-31'):
    start_ts = pd.to_datetime(start).date()

    end_ts = pd.to_datetime(end).date()

    # record timetsamp is empty for now
    dates =  pd.DataFrame(columns=['Record_timestamp'],
        index=pd.date_range(start_ts, end_ts))
    dates.index.name = 'Date'

    days_names = {
        i: name
        for i, name
        in enumerate(['Monday', 'Tuesday', 'Wednesday',
                      'Thursday', 'Friday', 'Saturday', 
                      'Sunday'])
    }

    dates['Day'] = dates.index.dayofweek.map(days_names.get)
    dates['Month'] = dates.index.month
    dates.reset_index(inplace=True)
    dates.index.name = 'date_id'
    return dates

df = create_date_table()
import numpy as np


df


# create a list of our conditions
conditions = [
    (df['Day'] == "Monday"),
    (df['Day'] == "Tuesday"),
    (df['Day'] == "Wednesday"),
    (df['Day'] == "Thursday"),
    (df['Day'] == "Friday"),
    (df['Day'] == "Saturday"),
    (df['Day'] == "Sunday")
    ]

# create a list of the values we want to assign for each condition
values = ['Werktag', 'Werktag', 'Werktag', 'Werktag','Werktag', 'Samstag', 'Sonntag']

# create a new column and use np.select to assign values to it using our lists as arguments
df['Gewerbe allgemein'] = np.select(conditions, values)

# display updated DataFrame
df.head()

date_day = df[["Date", "Day", "Month","Gewerbe allgemein"]]
date_day_winter = date_day[(date_day["Month"]==1)|(date_day["Month"]==2)|(date_day["Month"]==12)]
date_day_winter.head()


df_winter.reset_index(inplace=True)
df_winter["Gewerbe allgemein"] = pd.to_datetime(df_winter["Gewerbe allgemein"].str.replace(' ', ' ')).dt.time
df_winter
df_winter = df_winter.set_index("Gewerbe allgemein")
df_winter_T= df_winter.T
df_winter_T

date_day_winter.head()

final_df_winter = date_day_winter.join(df_winter_T, on="Gewerbe allgemein")
final_df_winter.head()

date_day_fall_spring = date_day[(date_day["Month"]==3)|(date_day["Month"]==4)|(date_day["Month"]==5)|(date_day["Month"]==9)|(date_day["Month"]==10)|(date_day["Month"]==11)]
date_day_fall_spring.head()

df_ubergangszeit.head()

df_ubergangszeit.head()

df_ubergangszeit.reset_index(inplace=True)
df_ubergangszeit["Gewerbe allgemein"] = pd.to_datetime(df_ubergangszeit["Gewerbe allgemein"].str.replace(' ', ' ')).dt.time
df_ubergangszeit
df_ubergangszeit = df_ubergangszeit.set_index("Gewerbe allgemein")
df_ubergangszeit_T= df_ubergangszeit.T
df_ubergangszeit_T.head()

final_df_ubergangszeit = date_day_fall_spring.join(df_ubergangszeit_T, on="Gewerbe allgemein")
final_df_ubergangszeit.head()

date_day_sommer = date_day[(date_day["Month"]==6)|(date_day["Month"]==7)|(date_day["Month"]==8)]
date_day_sommer.head()

df_sommer.head()

df_sommer.reset_index(inplace=True)
df_sommer["Gewerbe allgemein"] = pd.to_datetime(df_sommer["Gewerbe allgemein"].str.replace(' ', ' ')).dt.time
df_sommer
df_sommer = df_sommer.set_index("Gewerbe allgemein")
df_sommer_T= df_sommer.T
df_sommer_T.head()

final_df_sommer = date_day_sommer.join(df_sommer_T, on="Gewerbe allgemein")
final_df_sommer.head()

final_data = pd.concat([final_df_winter,final_df_sommer,final_df_ubergangszeit])
final_data.head()

final_data = pd.concat([final_df_winter[:60],final_df_ubergangszeit[:92],final_df_sommer,final_df_ubergangszeit[92:],final_df_winter[60:]])
# final_data
final_data.head()

final_data_new = final_data.drop(['Day','Month', 'Gewerbe allgemein'], axis = 1)
final_data_new.head()
electricity_demand = final_data_new.set_index("Date")
# electricity_demand
# final_data.to_excel("Final_dataframe.xlsx")
print("electricity demand\n")
print(electricity_demand.head())