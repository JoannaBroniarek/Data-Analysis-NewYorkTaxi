import pandas as pd
import matplotlib.pyplot as plt

def get_number_of_pick_ups(month=1):
    
    month = pd.read_csv('yellow_tripdata_2018-0'+str(month)+'.csv')
    month['tpep_pickup_datetime'] = pd.to_datetime(month.tpep_pickup_datetime)
    
    # count the number of PICK UPs per day
    month['Day'] = month.tpep_pickup_datetime.dt.day
    
    # plot the number of PICK UPs per day
    m = month.Day.value_counts().sort_index()
    #plt.plot(m, kind = "bar",figsize=(11,6))
    plt.title("Month: "+ str(month))
    #plt.ylabel("Number of pick ups")
    #plt.xlabel("Days of the month")
    return m
