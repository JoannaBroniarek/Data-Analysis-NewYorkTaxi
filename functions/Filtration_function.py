import pandas

def filter():
    months = ['0'+str(i) for i in range(1,7)]
    for month in months:
        taxi = pandas.read_csv('yellow_tripdata_2018-'+month+'.csv',sep=',', encoding='ISO-8859-1')
        
        #We delete data from wrong months and years
        taxi = taxi[list(map(lambda x: x[2:7] == '18-'+month, taxi["tpep_pickup_datetime"].values))]
        taxi = taxi[list(map(lambda x: x[2:7] == '18-'+month, taxi["tpep_dropoff_datetime"].values))]
        
        #We delete the trip where the departing time is later the arriving time
        taxi = taxi[list(map(lambda x: 0<x<100, (pandas.to_datetime(taxi['tpep_dropoff_datetime'])-pandas.to_datetime(taxi['tpep_pickup_datetime'])).astype('timedelta64[m]')))]
            
        #We filter the trip checking if the trip distance is ok
        taxi = taxi[list(map(lambda x: 0<x<50, taxi['trip_distance'].values))]
        
        #We save them in a new file with the same as before, but cleaned_ as a prefix
        taxi.to_csv('cleaned_yellow_tripdata_2018-'+month+'.csv')
