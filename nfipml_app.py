import streamlit as st
from decouple import config
import requests
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(page_icon='🗡', page_title='Streamlit Paywall Example', layout="wide")

# Main title for the app
st.title("🎈 Integrated Streamlit App 🎈")

# Section for interactive chat
st.markdown('## Chat with Tyrion Lannister ⚔️')
col1 = st.columns(1)
with col1:
    st.markdown(
        """
        Chat with Tyrion Lannister to advise you on:
        - Office Politics
        - War Strategy
        - The Targaryens

         #### [Sign Up Now 🤘🏻]({config('STRIPE_CHECKOUT_LINK')})
        """
    )

st.markdown('### Already have an Account? Login Below👇🏻')
with st.form("login_form"):
    st.write("Login")
    email = st.text_input('Enter Your Email')
    password = st.text_input('Enter Your Password', type='password')
    submitted = st.form_submit_button("Login")

if submitted:
    if password == config('SECRET_PASSWORD'):
        st.session_state['logged_in'] = True
        st.success('Succesfully Logged In!')
    else:
        st.error('Incorrect login credentials.')
        st.session_state['logged_in'] = False

if 'logged_in' in st.session_state.keys():
    if st.session_state['logged_in']:
        st.markdown('## Ask Me Anything')
        question = st.text_input('Ask your question')
        if question != '':
            st.write('I drink and I know things.')

# Divider
st.markdown("---")

# Title for the NFIP data search functionality
st.subheader("Search NFIP Multiple Loss Properties")

# Data dictionary and options for dropdown
data_dictionary = {
    'psCountyCode': {'description': 'FIPS County Code', 'required': True, 'type': 'text'},
    'state': {'description': 'State', 'required': True, 'type': 'text'},
    # Add more items as needed
}

column_options = {k: v['description'] for k, v in data_dictionary.items()}

zip_code = st.text_input('Enter zip code')
selected_columns = st.multiselect('Select columns to display', options=list(column_options.keys()), format_func=lambda x: column_options[x])

if st.button('Search NFIP Data'):
    if zip_code and selected_columns:
        params = {'zipCode': zip_code, '$allrecords': 'true'}
        response = requests.get('https://www.fema.gov/api/open/v1/NfipMultipleLossProperties', params=params)
        if response.status_code == 200:
            data = response.json().get('NfipMultipleLossProperties', [])
            if data:
                table_data = pd.DataFrame(data)[selected_columns]
                st.dataframe(table_data)
                
                # Plotting if more than one column is selected for a better comparison
                if len(selected_columns) > 1:
                    fig = px.bar(table_data, x=selected_columns[0], y=selected_columns[1:])
                    st.plotly_chart(fig)
            else:
                st.error("No results found for the specified zip code.")
        else:
            st.error("Failed to fetch data from API.")
    else:
        st.warning("Please enter a zip code and select at least one column.")
