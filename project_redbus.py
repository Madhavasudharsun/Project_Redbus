import streamlit as st
import pandas as pd
import pymysql

# Function to connect to the MySQL database
def create_connection():
    return pymysql.connect(host='127.0.0.1', user='root', passwd='Ammulu@7', database='REDBUS')

# Function to fetch data from the specified query
def fetch_data(query, params=None):
    connection = create_connection()
    if params is None:
        params = ()
    df = pd.read_sql(query, connection, params=params)
    connection.close()
    return df

# Streamlit app title
st.title("Bus Routes Data")

# Filter data section
st.sidebar.subheader("Filter Data")

# Connect to database and fetch initial data
query_all = "SELECT * FROM bus_routes"
df = fetch_data(query_all)

# Display the fetched data
st.write("## All Bus Routes")
st.write(df)

# Filter by State
selected_state = st.sidebar.selectbox("Select State", sorted(df['state'].unique()))
state_filtered_query = f"""
    SELECT * FROM bus_routes
    WHERE state = '{selected_state}'
"""
state_filtered_df = fetch_data(state_filtered_query)

# Filter by Route Name based on selected state
selected_route = st.sidebar.selectbox("Select Route Name", sorted(state_filtered_df['route_name'].unique()))
route_filtered_query = f"""
    SELECT * FROM bus_routes
    WHERE state = '{selected_state}'
    AND route_name = '{selected_route}'
"""
route_filtered_df = fetch_data(route_filtered_query)

# Filter by Star Rating based on selected route
min_star_rating = st.sidebar.slider("Select Minimum Star Rating", min_value=0.0, max_value=5.0, step=0.1, value=0.0)
star_rating_filtered_query = f"""
    SELECT * FROM bus_routes
    WHERE state = '{selected_state}'
    AND route_name = '{selected_route}'
    AND star_rating >= {min_star_rating}
"""
star_rating_filtered_df = fetch_data(star_rating_filtered_query)

# Show filtered results
st.write("## Filtered Bus Routes")
st.write(star_rating_filtered_df)
