import streamlit as st
import folium
import json
from streamlit_folium import st_folium
from folium.plugins import Draw

# Streamlit App Title
st.title("Draw green zone polygons!")

# Create a map where users can freely scroll and zoom
m = folium.Map(location=[45.0, -93.0], zoom_start=5)

# Add Draw Tool (Users can draw multiple polygons)
draw = Draw(
    draw_options={
        "polyline": False,
        "rectangle": False,
        "circle": False,
        "marker": False,
        "circlemarker": False,
        "polygon": {"shapeOptions": {"color": "green"}},  # Allow polygon drawing
    },
    edit_options={"edit": True, "remove": True},  # Enable edit & remove
)
draw.add_to(m)

# Display the Map in Streamlit
map_data = st_folium(m, width=1050, height=1150)

# Store drawn polygons
if "polygon_data" not in st.session_state:
    st.session_state["polygon_data"] = []

# Extract polygon coordinates if available
if map_data and map_data.get("all_drawings"):
    polygons = []
    for i, feature in enumerate(map_data["all_drawings"]):
        if feature["geometry"]["type"] == "Polygon":
            polygon_name = f"Polygon {i+1}"
            polygons.append({"name": polygon_name, "coordinates": feature["geometry"]["coordinates"][0]})

    st.session_state["polygon_data"] = polygons

st.write("")  # Adds some spacing
st.write("### Click below when you finish drawing:")

if st.button("Finish Drawing & Save"):
    if st.session_state["polygon_data"]:
        # Prepare JSON data
        final_data = []
        for i, poly in enumerate(st.session_state["polygon_data"]):
            poly_name = f"Polygon {i + 1}"
            final_data.append({"name": poly_name, "coordinates": poly["coordinates"]})

        # Convert to JSON string
        json_data = json.dumps(final_data, indent=4)

        # Allow user to download the file
        st.download_button(
            label="Download JSON File",
            data=json_data,
            file_name="polygon_coordinates.json",
            mime="application/json"
        )
    else:
        st.warning("No polygons drawn yet!")


