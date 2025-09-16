import streamlit as st
import folium
from streamlit_folium import st_folium

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

st.title('🏥 Hospice Nurse Routing Prototype')
st.markdown('Select a patient and nurse to generate a route map for Montana.')

# User inputs
selected_patient = st.selectbox('Select Patient', options=list(patients.keys()))
selected_nurse = st.selectbox('Select Nurse', options=list(nurses.keys()))

# Generate map on button click
if st.button('Generate Route'):
    nurse_loc = nurses[selected_nurse]
    patient_loc = patients[selected_patient]
    
    # Center map on Montana
    m = folium.Map(location=[46.0, -110.0], zoom_start=6)
    
    # Add markers
    folium.Marker(
        nurse_loc, 
        popup=f'{selected_nurse} (Starting Point)', 
        tooltip='Nurse Location',
        icon=folium.Icon(color='green')
    ).add_to(m)
    
    folium.Marker(
        patient_loc, 
        popup=f'{selected_patient} (Destination)', 
        tooltip='Patient Location',
        icon=folium.Icon(color='red')
    ).add_to(m)
    
    # Simple straight-line route
    folium.PolyLine(
        [nurse_loc, patient_loc], 
        color='blue', 
        weight=2.5, 
        opacity=1,
        popup='Route to Patient'
    ).add_to(m)
    
    # Display map in Streamlit – ADD returned_objects=[] and key
    st_folium(m, width=700, height=500, returned_objects=[], key="route_map")
    
    # Optional: Distance estimate (using haversine formula)
    from math import radians, sin, cos, sqrt, atan2
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    distance_km = haversine(nurse_loc[0], nurse_loc[1], patient_loc[0], patient_loc[1])
    st.metric(label="Estimated Straight-Line Distance", value=f"{distance_km:.1f} km")