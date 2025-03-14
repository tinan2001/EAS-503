#install libraries

import geopandas as geop
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

## Reading shapefiles
park_shp = geop.read_file(r'C:\Users\Tinanope28\Box\Mini Project\Parks_Buffalo\geo_export_5d2f0589-8fd7-4028-856a-31a8e619d536.shp')
censusdata = geop.read_file(r'C:\Users\Tinanope28\Box\Mini Project\censusdata_clip.shp')


## Census Data Manipulation
median_income = 31918                    # Median Income Level Threshold in 2015
above_below_income = []

for i, row in censusdata.iterrows():     # Create a new list to append to dataframe that categorizes census tracts above and below median income level
    if row['medincomeE'] >= median_income:
        above_below_income.append('Above Median Income')
    else:
        above_below_income.append('Below Median Income')

censusdata['Above/Below Median Income'] = above_below_income

## Park Data Manipulation


park_shp['year'] = park_shp['year'].astype(int)                             # Changing Year from float to int, I did not want to keep this a float becausee if I were to display it, it would appear with a decimal point 


park = park_shp[['name_label','year', 'acres', 'objectid', 'geometry']]     # Creating new geodataframe
park = park.sort_values(by ='year', ascending = True)


for i, row in park.iterrows():                                              # Remove Years = 0 (no year association). Years = 0 are considered extreme since I cannot categorize them correctly, there were like only 3 parks so I decided to leave them out of the study
    if row['year'] == 0:
        park = park.drop(axis = 'index', index = i)

# Adding New Column for categorizing Years into interval years
intyear = []

for i, row in park.iterrows():
    if ((row['year'] >= 1820) and (row['year'] <= 1839)):
        intyear.append("1820 to 1839")
    elif ((row['year'] >= 1840) and (row['year'] <= 1859)):
        intyear.append("1840 to 1859")
    elif ((row['year'] >= 1860) and (row['year'] <= 1879)):
        intyear.append("1860 to 1879")
    elif ((row['year'] >= 1880)) and ((row['year'] <= 1899)):
        intyear.append("1880 to 1899")
    elif ((row['year'] >= 1900)) and ((row['year'] <= 1919)):
        intyear.append("1900 to 1919")    
    elif ((row['year'] >= 1920)) and ((row['year'] <= 1939)):
        intyear.append("1920 to 1939")    
    elif ((row['year'] >= 1940)) and ((row['year'] <= 1959)):
        intyear.append("1940 to 1959")
    elif ((row['year'] >= 1960)) and ((row['year'] <= 1979)):
        intyear.append("1960 to 1979")
    elif ((row['year'] >= 1980)) and ((row['year'] <= 1999)):
        intyear.append("1980 to 1999")
    elif ((row['year'] >= 2000)) and ((row['year'] <= 2019)):
        intyear.append("2000 to 2019")
    else:
        continue
park['intervalyear'] = intyear
park['intervalyear'] = park['intervalyear'].astype('category')


# I created a park dictionary. I wanted to utilize dictionaries since I just learned about it in class.
# Overall the dictionary was actually very difficult to interate through, so I used the dictionary to get the lengths of park characteristics
# the dictionary key is park intervals and the values are the parks within those intervals

park_dictionary = {}
vicenniel_year_intervals =list(range(1830, 2031,20))

park_dictionary = {}
yearinterval_x = []
no_parks_y = []

for i, row in park.iterrows():
    year = row['year']

    first_year = (year// 20) * 20
    last_year = first_year + 19

    year_interval = (f'{first_year} to {last_year}') #the key to the dictionary
    

    if year_interval not in park_dictionary:
        park_dictionary[year_interval] = []
        yearinterval_x.append (year_interval)
        
    park_dictionary[year_interval].append(row)

for key in park_dictionary:
    no_parks_y.append(len(park_dictionary[key]))


##GRAPHS
# this bargraph is number of parks constructed using lists and the dictionary above
title_dict = {'fontsize': 15, 'fontweight' : 'bold'}
sns.set_theme(style="whitegrid", palette="pastel")
sns.color_palette("Set2", len(yearinterval_x))
fig, axy = plt.subplots(figsize=(16, 10))
sns.barplot(x = yearinterval_x, y = no_parks_y, hue = yearinterval_x, palette = "Set2", ax = axy)
axy.set_title('No. of Parks Constructed in the City of Buffalo Over Twenty-Year Intervals', pad = 15, fontdict = title_dict )
axy.set_ylabel("Number of Parks Constructed", labelpad = 15)
axy.set_xlabel("Twenty-Year Intervals", labelpad = 15)
for p in axy.patches:
    axy.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=12, color='black', xytext=(0, 10), textcoords='offset points')

