import streamlit as st
import folium
from streamlit_folium import st_folium
import openrouteservice
from openrouteservice import convert

# Placeholder data for Montana (lat, long)
nurses = {
    'Alice (Billings)': (45.783, -108.501),
    'Bob (Missoula)': (46.872, -113.994),
    'Carol (Helena)': (46.589, -112.039)
}

patients = {
    'David (Great Falls)': (47.506, -111.300),
    'Eve (Bozeman)': (45.677, -111.043),
    'Frank (Butte)': (46.004, -112.535)
}

# ORS Client (uses secret API key)
client = openrouteservice.Client(key=st.secrets["ORS_API_KEY"])

st.title('🏥 Hospice Nurse Routing Prototype')
st.markdown('Select a patient to auto-find the closest nurse and generate a driving route in Montana.')

# User input
selected_patient = st.selectbox('Select Patient', options=list(patients.keys()))

# Generate route on button click
if st.button('Find Closest Nurse and Generate Route'):
    patient_loc = patients[selected_patient]  # (lat, lon)
    distances = {}
    routes_dict = {}  # To store routes for each nurse if needed
    
    for nurse_name, nurse_loc in nurses.items():
        # ORS coords: ((start_lon, start_lat), (end_lon, end_lat))
        coords = ((nurse_loc[1], nurse_loc[0]), (patient_loc[1], patient_loc[0]))
        
        try:
            routes = client.directions(coords, profile='driving-car')
            dist = routes['routes'][0]['summary']['distance'] / 1000  # meters to km
            distances[nurse_name] = dist
            routes_dict[nurse_name] = routes  # Save for later use
        except Exception as e:
            st.error(f"Error calculating route for {nurse_name}: {str(e)}")
            continue
    
    if distances:
        # Find closest
        closest_nurse = min(distances, key=distances.get)
        closest_dist = distances[closest_nurse]
        
        # Get route details for closest
        routes = routes_dict[closest_nurse]
        geometry = routes['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)['coordinates']  # list of [lon, lat]
        polyline_points = [[point[1], point[0]] for point in decoded]  # Swap to [lat, lon] for Folium
        
        # Create map
        m = folium.Map(location=[46.0, -110.0], zoom_start=6)
        
        # Add markers
        nurse_loc = nurses[closest_nurse]
        folium.Marker(
            nurse_loc, 
            popup=f'{closest_nurse} (Starting Point)', 
            tooltip='Nurse Location',
            icon=folium.Icon(color='green')
        ).add_to(m)
        
        folium.Marker(
            patient_loc, 
            popup=f'{selected_patient} (Destination)', 
            tooltip='Patient Location',
            icon=folium.Icon(color='red')
        ).add_to(m)
        
        # Add driving route
        folium.PolyLine(
            polyline_points, 
            color='blue', 
            weight=2.5, 
            opacity=1,
            popup='Driving Route to Patient'
        ).add_to(m)
        
        # Fit map to route bounds
        m.fit_bounds(m.get_bounds())
        
        # Display map
        st_folium(m, width=700, height=500, returned_objects=[], key="route_map")
        
        # Display info
        st.metric(label="Closest Nurse", value=closest_nurse)
        st.metric(label="Driving Distance", value=f"{closest_dist:.1f} km")
    else:
        st.error("No routes could be calculated. Check API key or locations.")