from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import sum, col
import json
import altair as alt
import streamlit as st
st.set_page_config(
     page_title="Environment Data Atlas",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Snowflake Data Marketplace and Streamlit"
     }
)

def create_session():
    if "snowpark_session" not in st.session_state:
        connection_parameters = json.load(open('../connection.json'))
        connection_parameters['database'] = 'ENVIRONMENT_DATA_ATLAS'
        connection_parameters['schema'] = 'ENVIRONMENT'
        session = Session.builder.configs(connection_parameters).create()
        st.session_state['snowpark_session'] = session
    else:
        session = st.session_state['snowpark_session']

    return session

@st.experimental_memo()
def load_data():
    # CO2 Emissions
    snow_df_co2 = session.table("EDGARED2019").filter(col('Indicator Name') == 'Fossil CO2 Emissions').filter(col('Type Name') == 'All Type').sort('"Date"')

    # Forest Occupied Land Area by Country
    snow_df_land = session.table("\"WBWDI2019Jan\"").filter(col('Series Name') == 'Forest area (% of land area)')
    snow_df_land = snow_df_land.group_by('Country Name').agg(sum('$61').alias("Total Share of Forest Land")).sort('Country Name')

    return snow_df_co2.to_pandas(), snow_df_land.to_pandas()

# Add header and a sidebar
st.markdown("<h1 style='margin-top:-80px;'>Knoema: Environment Data Atlas</h1>", unsafe_allow_html=True)
session = create_session()
df_co2_overtime, df_forest_land = load_data()

def main_page():
    st.markdown("### CO2 Emissions By Countries")

    countries = ['United States','China','Russia','India','United Kingdom','Germany','Japan','Canada']
    selected_countries = st.multiselect('',countries, default = countries)
    st.write("")
    st.markdown("___")

    # Display an interactive chart to visualize CO2 Emissions over time by Country
    with st.container():
        st.subheader('CO2 Emissions by Countries Over Time')
        countries_list = countries if len(selected_countries) == 0 else selected_countries
        df_co2_overtime_filtered = df_co2_overtime[df_co2_overtime['Location Name'].isin(countries_list)]
        line_chart = alt.Chart(df_co2_overtime_filtered).mark_line(
            color="lightblue",
            line=True,
            point=alt.OverlayMarkDef(color="red")
        ).encode(
            x='Date',
            y='Value',
            color='Location Name',
            tooltip=['Location Name','Date','Value']
        )
        st.altair_chart(line_chart, use_container_width=True)

def page2():
    st.markdown("### Forest Occupied Land")

    threshold = st.slider(label='Forest Occupied Land By Countries',min_value=1000, max_value=2500, value=1800, step=200)
    st.write("")
    st.markdown("___")

    # Display an interactive chart to visualize Forest Occupied Land Area by Countries
    with st.container():
        st.subheader('Forest Occupied Land Area by Countries')
        filter = df_forest_land['Total Share of Forest Land'] > threshold
        pd_df_land_top_n = df_forest_land.where(filter)
        st.bar_chart(data=pd_df_land_top_n.set_index('Country Name'), width=850, height=400, use_container_width=True) 

page_names_to_funcs = {
    "CO2 Emissions": main_page,
    "Forest Occupied Land": page2
}

selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
