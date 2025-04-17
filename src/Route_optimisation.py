import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Mapbox API Key 
mapbox_api_key = os.getenv("MAPBOX_API_KEY")

# Fixed shuttle positions
shuttle_positions = {
    "Shuttle 1": {"lat": 49.014689777777775, "lon": 11.401692111111112},
    "Shuttle 2": {"lat": 49.0354084, "lon": 11.469803200000001}
}

# Function to get real route details from Mapbox Directions API
def get_real_route_mapbox(api_key, start, end):
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{start[0]},{start[1]};{end[0]},{end[1]}"
    params = {
        "access_token": api_key,
        "geometries": "geojson",
        "overview": "full",
        "annotations": "distance,duration",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['routes']:
            route = data['routes'][0]['geometry']['coordinates']
            distance = data['routes'][0]['distance'] / 1000  # Convert to kilometers
            duration = data['routes'][0]['duration'] / 60  # Convert to minutes
            co2_emission = distance * 120  # Estimate CO₂ emissions (e.g., 120 grams per km)
            return route, distance, duration, co2_emission
    else:
        st.write(f"Error fetching route data from Mapbox: {response.status_code}")
    return None, None, None, None

# Define a cost function based on distance, time, and emissions
def calculate_cost(distance, time, passengers, co2_emission):
    distance_weight, time_weight, passengers_weight, co2_weight = 1.0, 1.0, 0.5, 1.0
    return (distance_weight * distance) + (time_weight * time) + (passengers_weight * passengers) + (co2_weight * co2_emission)

# Main application
st.title("Live Shuttle Tracking and Route Optimization")

# Simulate a live pickup/drop-off request
pickup_coordinates = [11.4105, 49.0201]  # Example pickup coordinates [longitude, latitude]
dropoff_coordinates = [11.4200, 49.0300]  # Example drop-off coordinates
passenger_count = st.slider("Select Number of Passengers", min_value=1, max_value=8, value=3)

# Calculate costs for each shuttle and find the best one to assign
routes, distances, durations, co2_emissions, costs = {}, {}, {}, {}, {}
for shuttle_name, shuttle_location in shuttle_positions.items():
    shuttle_start = [shuttle_location["lon"], shuttle_location["lat"]]

    # Route from shuttle to pickup
    route_to_pickup, dist_to_pickup, time_to_pickup, co2_to_pickup = get_real_route_mapbox(mapbox_api_key, shuttle_start, pickup_coordinates)

    # Route from pickup to drop-off
    route_to_dropoff, dist_to_dropoff, time_to_dropoff, co2_to_dropoff = get_real_route_mapbox(mapbox_api_key, pickup_coordinates, dropoff_coordinates)

    if route_to_pickup and route_to_dropoff:
        # Combine routes and calculate total distance, duration, and CO₂ emissions
        combined_route = route_to_pickup + route_to_dropoff
        total_distance = dist_to_pickup + dist_to_dropoff
        total_duration = time_to_pickup + time_to_dropoff
        total_co2 = co2_to_pickup + co2_to_dropoff

        # Calculate cost for this shuttle
        cost = calculate_cost(total_distance, total_duration, passenger_count, total_co2)

        # Store results for each shuttle for visualization (all shuttles)
        routes[shuttle_name] = combined_route
        distances[shuttle_name] = total_distance
        durations[shuttle_name] = total_duration
        co2_emissions[shuttle_name] = total_co2
        costs[shuttle_name] = cost

# Select the shuttle with the lowest cost
if costs:
    selected_shuttle = min(costs, key=costs.get)
    selected_route = routes[selected_shuttle]
    selected_distance = distances[selected_shuttle]
    selected_duration = durations[selected_shuttle]
    selected_co2_emission = co2_emissions[selected_shuttle]

    # Display the selected shuttle and route information
    st.write(f"**Selected Shuttle for Pickup**: {selected_shuttle}")
    st.write(f"Route Distance: {selected_distance:.2f} km")
    st.write(f"Travel Time: {selected_duration:.2f} minutes")
    st.write(f"CO₂ Emissions: {selected_co2_emission:.2f} grams")

    # Map visualization for the selected shuttle
    m = folium.Map(location=[pickup_coordinates[1], pickup_coordinates[0]], zoom_start=13, tiles="cartodbpositron")

    # pickup and drop-off markers
    folium.Marker([pickup_coordinates[1], pickup_coordinates[0]], tooltip="Pickup Location", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker([dropoff_coordinates[1], dropoff_coordinates[0]], tooltip="Dropoff Location", icon=folium.Icon(color="purple")).add_to(m)

    # Add shuttle starting position marker
    initial_shuttle_position = shuttle_positions[selected_shuttle]
    folium.Marker(
        [initial_shuttle_position["lat"], initial_shuttle_position["lon"]],
        tooltip=f"{selected_shuttle} Start Position",
        icon=folium.Icon(color="red", icon="bus", prefix="fa")
    ).add_to(m)

    # Draw the real route for the selected shuttle
    folium.PolyLine(
        [(coord[1], coord[0]) for coord in selected_route],
        color="blue", weight=4, opacity=0.7, tooltip="Shuttle Route"
    ).add_to(m)

    # Display the map in Streamlit
    folium_static(m)
else:
    st.write("No valid routes found for any shuttles.")
