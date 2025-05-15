import streamlit as st
import pandas as pd
<<<<<<< HEAD
import folium
from folium import plugins
from streamlit_folium import st_folium
import requests



def data_collection():
    odata_urls = [
        'https://survey.kuklpid.gov.np/v1/projects/20/forms/kukl_customer_survey_phase1.svc'
    ]
    submission_entity_set = 'Submissions'
    username = 'anupthatal2@gmail.com'
    password = 'Super@8848'
    session = requests.Session()
    session.auth = (username, password)
    
    all_dfs = []  # List to store DataFrames from each URL
    
    for odata_url in odata_urls:
        submission_url = f"{odata_url}/{submission_entity_set}"
        response = session.get(submission_url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data['value'])
            pd.set_option('display.max_columns', None)
            print(df)
            df['lat'] = df['b02'].apply(lambda x: x['coordinates'][1] if isinstance(x, dict) and 'coordinates' in x else None)
            df['lon'] = df['b02'].apply(lambda x: x['coordinates'][0] if isinstance(x, dict) and 'coordinates' in x else None)
            customer = []
            connection = []
            submittername = []
            reviewState = []
            for i in df['gb12_skip']:
                customer.append(i['gc01_skp1']['gc20']['c20'])
                connection.append(i['gc01_skp1']['gc20']['c22'])
            for i in df['__system']:
                submittername.append(i['submitterName'])
                reviewState.append(i['reviewState'])
            # for i in df['gb10-b10_package']:
            #     packages.append(i['b10_dni']['b10_dmi'])
            #     print(packages)
            df['ReviewState'] = reviewState
            df['SubmitterName'] = submittername
            df['gb12_skip-gc01_skp1-gc20-c20'] = customer
            df['gb12_skip-gc01_skp1-gc20-c22'] = connection
            df['SubmitterName'] = df['SubmitterName'].str.upper()
            df = df[['b10_dmi','ward_number','unique_form_id','lat','lon','gb12_skip-gc01_skp1-gc20-c20', 'gb12_skip-gc01_skp1-gc20-c22','SubmitterName', 'ReviewState', 'unit_owners']]
            all_dfs.append(df)  # Append the processed DataFrame
    final_df = pd.concat(all_dfs, ignore_index=True)
    return final_df

df = data_collection()


# Sidebar
with st.sidebar:
    
    location=df['ward_number'].unique().tolist()
    # location_area=st.selectbox('Select location',location)
    areas_list = df['b10_dmi'].dropna().unique().tolist()
    selected_area = st.selectbox('Select Area', areas_list)
    if selected_area:
        filtered_df = df[df['b10_dmi'] == selected_area]
        # filtered_df=df1[df1['Areas']==location_area]
        # P=filtered_df['Packages']
        SDMA=filtered_df['b10_dmi'].unique().tolist()[0]
        ward=filtered_df['ward_number'].unique().tolist()[0]
    
        # person=filtered_df['Person']
        # phone=filtered_df['Phone']
        sub_dmi_counts = filtered_df['b10_dmi'].value_counts()
        st.write(f"ward of that areas :blue[{ward}]")
        # st.write(f'Packages of :blue[{packages}]')
        st.write(f"ward of :blue[{SDMA}]")
        # st.write(f'Person responsible :blue[{person}]')
        # st.write(f'Phone number of that person :blue[{phone}]')
        st.write(sub_dmi_counts)

# Main content
col1, = st.columns(1)  # Note the use of comma to unpack the list

with col1:
    if selected_area:
        # Filter DataFrame for selected area
        selected_df = df[df['b10_dmi'] == selected_area]

        # Drop rows with NaN values in location coordinates
        selected_df = selected_df.dropna(subset=['lat', 'lon'])

        # Extract latitude and longitude lists
        lat = selected_df['lat'].astype(float).tolist()
        lon = selected_df['lon'].astype(float).tolist()

        # Calculate the center of the map
        center_lat = sum(lat) / len(lat) if len(lat) > 0 else 0
        center_lon = sum(lon) / len(lon) if len(lon) > 0 else 0

        # Create a Folium map centered at the mean of coordinates
        folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=16)

        # Add markers for each location with smaller icon
        for i in range(len(lat)):
            folium.Marker([lat[i], lon[i]], icon=folium.Icon(icon="circle", prefix='fa', icon_color='blue', icon_size=(2,2))).add_to(folium_map)

        # Display the Folium map using streamlit_folium
        st_folium(folium_map,width=1000, height=500)
=======
import requests
import plotly.express as px
from ipyleaflet import Map, Marker, Polyline, Polygon, LayersControl, basemaps, basemap_to_tiles
from ipywidgets import HTML
from branca.colormap import linear


