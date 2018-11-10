import pandas
from collections import defaultdict
import matplotlib.pyplot
import scipy.stats

#This function reads the file zone lookup and return a dictonary with as entrys the names of the boroughs and as values a list with the IDs of the associated zones
def boroughsIdentifyer():
    #We load the lookup table with the names of the zones and the rispective codes
    zones = pandas.read_csv('taxi _zone_lookup.csv',sep=',', encoding='ISO-8859-1')
    
    boroughs = defaultdict(list)
    
    #We create the dicontary    
    for number,name in list(zip(zones["LocationID"].values,zones["Borough"].values)): 
        boroughs[name].append(number)
        
    #We delete the IDs associated to unknow zones considering them an error
    boroughs.pop('Unknown')
    
    #We return it
    return dict(boroughs)

#This function, given the dictonary of the boroughs, returns a dictonary of data frames: one for each boroughs containing the P values and the P-wighted values
def price_calculator(boroughs):
    
    #We define a function to calculate the duration of the trips that directly modify the data frame
    def calculate_trip_duration(df):
        #Converting colums from 'string' type to 'datetime' type
        drop_off = pandas.to_datetime(df.tpep_dropoff_datetime)
        pick_up = pandas.to_datetime(df.tpep_pickup_datetime)
    
        #Adding a new column 'duration' converted to minutes [m]
        df['duration'] = (drop_off - pick_up).astype('timedelta64[m]')
        return df
    
    #We create a dictonary of dataframe to be populated with the values of P and Pw
    taxi_boroughs = {borough:pandas.DataFrame(columns=['P','Pw']) for borough in boroughs}
    
    #We create a list with the month numbers we are interested in
    months = ['0'+str(i) for i in range(1,7)]
    for month in months:
        
        #We load the file
        taxi = pandas.read_csv('cleaned_yellow_tripdata_2018-'+month+'.csv',sep=',', encoding='ISO-8859-1')

        #We delete the wrong columns, add the value we need and filter them eliminating odd results. Then we delete all the others columns
        taxi = calculate_trip_duration(taxi)
        taxi['P'] = taxi['fare_amount']/taxi['trip_distance']
        taxi = taxi[taxi['P']<15]
        taxi = taxi[0<taxi['P']]
        taxi['Pw'] = taxi['P']/taxi['duration']
        
        #We populate our dictonary filtering the dataframe by boroughs
        for borough in boroughs.keys():
            taxi_boroughs[borough] = taxi_boroughs[borough].append(pandas.DataFrame(taxi[taxi['PULocationID'].isin(boroughs[borough])],columns = ['P','Pw']))
            
    return taxi_boroughs
    
#We build a function that, given our data frame and the list of boroughs, return the mean and standard deviation for both P and Pw
def mean_and_std(df_dict,boroughs):
    #We compute the mean and standard deviation using the dedicated pandas function
    means = pandas.DataFrame({borough:df_dict[borough].mean() for borough in boroughs})
    stds = pandas.DataFrame({borough:df_dict[borough].std(ddof = 0) for borough in boroughs})
    
    #We reorganize our values in some convenient data frame
    Pdf = pandas.DataFrame()
    Pdf['Mean'] = means.loc['P']
    Pdf['Std'] = stds.loc['P']
    
    Pwdf = pandas.DataFrame()
    Pwdf['Mean'] = means.loc['Pw']
    Pwdf['Std'] = stds.loc['Pw']
    
    return (Pdf.sort_values(by = ['Mean'],ascending = False),Pwdf.sort_values(by = ['Mean'],ascending = False))

#We build a function that will give us two set of plots: one for P and one for Pw
def grapher(df,boroughs):
    
    #We build two dictonaris where we count how many trip for each value of P and Pw (approximated) there are
    grapherP = {borough:defaultdict(int) for borough in boroughs}
    grapherPw = {borough:defaultdict(int) for borough in boroughs}
    for borough in boroughs:
        for v in df[borough]['P'].values.tolist():
            grapherP[borough][round(v, 1)] += 1
        for v in df[borough]['Pw'].values.tolist():
            grapherPw[borough][round(v, 1)] += 1
            
    #We draw 6 graphs, one for each borough, for the values of P
    print('Plot for the values of P on the x-axis and how many occurences on the y-axis')    
    figP, axesP = matplotlib.pyplot.subplots(nrows=2, ncols=3, figsize = (16,10))
    c = 0
    for borough in boroughs:
        axesP[c % 2, c % 3].scatter(*zip(*[x for x in sorted(list(grapherP[borough].items()),key = lambda x: x[0])]),s=1)
        axesP[c % 2, c % 3].set_title(borough)
        c+=1
    matplotlib.pyplot.show()
    
    #We draw 6 graphs, one for each borough, for the values of Pw
    print('Plot for the values of Pw on the x-axis and how many occurences on the y-axis')        
    figPw, axesPw = matplotlib.pyplot.subplots(nrows=2, ncols=3, figsize = (16,10))
    c = 0
    for borough in boroughs:
        axesPw[c % 2, c % 3].scatter(*zip(*[x for x in sorted(list(grapherPw[borough].items()),key = lambda x: x[0])]),s=1)
        axesPw[c % 2, c % 3].set_title(borough)
        c+=1
    matplotlib.pyplot.show()
    
#We define a function that given the data frame and the boroughs do the t-test for each couple of boroughs and return two dataframe, one for P and the other for Pw, contaning the p-values
def ttester(df,boroughs):
    
    #We make a dicontary of dictonaris having as keys, at both levels, the names of the boroughs. We populate it with the p-values of the t-tests
    ttestsP = {borough:{} for borough in boroughs}
    for b1 in boroughs:
        for b2 in boroughs:
            #We round the values at the 3-th deciaml as we are interested in a treshold of 0.05 for the p-values
            ttestsP[b1][b2] = round(list(scipy.stats.ttest_ind(df[b1]['P'],df[b2]['P']))[1],3)
   
    #We do the same thing for Pw         
    ttestsPw = {borough:{} for borough in boroughs}
    for b1 in boroughs:
        for b2 in boroughs:
            ttestsPw[b1][b2] = round(list(scipy.stats.ttest_ind(df[b1]['Pw'],df[b2]['Pw']))[1],3)
    #and return them after a conversion in dataframes        
    return (pandas.DataFrame(ttestsP).reindex(sorted(boroughs.keys()), axis=1), pandas.DataFrame(ttestsPw).reindex(sorted(boroughs.keys()), axis=1))
