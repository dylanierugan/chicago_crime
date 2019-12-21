import geopandas as gpd
import pandas
import matplotlib.pyplot as plt

chicago_crime_data = open('Crimes_-_2012_to_present.csv')
chicago_crime_data_frame = pandas.read_csv(chicago_crime_data)

communities = gpd.read_file('Boundaries_Community.geojson')

def com_count(df, col, value, unique_id, com_num):
    
    """Returns count of unique_id in df com_num rows 
    w/entry value in column col"""
    
    rows = df[df[col] == value] # boolean slice of rows we want
    if com_num not in rows['Community Area'].values:
        return 0
    grouped = rows.groupby('Community Area')
    return grouped[unique_id].count()[com_num]


ls = []
for area in communities['area_num_1']:
    ls.append(area)

def make_dictionary(df, col, value, unique_id):
    
    ''' Creates a dictionary where the key is one of 1-77 Chicago 
    districts. The value is the number of crimes in that district since 
    2012. Edit'''
    
    crime_dictionary = {}
    for x in ls:
        com_num = int(x)
        crime_dictionary[x] = com_count(df, col, value, unique_id, com_num)
    return crime_dictionary

homicide_dict = make_dictionary(chicago_crime_data_frame, 'Primary Type', 'HOMICIDE', 'Case Number')
battery_dict = make_dictionary(chicago_crime_data_frame, 'Primary Type', 'BATTERY', 'Case Number')

communities['Total_Homi'] = homicide_dict.values()

fig, ax = plt.subplots()
fig.set_size_inches (10, 10)
communities.plot(column='Total_Homi', scheme='quantiles',
edgecolor='black', ax=ax, legend=True, cmap= 'winter')
plt.title('Chicago Homicides by Region')

homocide_values_list = homicide_dict.values()
homocide_max = max(homocide_values_list)
for item in homicide_dict.keys():
    homicide_dict[item] = homicide_dict[item] / homocide_max
    
communities['Total_Homi_scaled'] = homicide_dict.values()

fig, ax = plt.subplots() 
fig.set_size_inches (10, 10)
communities.plot(column='Total_Homi_scaled', scheme='equalinterval',
edgecolor='black', ax=ax, legend=True, cmap= 'winter')
plt.title('Chicago Homicides Scaled by Region')
battery_values_list = battery_dict.values()

battery_max = max(battery_values_list)
for item in battery_dict.keys():
    battery_dict[item] = battery_dict[item] / battery_max
    
communities['Total_Battery_scaled'] = homicide_dict.values()

fig, ax = plt.subplots() 
fig.set_size_inches (10, 10)
communities.plot(column='Total_Battery_scaled', scheme='equalinterval',
edgecolor='black', ax=ax, legend=True, cmap= 'autumn')
plt.title('Chicago Batteries Scaled by Region')