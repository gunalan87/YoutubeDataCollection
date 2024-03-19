import streamlit as st
import requests
import pandas as pd
import numpy as np
from mongodbdetails import mongodbdetails
from mysqldbconnect import mysqldbconnect
from pprint import pprint
#=============SETTINGS Started==========#
page_title = "List of Youtube Channels"
layout = "wide" # centered, wide
page_icon = ":sunrise_over_mountains:" # Reference : https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
initial_sidebar_state = "collapsed" #collapsed, expanded, auto
#=============SETTINGS Ended==========#
st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout,initial_sidebar_state=initial_sidebar_state)
st.title("Channel List")
mdbi = mongodbdetails() # Mongo DB Instance
acd = mdbi.get_all_channel_names() # All Channel Data
#st.dataframe(cdf.T,use_container_width=True)
with st.form(key="add_ytc_sql",clear_on_submit=True,border=True):
    selected_channel = st.selectbox("Filter by Channel :",acd)
    submitted = st.form_submit_button("Submit",type="primary")

if submitted:
    channel_result = mdbi.get_channel_data(selected_channel)
    sqldbobj = mysqldbconnect()
    sqldbobj.add_channel_details(channel_result)
    st.success("Channel details added to Dataware House")

