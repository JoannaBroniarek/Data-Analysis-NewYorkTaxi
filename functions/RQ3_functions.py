import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def calculate_trip_duration(df):
    """
    Function returns a dataframe with additional column 'trip_duration'.
    'trip_duration' is a time in minutes between tpep_pickup_datetime and tpep_dropoff_datetime
    """
    # Converting colums from 'string' type to 'datetime' type
    drop_off = pd.to_datetime(df.tpep_dropoff_datetime)
    pick_up = pd.to_datetime(df.tpep_pickup_datetime)

    # Adding a new column 'duration' converted to minutes [m]
    df['duration'] = (drop_off - pick_up).astype('timedelta64[m]')
    return df

def get_trip_duration_all_months(path = "D:/"):
    #We create a list with the name of the .csv files
    taxi_data = ['yellow_tripdata_2018-0'+str(i)+'.csv' for i in range(1,7)]
    # Creating dataframe for prepared data (all months)
    trip_duration_all_months_df = pd.DataFrame(data={"duration":[], "PULocationID":[], "DOLocationID":[]})
    # Loop for each file
    for month_data in taxi_data:
        month_data_df = pd.read_csv(path + month_data)
        # Selecting interesting columns
        tmp_trip_duration_df = month_data_df[["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"]]
        # Calculating trip duration using before defined function
        trip_duration_df = calculate_trip_duration(tmp_trip_duration_df)[["duration", "PULocationID", "DOLocationID"]]
        # Concatenating prepared data to the dataframe with all months
        trip_duration_all_months_df = pd.concat([trip_duration_all_months_df, trip_duration_df])
        # Deleting unnecessary variables for better memory menaging
        del trip_duration_df, tmp_trip_duration_df,
        #trip_duration_all_months_df.to_csv("trip_duration_all_months_df.csv")
    return trip_duration_all_months_df

def plot_distribution_trip_duration(filtered_trip_duration_df):
    h1 = plt.hist(filtered_trip_duration_df.duration, bins=100, density=True, color="red")
    mean_ = filtered_trip_duration_df.duration.mean()
    mode_ = filtered_trip_duration_df.duration.mode()[0]
    plt.vlines(x=[mean_, mode_], color = ["black", "blue"], ymin=0, ymax=0.07)
    plt.xlabel('The trip duration'); plt.ylabel('Density'); plt.title('The distribution of the trip duration')
    plt.grid(True); plt.show()

def merge_and_group_by(filtered_trip_duration_df):
    # Merging prepared data with 'taxi_lookup_file' in order to get information about the broughs
    trip_duration_location = pd.merge(filtered_trip_duration_df, taxi_zone_lookup, left_on='PULocationID' , right_on='LocationID')
    # Selecting the columns for "duration - borough" analysis. We need only two columns.
    trip_duration_borough = trip_duration_location[['duration', 'Borough']]
    grouped_trip_duration_borough = trip_duration_borough.groupby(['Borough'])
    return grouped_trip_duration_borough
