import streamlit as st 
from streamlitV1 import load_all_models, predict_demand
from datetime import datetime
import pandas as pd

def run():
    st.title("Products")
    st.subheader("Products - Pickup Demand Forecasting")

    # Define available products
    products = {
        "Forecasting Demand Pickups": "forecast_demand_pickups"
    }

    # Select the product
    selected_product = st.selectbox("Select a Product", list(products.keys()))

    # If the selected product is "Forecasting Demand Pickups", show the related functionality
    if selected_product == "Forecasting Demand Pickups":
        # List of Pickup IDs (replace with actual Pickup IDs)
        pickup_ids = [0, 8, 19, 30, 31]

        # Load all models
        with st.spinner('Loading models...'):
            models = load_all_models(pickup_ids)
        st.success("Models loaded.")

        # User input: Select Pickup ID
        pickup_id = st.selectbox("Select Pickup ID", pickup_ids)

        # User input: Date and Time
        forecast_date = st.date_input("Select Date", value=datetime.today())
        forecast_hour = st.slider("Select Hour", min_value=0, max_value=23, step=1)
        forecast_datetime = datetime.combine(forecast_date, datetime.min.time()) + pd.Timedelta(hours=forecast_hour)

        st.write(f"Forecasting for Pickup ID {pickup_id} on {forecast_datetime.strftime('%Y-%m-%d %H:%M')}")

        # Make prediction
        if st.button("Get Prediction"):
            if pickup_id in models:
                model = models[pickup_id]
                demand = predict_demand(model, forecast_datetime)
                st.success(f"Predicted demand for Pickup ID {pickup_id} at {forecast_datetime.strftime('%Y-%m-%d %H:%M')} is {demand} bookings.")
            else:
                st.error(f"Model for Pickup ID {pickup_id} is not available.")