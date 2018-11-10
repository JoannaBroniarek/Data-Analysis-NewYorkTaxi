import pandas
from collections import defaultdict

#This function read the file zone lookup and return a dictonary with as entrys the name of the boroughs and as values a list with the IDs of the associated zones
def boroughsIdentifyer():
    #We load the lookup tables with the name of the zones and the rispective codes
    zones = pandas.read_csv('taxi _zone_lookup.csv',sep=',', encoding='ISO-8859-1')
    
    boroughs = defaultdict(list)
    
    #We create the dicontary    
    for number,name in list(zip(zones["LocationID"].values,zones["Borough"].values)): 
        boroughs[name].append(number)
        
    #We delete the IDs associated to unknow zones considering them an error
    boroughs.pop('Unknown')
    
    #We return it
    return dict(boroughs)

#This function take the list of the boroughs and creates a dictonary and a data frame contaning the number of ride for time slot both for the whole city and for each single borough
def time_slotter(boroughs):
    #We create dictonarys with as keys different time slots that we will use to count the rides starting in these time slots
    time_slots_boroughs = {name:{'6-10':0, '10-12':0,'12-15':0,'15-17':0,'17-22':0,'22-6':0} for name in boroughs.keys()}
    
    time_slots = {'6-10':0, '10-12':0,'12-15':0,'15-17':0,'17-22':0,'22-6':0}
    
    #We define a function that counts the number of trip in a data frame and put them in a dictonary
    def _time_slotter(taxi_df, times_dict, month):
        #We extract, from the list of departing time, a list containing two int: one give us the year of the trip, the other the hour of the day for the trip
        for t in map(lambda x: [x[2:7],int(x[11:13])], taxi_df["tpep_pickup_datetime"].values.tolist()): 
            #We ignor trips not done in the relevant month of the 2018 (example: wrongly registered, registered in other years)
            if t[0] == '18-'+month:
                if 6<t[1]<=10:
                    times_dict['6-10']+=1
                elif 10<t[1]<=12:
                    times_dict['10-12']+=1
                elif 12<t[1]<=15:
                    times_dict['12-15']+=1
                elif 15<t[1]<=17:
                    times_dict['15-17']+=1
                elif 17<t[1]<=22:
                    times_dict['17-22']+=1
                elif 22<t[1] or t[1]<=6:
                    times_dict['22-6']+=1
        return times_dict
    
    
    #We create a list with the month number we are interested in
    months = ['0'+str(i) for i in range(1,7)]
    #Now we read the files month by month to don't overload the memory and call our function time_slotter on it
    for month in months:
    
        taxi = pandas.read_csv('yellow_tripdata_2018-'+month+'.csv',sep=',', encoding='ISO-8859-1')
    
        #We call the function defined above to count the total number of rides
        time_slots = _time_slotter(taxi, time_slots, month)
    
        #and we call it iteratively on the different boroughs
        for borough in time_slots_boroughs.keys():
            time_slots_boroughs[borough] = _time_slotter(taxi.loc[taxi['PULocationID'].isin(boroughs[borough])],time_slots_boroughs[borough],month)
    
    #We convert the second diconary in a data frame and we order his columns        
    time_df = pandas.DataFrame(time_slots_boroughs)
    time_df = time_df.reindex(['6-10', '10-12','12-15','15-17','17-22','22-6'])
    
    
    return(time_slots,time_df)
