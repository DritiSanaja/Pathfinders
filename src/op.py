import openrouteservice
import folium
import os
from dotenv import load_dotenv


load_dotenv()


ors_client = openrouteservice.Client(key=os.getenv('ORS_API_KEY'))  

# coordinates for pickup and drop-off (longitude, latitude)
pickup_point = (48.994215, 11.461103)  # Pickup coordinates (longitude, latitude)
dropoff_point = (49.033525, 11.475793)  # Drop-off coordinates (longitude, latitude)

# Define a larger polygon area to force route avoidance (coordinates are specified in longitude, latitude order)
expanded_avoidance_area = {
    "type": "Polygon",
    "coordinates": [[
        [11.450000, 49.000000],
        [11.470000, 49.000000],
        [11.470000, 49.030000],
        [11.450000, 49.030000],
        [11.450000, 49.000000]
    ]]
}

# Request route with expanded avoidance area
try:
    route_with_avoidance = ors_client.directions(
        coordinates=[pickup_point, dropoff_point],
        profile='driving-car',
        format='geojson',
        options={"avoid_polygons": expanded_avoidance_area}  
    )
    
    # Extract route coordinates for plotting
    route_coords_with_avoidance = [(coord[1], coord[0]) for coord in route_with_avoidance['features'][0]['geometry']['coordinates']]

    # Init map centered around the pickup point for the avoided route
    m_avoidance = folium.Map(location=[pickup_point[0], pickup_point[1]], zoom_start=13)

    # Add avoided route to the map
    folium.PolyLine(route_coords_with_avoidance, color="red", weight=2.5, opacity=0.7).add_to(m_avoidance)

    # Add markers for pickup and drop-off points
    folium.Marker(
        location=[pickup_point[0], pickup_point[1]],  # Note the coordinate order (latitude, longitude)
        popup="Pickup",
        icon=folium.Icon(color="blue")
    ).add_to(m_avoidance)

    folium.Marker(
        location=[dropoff_point[0], dropoff_point[1]],  # Note the coordinate order (latitude, longitude)
        popup="Drop-off",
        icon=folium.Icon(color="green")
    ).add_to(m_avoidance)

    # Save and display the avoidance map
    m_avoidance.save("vgi_flexi_route_with_expanded_avoidance.html")
    print("Route with expanded avoidance created successfully. Saved as 'vgi_flexi_route_with_expanded_avoidance.html'.")

except Exception as e:
    print(f"Error fetching route with expanded avoidance: {e}")
