import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def get_trip_duration_and_distance_all_months():
    # We create a list with the name of the .csv files
    taxi_data = ['yellow_tripdata_2018-0'+str(i)+'.csv' for i in range(1,7)]
    # Creating dataframe for prepared data (all months)
    trip_duration_and_distance_df = pd.DataFrame(data={"duration":[], "trip_distance":[]})
    # Setting the path to the files
    path = "D:/"

    # Loop for each file
    for month_data in taxi_data:
        month_data_df = pd.read_csv(path + month_data)
        # Selecting interesting columns
        tmp_trip_duration_df = month_data_df[["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance"]]
        # Calculating trip duration using before defined function
        trip_duration_df = calculate_trip_duration(tmp_trip_duration_df)[["duration", "trip_distance"]]
        # Concatenating prepared data to the dataframe with all months
        trip_duration_and_distance_df = pd.concat([trip_duration_and_distance_df, trip_duration_df])
        # Deleting unnecessary variables for better memory managing
        del trip_duration_df, tmp_trip_duration_df, month_data_df
        return trip_duration_and_distance_df

def plot_cdf(filtered_trip_duration_and_distance_df):
    # Setting the image size and location
    plt.rcParams["figure.figsize"] = [8,3]
    f2, axarr2 = plt.subplots(1, 2)
    # Plotting
    axarr2[0].hist(filtered_trip_duration_and_distance_df.trip_distance, cumulative=True, density=True, bins=100, color="C1")
    axarr2[0].plot([0, 30], [1, 1], 'k-', lw=2)
    axarr2[0].set_title('The trip distance Cumulative DF')

    axarr2[1].hist(filtered_trip_duration_and_distance_df.duration, cumulative=True,  density=True, bins=100, color="C2")
    axarr2[1].plot([0, 100], [1, 1], 'k-', lw=2)
    axarr2[1].set_title('The trip duration Cumulative DF')

def plot_density(filtered_trip_duration_and_distance_df):
    # Setting the image size and location
    plt.rcParams["figure.figsize"] = [12,6]
    f, axarr = plt.subplots(1, 2)

    # Plotting histograms
    axarr[0].hist(filtered_trip_duration_and_distance_df.trip_distance, density=True, bins=100, color="C1")
    axarr[0].set_title('The trip distance distribution')

    axarr[1].hist(filtered_trip_duration_and_distance_df.duration, density=True, bins=100, color="C2")
    axarr[1].set_title('The trip duration distribution')
