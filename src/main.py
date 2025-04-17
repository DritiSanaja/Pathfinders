import pandas as pd

# Load the datasets 
trip_data = pd.read_excel('./data/FLEXI_trip_data.xlsx')  
bus_stops = pd.read_excel('./data/FLEXI_bus_stops.xlsx')  

# Merge data to get pickup and dropoff coordinates
merged_data = trip_data.merge(bus_stops, left_on='Pickup ID', right_on='index', suffixes=('', '_pickup'))
merged_data = merged_data.merge(bus_stops, left_on='Dropoff ID', right_on='index', suffixes=('', '_dropoff'))

# Drop extra index columns to avoid exposing unnecessary data
merged_data = merged_data.drop(columns=['index', 'index_dropoff'])

# Convert time columns to datetime
merged_data['Actual Pickup Time'] = pd.to_datetime(merged_data['Actual Pickup Time'])
merged_data['Actual Dropoff Time'] = pd.to_datetime(merged_data['Actual Dropoff Time'])

# Calculate trip duration in minutes
merged_data['Trip Duration (minutes)'] = (merged_data['Actual Dropoff Time'] - merged_data['Actual Pickup Time']).dt.total_seconds() / 60

# columns selection for heatmap visualization
heatmap_data = merged_data[['Booking ID', 'Pickup ID', 'Dropoff ID',
                            'Actual Pickup Time', 'Actual Dropoff Time',
                            'latitude', 'longitude', 'latitude_dropoff', 'longitude_dropoff', "name", "district", "Passenger status"]]

# Rename columns for clarity
heatmap_data = heatmap_data.rename(columns={
    'latitude': 'Pickup Latitude',
    'longitude': 'Pickup Longitude',
    'latitude_dropoff': 'Dropoff Latitude',
    'longitude_dropoff': 'Dropoff Longitude'
})

# Filter the data based on Pickup and Dropoff IDs
heatmap_data = heatmap_data[(heatmap_data['Pickup ID'] <= 69) & (heatmap_data['Dropoff ID'] <= 69)]

# Display the cleaned and filtered data (Be mindful of what is printed)
print(heatmap_data[['Booking ID', 'Pickup ID', 'Dropoff ID', 'Pickup Latitude', 'Pickup Longitude']].head())  # Example of selective printing
