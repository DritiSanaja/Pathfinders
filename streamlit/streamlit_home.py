import streamlit as st 

def run():
    # st.title("Willkomen auf unserer Seite zur Pathfinder APP")
    st.subheader("Pickup Demand Forecasting VGI-FLEXI App! 🎉")
    # Introduction
    st.write("""
    This app uses machine learning to forecast the demand for public transportation pickups in Ingolstadt. 
    It helps in predicting the number of bookings for a specific pickup location at a given time. 
    With this tool, you can optimize resources and better manage transportation demand.
    """)
    # Instructions
    st.write("""
    Here's how to use the app:
    1. Go to the **Products** section to start making predictions. You can select a pickup location, set the date and time, and the app will predict the demand for that location.
    2. Check the **About Us** section to learn more about the app and the team behind it.
    """)