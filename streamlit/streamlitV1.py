import streamlit as st
import pandas as pd
import joblib
from prophet import Prophet
from datetime import datetime
from streamlit_navigation_bar import st_navbar
import streamlit_home 
import streamlit_products
import streamlit_about


# Function to load all pre-trained models
def load_all_models(pickup_ids):
    models = {}
    for pickup_id in pickup_ids:
        model_filename = f"prophet_model_pickup_{pickup_id}.pkl"
        try:
            models[pickup_id] = joblib.load(model_filename)
        except FileNotFoundError:
            st.write(f"Model for Pickup ID {pickup_id} not found.")
    return models

# Function to predict demand using a selected model
def predict_demand(model, forecast_time):
    future = pd.DataFrame({'ds': [forecast_time]})
    future['Weekday'] = future['ds'].dt.dayofweek
    forecast = model.predict(future)
    predicted_demand = forecast['yhat'].values[0]
    return int(round(predicted_demand))

# Top Navigation Bar using columns
# st.title("📈 VGI-FLEXI in Rural Areas")

# Create the top navigation bar
# page = st_navbar(["Home", "Products", "About Us"])
page = st.radio("", ["Home", "Products", "About Us"], horizontal=True)
st.write(page)

if page == "Home":
    streamlit_home.run()
if page == "Products":
    streamlit_products.run()
if page == "About Us":
    streamlit_about.run()

# col1, col2, col3 = st.columns(3)
# with col1:
#     if st.button("Home"):
#         page = "Home"
# with col2:
#     if st.button("Products"):
#         page = "Products"
# with col3:
#     if st.button("About Us"):
#         page = "About Us"

# Set default page
# if 'page' not in st.session_state:
#     st.session_state.page = "Home"

# # Update page state based on button click
# if 'page' in locals():
#     st.session_state.page = page


# if st.session_state.page == "Home":
#     st.subheader("Pickup Demand Forecasting VGI-FLEXI App! 🎉")
#     # Introduction
#     st.write("""
#     This app uses machine learning to forecast the demand for public transportation pickups in Ingolstadt. 
#     It helps in predicting the number of bookings for a specific pickup location at a given time. 
#     With this tool, you can optimize resources and better manage transportation demand.
#     """)
#     # Instructions
#     st.write("""
#     Here's how to use the app:
#     1. Go to the **Products** section to start making predictions. You can select a pickup location, set the date and time, and the app will predict the demand for that location.
#     2. Check the **About Us** section to learn more about the app and the team behind it.
#     """)

# Page: Products
# elif st.session_state.page == "Products":
#     st.subheader("Products - Pickup Demand Forecasting")

    # Define available products
#     products = {
#         "Forecasting Demand Pickups": "forecast_demand_pickups"
#     }

#     # Select the product
#     selected_product = st.selectbox("Select a Product", list(products.keys()))

#     # If the selected product is "Forecasting Demand Pickups", show the related functionality
#     if selected_product == "Forecasting Demand Pickups":
#         # List of Pickup IDs (replace with actual Pickup IDs)
#         pickup_ids = [0, 8, 19, 30, 31]

#         # Load all models
#         with st.spinner('Loading models...'):
#             models = load_all_models(pickup_ids)
#         st.success("Models loaded.")

#         # User input: Select Pickup ID
#         pickup_id = st.selectbox("Select Pickup ID", pickup_ids)

#         # User input: Date and Time
#         forecast_date = st.date_input("Select Date", value=datetime.today())
#         forecast_hour = st.slider("Select Hour", min_value=0, max_value=23, step=1)
#         forecast_datetime = datetime.combine(forecast_date, datetime.min.time()) + pd.Timedelta(hours=forecast_hour)

#         st.write(f"Forecasting for Pickup ID {pickup_id} on {forecast_datetime.strftime('%Y-%m-%d %H:%M')}")

#         # Make prediction
#         if st.button("Get Prediction"):
#             if pickup_id in models:
#                 model = models[pickup_id]
#                 demand = predict_demand(model, forecast_datetime)
#                 st.success(f"Predicted demand for Pickup ID {pickup_id} at {forecast_datetime.strftime('%Y-%m-%d %H:%M')} is {demand} bookings.")
#             else:
#                 st.error(f"Model for Pickup ID {pickup_id} is not available.")

# # Page: About Us
# elif st.session_state.page == "About Us":
#     st.subheader("About Us")
#     st.write("""
#     This app was developed to assist in demand forecasting for public transportation pickups.
#     It uses machine learning to predict future booking demand based on historical data, allowing for improved resource allocation.
    
#     For more information, contact us at: support@example.com.
#     """)
