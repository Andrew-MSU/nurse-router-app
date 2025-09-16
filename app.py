import streamlit as st
import folium
from streamlit_folium import st_folium
import openrouteservice
from openrouteservice import convert
import pandas as pd  # Added for clean table display

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

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m" if hours else f"{minutes}m"

st.title('🏥 Hospice Nurse Routing Prototype')
st.markdown('Select a patient to auto-find the closest nurse and generate a driving route in Montana.')

# User input
selected_patient = st.selectbox('Select Patient', options=list(patients.keys()))

# Generate route on button click
if st.button('Find Closest Nurse and Generate Route'):
    patient_loc = patients[selected_patient]  # (lat, lon)
    results = []  # List for all nurses' data
    
    for nurse_name, nurse_loc in nurses.items():
        # ORS coords: ((start_lon, start_lat), (end_lon, end_lat))
        coords = ((nurse_loc[1], nurse_loc[0]), (patient_loc[1], patient_loc[0]))
        
        try:
            routes = client.directions(coords, profile='driving-car')
            summary = routes['routes'][0]['summary']
            dist_meters = summary['distance']
            duration_sec = summary['duration']
            
            dist_miles = dist_meters / 1609.34  # meters to miles
            time_str = format_time(duration_sec)
            
            results.append({
                'Nurse': nurse_name,
                'Distance (miles)': round(dist_miles, 1),
                'Drive Time': time_str,
                'routes': routes  # Save for map if selected
            })
        except Exception as e:
            st.error(f"Error calculating route for {nurse_name}: {str(e)}")
            continue
    
    if results:
        # Sort by distance
        results_sorted = sorted(results, key=lambda x: x['Distance (miles)'])
        
        # Closest for map
        closest = results_sorted[0]
        routes = closest['routes']
        geometry = routes['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)['coordinates']  # [lon, lat]
        polyline_points = [[point[1], point[0]] for point in decoded]  # [lat, lon]
        
        # Create map
        m = folium.Map(location=[46.0, -110.0], zoom_start=6)
        
        # Add markers
        nurse_loc = nurses[closest['Nurse']]
        folium.Marker(
            nurse_loc, 
            popup=f"{closest['Nurse']} (Starting Point)", 
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
        
        # Display closest info
        st.metric(label="Closest Nurse", value=closest['Nurse'])
        st.metric(label="Driving Distance", value=f"{closest['Distance (miles)']} miles")
        st.metric(label="Estimated Drive Time", value=closest['Drive Time'])
        
        # Show ranked options table (only name, distance, time)
        st.subheader("Ranked Nurse Options")
        df = pd.DataFrame(results_sorted)
        df = df[['Nurse', 'Distance (miles)', 'Drive Time']]  # Select only desired columns
        st.table(df)
    else:
        st.error("No routes could be calculated. Check API key or locations.")