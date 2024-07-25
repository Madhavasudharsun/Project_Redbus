import streamlit as st
import pandas as pd
import pymysql

# Function to connect to the MySQL database
def create_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='Ammulu@7',
                           database='REDBUS')

# Function to fetch data from MySQL using a query
def fetch_data(query):
    connection = create_connection()
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(data, columns=columns)
    connection.close()
    return df

# Streamlit app title
st.title("Bus Routes Data")

# Filter data section
st.sidebar.subheader("Filter Data")

# Connect to database and fetch initial data
query_all = "SELECT * FROM bus_routes"
data = fetch_data(query_all)
df = pd.DataFrame(data)

# Display the fetched data
st.write("## All Bus Routes")
st.write(df)

# Initialize the filtered query
filtered_query = "SELECT * FROM bus_routes WHERE 1=1"

# Filter by State
selected_state = st.sidebar.selectbox("Select State", sorted(df['state'].unique()))
if selected_state:
    filtered_query += f" AND state = '{selected_state}'"

# Filter by Route Name based on selected state
if selected_state:
    selected_route = st.sidebar.selectbox("Select Route Name", sorted(df[df['state'] == selected_state]['route_name'].unique()))
    if selected_route:
        filtered_query += f" AND route_name = '{selected_route}'"

# Filter by Seating Type (Seater, Semi Sleeper, Sleeper, All)
seating_options = ['All', 'Seater', 'Semi Sleeper', 'Sleeper']
selected_seating = st.sidebar.selectbox("Select Seating Type", seating_options)
if selected_seating != 'All':
    filtered_query += f" AND bus_type LIKE '%{selected_seating}%'"

# Filter by Price Range
min_price, max_price = st.sidebar.slider("Select Price Range", min_value=0, max_value=5000, value=(0, 5000))
filtered_query += f" AND price BETWEEN {min_price} AND {max_price}"

# Filter by Seat Availability (Available, Almost Full)
seats_available = ['All', 'Available', 'Almost Full']
selected_seat_availability = st.sidebar.selectbox("Select Seat Availability", seats_available)
if selected_seat_availability != 'All':
    if selected_seat_availability == 'Available':
        filtered_query += " AND seats_available > 10"
    elif selected_seat_availability == 'Almost Full':
        filtered_query += " AND seats_available <= 10"

# Filter by Star Rating
min_star_rating = st.sidebar.slider("Select Minimum Star Rating", min_value=0.0, max_value=5.0, step=0.1, value=0.0)
if min_star_rating > 0.0:
    filtered_query += f" AND star_rating >= {min_star_rating}"

# Fetch filtered data
data = fetch_data(filtered_query)
filtered_df = pd.DataFrame(data)

# Display final filtered results
st.write("## Filtered Bus Routes")
st.write(filtered_df)
