import streamlit as st
from decouple import config
import requests
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(page_icon='🗡', page_title='Streamlit Paywall Example', layout="wide")

# Main title for the app
st.title("🎈 Streamlit App with Paywall 🎈")

# Button for signing up
if st.button("Sign Up Now 🤘🏻"):
    st.write(f"Please visit the following link to sign up: {config('STRIPE_CHECKOUT_LINK')}")

st.markdown('### Already have an Account? Login Below👇🏻')
with st.form("login_form"):
    st.write("Login")
    email = st.text_input('Enter Your Email')
    password = st.text_input('Enter Your Password', type='password')
    submitted = st.form_submit_button("Login")

if submitted:
    if password == config('SECRET_PASSWORD'):
        st.session_state['logged_in'] = True
        st.success('Successfully Logged In!')
    else:
        st.error('Incorrect login credentials.')
        st.session_state['logged_in'] = False

# Check if logged in before displaying the rest of the app
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    # Divider
    st.markdown("---")

    # Title for the NFIP data search functionality
    st.subheader("Search NFIP Multiple Loss Properties")

 # Define the data dictionary before its usage
data_dictionary = {
    'psCountyCode': {'description': 'FIPS County Code', 'required': True, 'type': 'text'},
    'state': {'description': 'State', 'required': True, 'type': 'text'},
    'stateAbbreviation': {'description': 'State Abbreviation', 'required': True, 'type': 'text'},
    'county': {'description': 'County', 'required': True, 'type': 'text'},
    'zipCode': {'description': 'Zip Code', 'required': True, 'type': 'text'},
    'reportedCity': {'description': 'Reported City', 'required': True, 'type': 'text'},
    'communityIdNumber': {'description': 'NFIP Community ID Number', 'required': True, 'type': 'text'},
    'communityName': {'description': 'NFIP Community Name', 'required': True, 'type': 'text'},
    'censusBlockGroup': {'description': 'Census Block Group FIPS', 'required': True, 'type': 'text'},
    'nfipRl': {'description': 'NFIP RL', 'required': True, 'type': 'boolean'},
    'nfipSrl': {'description': 'NFIP SRL', 'required': True, 'type': 'boolean'},
    'fmaRl': {'description': 'FMA RL', 'required': True, 'type': 'boolean'},
    'fmaSrl': {'description': 'FMA SRL', 'required': True, 'type': 'boolean'},
    'asOfDate': {'description': 'As of Date', 'required': True, 'type': 'date'},
    'floodZone': {'description': 'Flood Zone', 'required': True, 'type': 'text'},
    'latitude': {'description': 'Latitude', 'required': True, 'type': 'decimal'},
    'longitude': {'description': 'Longitude', 'required': True, 'type': 'decimal'},
    'occupancyType': {'description': 'Occupancy Type', 'required': True, 'type': 'smallint'},
    'originalConstructionDate': {'description': 'Original Construction Date', 'required': True, 'type': 'date'},
    'originalNBDate': {'description': 'Original NB Date', 'required': True, 'type': 'date'},
    'postFIRMConstructionIndicator': {'description': 'Post FIRM Construction Indicator', 'required': True, 'type': 'boolean'},
    'primaryResidenceIndicator': {'description': 'Primary Residence Indicator', 'required': True, 'type': 'boolean'},
    'mitigatedIndicator': {'description': 'Mitigated Indicator', 'required': True, 'type': 'boolean'},
    'insuredIndicator': {'description': 'Insured Indicator', 'required': True, 'type': 'boolean'},
    'totalLosses': {'description': 'Total Losses', 'required': True, 'type': 'smallint'},
    'mostRecentDateofLoss': {'description': 'Most Recent Date of Loss', 'required': True, 'type': 'date'},
    'id': {'description': 'ID', 'required': True, 'type': 'uuid'}
}

# Convert data dictionary to options for the dropdown
column_options = [{'label': v['description'], 'value': k} for k, v in data_dictionary.items()]

# Streamlit layout
st.title("Search NFIP Multiple Loss Properties")
zip_code = st.text_input('Enter zip code', key='zip_code_input')
selected_columns = st.multiselect('Select columns to display', options=[option['value'] for option in column_options], format_func=lambda x: data_dictionary[x]['description'])

if st.button('Search NFIP Data'):
    if zip_code and selected_columns:
        params = {'zipCode': zip_code, '$allrecords': 'true'}
        response = requests.get('https://www.fema.gov/api/open/v1/NfipMultipleLossProperties', params=params)
        if response.status_code == 200:
            data = response.json().get('NfipMultipleLossProperties', [])
            if data:
                table_data = pd.DataFrame(data)[selected_columns]
                st.dataframe(table_data)
                
                # Allow graph generation if more than one column is selected
                if len(selected_columns) > 1:
                    st.button('Show Graph', key='show_graph_button')

                    if st.session_state.get('show_graph'):
                        fig = px.bar(table_data, x=selected_columns[0], y=selected_columns[1:])
                        st.plotly_chart(fig)
            else:
                st.error("No results found for the specified zip code.")
        else:
            st.error("Failed to fetch data from API.")
    else:
        st.warning("Please enter a zip code and select at least one column.")
else:
    st.info('Please log in or sign up to access the app.')

if 'logged_in' in st.session_state.keys():
    if st.session_state['logged_in']:
        st.markdown('## Ask Me Anything')
        question = st.text_input('Ask your question')
        if question != '':
            st.write('I drink and I know things.')