# 1. Data Collection Function (Same as yours)

def data_collection():
    odata_urls = [
        'https://survey.kuklpid.gov.np/v1/projects/20/forms/kukl_customer_survey_phase1.svc',
        'https://survey.kuklpid.gov.np/v1/projects/20/forms/kukl_customer_survey_phase2.svc'
    ]
    params = {
        '$select': 'unique_form_id,b10_dmi,gb12_skip/gc01_skp1/gc20/c20,gb12_skip/gc01_skp1/gc20/c22,__system/submitterName,__system/reviewState,b02,unit_owners,gb12_skip/gc01_skp2/d08,__system/attachmentsPresent,__system/attachmentsExpected,meta/instanceName'
    }
    session = requests.Session()
    session.auth = ('anupthatal2@gmail.com', 'Super@8848')
    all_dfs = []

    for odata_url in odata_urls:
        submission_url = f"{odata_url}/Submissions"
        response = session.get(submission_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'value' in data:
                df = pd.DataFrame(data['value'])
                df['url'] = odata_url
                all_dfs.append(df)

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df['gb12_skip-gc01_skp1-gc20-c20'] = final_df['gb12_skip'].apply(lambda x: x.get('gc01_skp1', {}).get('gc20', {}).get('c20'))
    final_df['gb12_skip-gc01_skp1-gc20-c22'] = final_df['gb12_skip'].apply(lambda x: x.get('gc01_skp1', {}).get('gc20', {}).get('c22'))
    final_df['SubmitterName'] = final_df['__system'].apply(lambda x: x['submitterName'] if 'submitterName' in x else None).str.upper()
    final_df['ReviewState'] = final_df['__system'].apply(lambda x: x['reviewState'] if 'reviewState' in x else None)
    final_df['b02-Longitude'] = final_df['b02'].apply(lambda x: x['coordinates'][0] if (x and 'coordinates' in x) else None)
    final_df['b02-Latitude'] = final_df['b02'].apply(lambda x: x['coordinates'][1] if (x and 'coordinates' in x) else None)
    final_df['gb12_skip-gc01_skp2-d08'] = final_df['gb12_skip'].apply(lambda x: x.get('gc01_skp2', {}).get('d08'))
    final_df['AttachmentsPresent'] = final_df['__system'].apply(lambda x: x['attachmentsPresent'] if 'attachmentsPresent' in x else None)
    final_df['AttachmentsExpected'] = final_df['__system'].apply(lambda x: x['attachmentsExpected'] if 'attachmentsExpected' in x else None)
    final_df['InstanceName'] = final_df['meta'].apply(lambda x: x['instanceName'] if 'instanceName' in x else None)

    return final_df

# 2. Load Data
df = data_collection()

selected_area = st.sidebar.selectbox('Select DMA', df['b10_dmi'].dropna().unique().tolist())
filtered_df = df[df['b10_dmi'] == selected_area]
filtered_df = filtered_df.dropna(subset=['b02-Latitude', 'b02-Longitude'])
print(filtered_df)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 200px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 5. Generate Map using ipyleaflet
def display_ipyleaflet_map(data):
    basemap_options = {
    "Open Street Map": "open-street-map",
    "Carto Positron (Light)": "carto-positron",
    "Carto Darkmatter (Dark)": "carto-darkmatter",
    "Stamen Terrain": "stamen-terrain",
    "White Background": "white-bg"
}

    selected_basemap = st.sidebar.selectbox("Select Basemap Style", list(basemap_options.keys()))
    selected_style = basemap_options[selected_basemap]

    center_lat = data['b02-Latitude'].mean()
    center_lon = data['b02-Longitude'].mean()
    fig=px.scatter_mapbox(data,lat='b02-Latitude',size_max=20,lon='b02-Longitude',color='SubmitterName',zoom=11,height=500,hover_name='gb12_skip-gc01_skp1-gc20-c22',width=800)

    

    fig.update_layout(mapbox_style=selected_style,mapbox_center={"lat": center_lat, "lon": center_lon},dragmode='pan',margin={"r":0,"t":0,"l":0,"b":0},  legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(size=10)
    ))


    return fig,center_lat, center_lon

st.markdown("### Map View")
px_map, center_lat, center_lon = display_ipyleaflet_map(data=filtered_df)
st.plotly_chart(px_map,use_container_width=True)
st.markdown(f"**Map Center Coordinates:** Latitude: `{center_lat:.5f}`, Longitude: `{center_lon:.5f}`")
>>>>>>> a8daf38 (Initial commit of mapsenv)
