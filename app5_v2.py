import streamlit as st
from streamlit_gsheets import GSheetsConnection
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime
import pandas as pd

# Initialize connection
conn = st.connection("gsheets", type=GSheetsConnection)
st.image("volt.png", width=200)
st.title("Book a Volt Taxi")

with st.form("booking_form", clear_on_submit=False):
    try:
        location = streamlit_geolocation()
        lat = location["latitude"]
        lng = location["longitude"]
        acc = location['accuracy']
        
        st.subheader("Pickup Location")
        pickup = st.text_input("Coordinates", value=f"{lat} - {lng}")
        pickup_details = st.text_area('Location Details', 
                                    placeholder="Ex: Near the mosque",
                                    help="Add landmarks or other helpful details")
        
        m = folium.Map(location=[lat, lng], zoom_start=13)
        folium.Marker([lat, lng], popup="Your Location").add_to(m)    
        st_folium(m, width=700, height=200)
        
        st.subheader("Destination")
        dropoff = st.text_input("Drop-off Location")

    except Exception as e:
        st.error("Unable to get location. Please enable location services.")
        print(f"Localization error: {e}")

    if st.form_submit_button("Book Now"):
        booking_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'pickup_coords': pickup,
            'pickup_details': pickup_details,
            'dropoff': dropoff,
            'accuracy': acc
        }
        new_booking_df = pd.DataFrame(booking_data,index=[1]) 
        #st.write(new_booking_df)
        try:
            # Update Google Sheet
            #df = conn.read(spreadsheet='bookings',worksheet='Sheet1')
            #st.write(df)
            #f2 = pd.concat([df, new_booking_df], ignore_index=True) 
            #st.dataframe(df2)
            conn.update(data=new_booking_df)
            st.success("Booking sent! A taxi :taxi: will arrive soon :smile:")
        except Exception as e:
            st.error(f"Failed to save booking: {str(e)}")