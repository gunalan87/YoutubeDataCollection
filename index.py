import os
import streamlit as st
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import googleapiclient.discovery
import googleapiclient.errors
import requests
from pprint import pprint
from pathlib import Path
from youtubedataapi import YoutubeDataApi
import pymongo
from mongodbdetails import mongodbdetails
from datetime import datetime
from streamlit_option_menu import option_menu
import toml

#=============SETTINGS Started==========#
page_title = "Youtube Data Harvesting using Python, Youtube Data API, MongoDB and MySQL"
layout = "wide" # centered, wide
page_icon = ":sunrise_over_mountains:" # Reference : https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
initial_sidebar_state = "collapsed" #collapsed, expanded, auto
#=============SETTINGS Ended==========#

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout,initial_sidebar_state=initial_sidebar_state)

st.title(page_title)
st.divider()#"---"

with st.form(key="get_ytc_url",clear_on_submit=True,border=True):
    uiytcid = st.text_input(label="Enter Youtube Channel ID",type="default",key="ytcid")
    submitted = st.form_submit_button("Submit",type="primary")

if submitted:
    ytcid = st.session_state['ytcid']
    if len(ytcid) == 0:
        st.error("Youtube Channel ID can't be empty")

    cd = YoutubeDataApi() # Channel Details
    ci = cd.channel_details(channel_id=ytcid) #channel info
    
    whole_dict = {'videos':{}}
    #========== Channel INFO Started==================
    channel_name = ci['items'][0]['snippet']['title']
    dt_object = datetime.fromisoformat(ci['items'][0]['snippet']['publishedAt'].replace('Z', '+00:00'))
    channel_publish_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    channel_id = ci['items'][0]['id']
    channel_video_count = ci['items'][0]['statistics']['videoCount']
    channel_subscriber_count = ci['items'][0]['statistics']['subscriberCount']
    #channel_hidden_subscriber_count = ci['items'][0]['statistics']['hiddenSubscriberCount']
    channel_view_count = ci['items'][0]['statistics']['viewCount']
    channel_description = ci['items'][0]['snippet']['description']
    channel_playlist_id = ci['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    #channel_default_thumbnail_url = ci['items'][0]['snippet']['thumbnails']['default']['url']
    channel_high_thumbnail_url = ci['items'][0]['snippet']['thumbnails']['high']['url']
    channel_status = ci['items'][0]['status']['privacyStatus']

    # Add Dictionary values for channel information
    whole_dict['channel_name'] = channel_name
    whole_dict['publish_time'] = channel_publish_time
    whole_dict['channel_id'] = channel_id
    whole_dict['video_count'] = channel_video_count
    whole_dict['subscriber_count'] = channel_subscriber_count
    whole_dict['total_views'] = channel_view_count
    whole_dict['description'] = channel_description
    whole_dict['playlist_id'] = channel_playlist_id
    whole_dict['thumbnail_url'] = channel_high_thumbnail_url
    whole_dict['status'] = channel_status

    #=== Get Video IDs of the channel starts here =====#
    video_ids = []
    next_page_token = None

    while True:
        pitems = cd.playlist_items(channel_playlist_id,next_page_token)

        for i in range(len(pitems['items'])):
            video_ids.append(pitems['items'][i]['contentDetails']['videoId'])
        next_page_token = pitems.get('nextPageToken')
        if next_page_token is None:
            break
    #=== Get Video IDs of the channel Ends here =====#
    #=== Get Details about each video of the channel starts here =====#
    total_videos = {}
    if len(video_ids)>0 :
        for i in video_ids:
            video_comment_list = cd.video_comment_details(i)
            total_videos[i] = video_comment_list
        whole_dict['videos'] = total_videos

    #=== Get Details about each video of the channel starts here =====#
    mongoobj = mongodbdetails() # Channel Details
    res = mongoobj.add_data(whole_dict)
    st.success("Channel Data saved successfully.")
    st.subheader("Channel Details")
    st.image(channel_high_thumbnail_url,width = 100)
    st.text("Channel Name : "+channel_name)
    st.text("Channel Publish Date : "+channel_publish_time)
    st.text("Total Videos : "+channel_video_count)
    st.text("Subscriber Count : "+channel_subscriber_count)
    st.text("Total View Count : "+channel_view_count)
    #========== Channel INFO Ended==================
st.divider()