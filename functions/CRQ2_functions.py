import pandas as pd
import branca.colormap as cm

def get_cleaned_data():
    cleaned_taxi_data = ['cleaned_yellow_tripdata_2018-0'+str(i)+'.csv' for i in range(1,7)]
    # Creating dataframe for prepared data (all months)
    cleaned_taxi_data_df = pd.DataFrame(data={"PULocationID":[], "DOLocationID":[]})
    # Loop for each file
    for month_data in cleaned_taxi_data:
        month_data_df = pd.read_csv("D:/" + month_data)[["PULocationID", "DOLocationID"]]
        cleaned_taxi_data_df = pd.concat([cleaned_taxi_data_df, month_data_df])
        print(month_data)
    return cleaned_taxi_data_df

def prepare_and_draw_colormap(grouped_by_zone, column = 'PULocationID', file='Colormaps_.html'):
    """
    Arguments:
        grouped_by_zone -- the data frame merged previously with taxi_zone_lookup
        column -- the column used in marging (i.e. PULocationID, DOLocationID)
        file -- name of the file where the map will be saved
    """
    # Finding minimal and maximal value in dataset
    if column=='difference':
        min_val = grouped_by_zone[column].min()
        max_val = grouped_by_zone[column].max()
        zones_counts = grouped_by_zone[column].reset_index()
        zone_dict = zones_counts.set_index('Zone')['difference']
        # Defining function for intensity od colors
        linear = cm.LinearColormap(
        ['blue', 'white', 'red'],
        vmin=-1*max_val, vmax=max_val)
    else:
        min_val = grouped_by_zone[column].min()[0]
        max_val = grouped_by_zone[column].max()[0]
        # Creating the dictionary with {'Zone': number of trips}
        zones_counts = grouped_by_zone[column]['count'].reset_index()
        zone_dict = zones_counts.set_index('Zone')['count']
        # Defining function for intensity od colors
        linear = cm.LinearColormap(
        ['green', 'yellow', 'red'],
        vmin=min_val, vmax=max_val)
    # Defining the function for coloring
    def my_color_function(feature, zone_dict = zone_dict, names = False):
        try:
            return linear(zone_dict[feature['properties']['zone']])
        except Exception as e:
            print(e)
            return '#FFFFFF'
    # Drawing the map
    m = folium.Map([40.7, -74], tiles='cartodbpositron', zoom_start=10)
    linear.add_to(m) # adding the colorbar

    gj = folium.GeoJson(
        data = geojson,
        style_function=lambda feature: {
            'fillColor': my_color_function(feature),
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.5,
            'popup': "aaa"
        }
    ).add_to(m)
    m.save(file)
    return m
