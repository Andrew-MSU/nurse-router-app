Hospice Nurse Routing Prototype
This is a simple web-based application built with Streamlit to help hospice care managers match patients to the closest available nurses in Montana. It uses placeholder data for patients and nurses, calculates driving distances and times via the OpenRouteService API, and displays interactive maps with routes using Folium.
The app is live at: https://nurse-router.streamlit.app/
Features

Patient Selection: Choose a patient from a dropdown list (with pre-defined locations in Montana).
Auto-Matching: Automatically finds the closest nurse based on driving distance.
Driving Routes: Generates real road-based routes, distances (in miles), and estimated drive times.
Ranked Options: Displays a table of all nurses ranked by distance, showing name, distance, and drive time.
Interactive Map: Visualizes the route from the closest nurse to the patient with markers and a polyline.
Placeholder Data: Fictional nurses and patients in Montana cities; easily extensible to real data.

Setup and Installation
Local Development

Clone the repository (or copy the app.py code provided).
Install dependencies:
textpip install -r requirements.txt
Where requirements.txt contains:
textstreamlit
folium
streamlit-folium
openrouteservice
pandas

Get an OpenRouteService API key:

Sign up at openrouteservice.org.
Create a .streamlit/secrets.toml file in your project root:
textORS_API_KEY = "your_api_key_here"



Run the app locally:
textstreamlit run app.py


Deployment on Streamlit Cloud

Push your code to a GitHub repository (include app.py and requirements.txt).
Sign in to Streamlit Community Cloud with GitHub.
Create a new app, link your repo, set the entrypoint to app.py.
Add your ORS API key in the app's Settings > Secrets.
Deploy—it auto-builds and provides a public URL.

Usage

Open the app in your browser (local: http://localhost:8501 or deployed URL).
Select a patient from the dropdown.
Click "Find Closest Nurse and Generate Route".
View the interactive map, closest nurse metrics, and ranked table below.

Code Overview
The core logic in app.py:

Uses dictionaries for placeholder nurse/patient locations.
Fetches routes via OpenRouteService API.
Sorts nurses by driving distance.
Renders map with Folium and displays data with Streamlit components.

For extensions:

Add real addresses with geocoding (e.g., via Nominatim).
Integrate nurse availability or scheduling.
Upload CSV for dynamic data.

Dependencies

Python 3.8+
Streamlit: Web app framework.
Folium: Interactive maps.
streamlit-folium: Streamlit integration for Folium.
openrouteservice: API client for routing.
Pandas: For clean table display.

Limitations

Free ORS API: Limited to ~2,000 requests/day—monitor usage.
Placeholder Data: Update with real coordinates for production.
Straightforward Routing: Assumes car travel; no traffic or optimizations yet.

Contributing
Feel free to fork and submit PRs for improvements, like adding more features or real data integration.
License
MIT License - Free to use and modify.