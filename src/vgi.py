import openrouteservice
import folium
import pandas as pd
import os
from dotenv import load_dotenv
from streamlit_folium import folium_static

# Load environment variables from .env file
load_dotenv()

# Initialize ORS client with your API key from the .env file
ors_client = openrouteservice.Client(key=os.getenv("ORS_API_KEY"))

# Load data (adjust paths as needed)
bus_stops_df = pd.read_excel('/Users/shendsanaja/Downloads/FLEXI_bus_stops.xlsx', engine='openpyxl')
trip_data_df = pd.read_excel('/Users/shendsanaja/Downloads/FLEXI_trip_data.xlsx', engine='openpyxl')

completed_trips = trip_data_df[trip_data_df['Passenger status'] == 'Trip completed']
print("Completed Trips Sample:\n", completed_trips.head())

# Merge to get pickup coordinates and rename them explicitly
pickup_coords = completed_trips.merge(bus_stops_df, left_on='Pickup ID', right_on='index', how='left')
pickup_coords = pickup_coords.rename(columns={'latitude': 'pickup_lat', 'longitude': 'pickup_lon', 'name': 'pickup_name'})
print("After Pickup Merge Sample:\n", pickup_coords[['Pickup ID', 'pickup_lat', 'pickup_lon', 'pickup_name']].head())

# Merge to get dropoff coordinates and rename them explicitly
dropoff_coords = pickup_coords.merge(
    bus_stops_df,
    left_on='Dropoff ID',
    right_on='index',
    how='left',
    suffixes=('_pickup', '_dropoff')
)

# Explicitly rename dropoff columns
dropoff_coords = dropoff_coords.rename(columns={'latitude': 'dropoff_lat', 'longitude': 'dropoff_lon', 'name': 'dropoff_name'})
print("After Dropoff Merge Sample:\n", dropoff_coords[['Dropoff ID', 'dropoff_lat', 'dropoff_lon', 'dropoff_name']].head())

# Filter rows to ensure complete pickup and dropoff coordinates
dropoff_coords_clean = dropoff_coords.dropna(subset=['pickup_lat', 'pickup_lon', 'dropoff_lat', 'dropoff_lon'])
print("Cleaned Dropoff Coordinates Sample:\n", dropoff_coords_clean[['pickup_lat', 'pickup_lon', 'dropoff_lat', 'dropoff_lon']].head())

# Step 3: Initialize map
map_center = [bus_stops_df['latitude'].mean(), bus_stops_df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# Sample 10 random completed trips
sampled_trips = dropoff_coords_clean.sample(10, random_state=1)

# Proceed with the rest of the code using sampled_trips
for i, row in sampled_trips.iterrows():
    pickup_point = (row['pickup_lon'], row['pickup_lat'])
    dropoff_point = (row['dropoff_lon'], row['dropoff_lat'])

    try:
        route = ors_client.directions(
            coordinates=[pickup_point, dropoff_point],
            profile='driving-car',
            format='geojson'
        )

        # Extract route coordinates for plotting
        route_coords = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]

        # Add route to map
        folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=0.7).add_to(m)

        # Add pickup and dropoff markers
        folium.Marker(
            location=[row['pickup_lat'], row['pickup_lon']],
            popup=f"Pickup: {row['pickup_name']}",
            icon=folium.Icon(color="blue"),
        ).add_to(m)

        folium.Marker(
            location=[row['dropoff_lat'], row['dropoff_lon']],
            popup=f"Dropoff: {row['dropoff_name']}",
            icon=folium.Icon(color="green"),
        ).add_to(m)

    except Exception as e:
        print(f"Error fetching route for trip {i}: {e}")
        st.write(f"Error fetching route for trip {i}: {e}")  # Provide user feedback in case of error

# Display map in Streamlit
folium_static(m)

# Save the map to HTML file (optional)
m.save("vgi_flexi_real_routes_map.html")