# this linegraph is number of parks constructed using lists and the dictionary above   
title_dict = {'fontsize': 15, 'fontweight' : 'bold'}
sns.set_theme(style="whitegrid", palette="pastel")
sns.color_palette("Set2", len(yearinterval_x))
fig, axy = plt.subplots(figsize=(16, 10))
sns.lineplot(x = yearinterval_x, y = no_parks_y, palette = "Set2", ax = axy)
axy.set_title('No. of Parks Constructed in the City of Buffalo Over Twenty-Year Intervals', pad = 15, fontdict = title_dict )
axy.set_ylabel("Number of Parks Constructed", labelpad = 15)
axy.set_xlabel("Twenty-Year Intervals", labelpad = 15)
for p in axy.patches:
    axy.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=12, color='black', xytext=(0, 10), textcoords='offset points')

##This dictionary was used to calculate average size of parks
for key, value in park_dictionary.items(): #in value list
    
    park_dict_list = []
    
    for i, series in enumerate(value):
        temp_dictionary = {} 

        for i, items in enumerate(series):
            if (i == 0):
                temp_dictionary ['Park Name'] = items
            elif (i == 1):
                temp_dictionary ['Establish Year'] = items
            elif (i == 2):
                temp_dictionary ['Area'] = items*4046.86
            elif (i == 3):
                temp_dictionary['Object_ID'] = items
            else:
                temp_dictionary['Geometry'] = items #this is still a geometry type
        
        park_dict_list.append(temp_dictionary)
    
    park_dictionary[key] = park_dict_list

average_size_park_y = []

for key in park_dictionary:
    sum_size = 0
    num_size = 0
    for values in park_dictionary[key]:
            sum_size += values['Area']
            num_size += 1


    average_size_park_y.append(round(sum_size/num_size,2))

#GRAPHS   
# this bargraph is park size using lists and the dictionary above
title_dict = {'fontsize': 15, 'fontweight' : 'bold'}
sns.set_theme(style="whitegrid", palette="pastel")
fig, axy = plt.subplots(figsize=(16, 10))
sns.barplot(x = yearinterval_x, y = average_size_park_y, hue = yearinterval_x, palette = "Set2", ax = axy)
axy.set_title('Avg. Park Size Constructed in the City of Buffalo Over Twenty-Year Intervals', pad = 15, fontdict = title_dict )
axy.set_ylabel("Avg. Size Park Constructed (Squared Meters)", labelpad = 15)
axy.set_xlabel("Twenty-Year Intervals", labelpad = 15)
for p in axy.patches:
    axy.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=12, color='black', xytext=(0, 10), textcoords='offset points')

# this linegraph is park size using lists and the dictionary above
title_dict = {'fontsize': 15, 'fontweight' : 'bold'}
sns.set_theme(style = "whitegrid", palette = "pastel")
fig, axy = plt.subplots(figsize=(16, 10))
sns.lineplot(x = yearinterval_x, y = average_size_park_y, palette = "Set2", ax = axy)
axy.set_title('Avg. Park Size Constructed in the City of Buffalo Over Twenty-Year Intervals', pad = 15, fontdict = title_dict )
axy.set_ylabel("Avg. Size Park Constructed (Squared Meters)", labelpad = 15)
axy.set_xlabel("Twenty-Year Intervals", labelpad = 15)
for p in axy.patches:
    axy.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), ha ='center', va ='center', fontsize = 12, color = 'black', xytext=(0, 10), textcoords='offset points')
    

##MAPS
#first park map
park_plot = park.plot   (column = 'intervalyear',
                        categorical = True,
                        cmap='brg',
                        edgecolor = 'black',
                        figsize = (15,15),
                        legend = True,
                        legend_kwds = {'loc': 'lower left', 'edgecolor': 'black'})
park_plot.set_title('Park Establishment Through through Twenty-Year Intervals')

#Census map
census_map = censusdata.plot (column = 'Above/Below Median Income',
                              cmap = 'Accent',
                              edgecolor = 'white',
                              figsize = (15,15),
                              legend = True,
                              legend_kwds = {'loc': 'upper right', 'edgecolor': 'black'})
census_map.set_title('Median Income Within Buffalo, NY Census Tracts')

#combined map of park and census
fig, ax = plt.subplots(figsize = (15, 15))

census_map = censusdata.plot (ax = ax,
                              column = 'Above/Below Median Income',
                              cmap = 'Accent',
                              edgecolor = 'white',
                              figsize = (15,15),
                              legend = True,
                              legend_kwds = {'loc': 'upper right', 'edgecolor': 'black'})
                

c_park = park.plot (ax = ax,
                    column = 'intervalyear',
                    categorical = True,
                    cmap='brg',
                    edgecolor = 'black',
                    figsize = (15,15),
                    legend = True,
                    legend_kwds = {'loc': 'lower left', 'edgecolor': 'black'})
c_park.set_title('Buffalo Parks in Buffalo Census Tracts')