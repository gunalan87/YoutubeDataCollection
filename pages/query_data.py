import streamlit as st
import mysql.connector
import os
import pandas as pd
from pprint import pprint
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
mysql_user = os.getenv("mysql_user")
mysql_password = os.getenv("mysql_password")
mysql_host = os.getenv("mysql_host")
mysql_database = os.getenv("mysql_database")

try:
    dbconnect = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
    dbcursor = dbconnect.cursor()
except mysql.connector.Error as err:
    st.write("Connection Error",err)


question_list = ["What are the names of all the videos and their corresponding channels?",
                 "Which channels have the most number of videos, and how many videos do they have?",
                 "What are the top 10 most viewed videos and their respective channels?",
                 "How many comments were made on each video, and what are their corresponding video names?",
                 "Which videos have the highest number of likes, and what are their corresponding channel names?",
                 "What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                 "What is the total number of views for each channel, and what are their corresponding channel names?",
                 "What are the names of all the channels that have published videos in the year 2022?",
                 "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                 "Which videos have the highest number of comments, and what are their corresponding channel names?"]

with st.form(key="query_sql",border=True):
    selected_channel = st.selectbox("Choose a Question :",question_list)
    submitted = st.form_submit_button("Submit",type="primary")


if submitted:
    
    selected_index = question_list.index(selected_channel)

    match selected_index:
        case 0:
            qry = "select video_name,videos.playlist_id,channel_name from videos inner join playlist on videos.playlist_id = playlist.id inner join channels on playlist.cid = channels.id"
            st.title("What are the names of all the videos and their corresponding channels?")
        case 1:
            qry = "select channel_name,count(videos.id) as total_videos from videos inner join playlist on videos.playlist_id = playlist.id inner join channels on playlist.id = channels.id group by videos.playlist_id order by total_videos desc limit 1;"
            st.title("Which channels have the most number of videos, and how many videos do they have?")
        case 2:
            qry = "select video_name, channel_name, view_count from videos inner join playlist on videos.playlist_id = playlist.id inner join channels on playlist.cid = channels.id order by view_count desc limit 10;"
            st.title("What are the top 10 most viewed videos and their respective channels?")
        case 3:
            qry = "select video_name,count(comments.video_id) as comment_count from comments inner join videos on comments.video_id = videos.id group by comments.video_id order by comment_count desc;"
            st.title("How many comments were made on each video, and what are their corresponding video names?")
        case 4:
            qry = "select video_name,like_count,channel_name from videos inner join playlist on videos.playlist_id = playlist.id inner join channels on playlist.cid = channels.id order by like_count desc limit 1;"
            st.title("Which videos have the highest number of likes, and what are their corresponding channel names?")
        case 5:
            qry = "select video_name, like_count from videos order by like_count desc;"
            st.title("What is the total number of likes and dislikes for each video, and what are their corresponding video names?")
        case 6:
            qry= "select channel_name,channel_view from channels;"
            st.title("What is the total number of views for each channel, and what are their corresponding channel names?")
        case 7:
            qry = "select distinct(channel_name),year(published_date) from videos inner join playlist on videos.playlist_id = playlist.id inner join channels on playlist.cid = channels.id where year(videos.published_date) = 2022;"
            st.title("What are the names of all the channels that have published videos in the year 2022?")
        case 8:
            qry = "select channel_name,round(avg(duration),2) as avg_video_time from videos inner join playlist on videos.playlist_id = playlist.id inner join channels on playlist.cid = channels.id group by videos.playlist_id;"
            st.title("What is the average duration of all videos in each channel, and what are their corresponding channel names?")
        case 9:
            qry = "select video_name,count(comments.id) as total_comments from videos inner join comments on videos.id = comments.video_id group by comments.video_id order by total_comments desc limit 5;"
            st.title("Which videos have the highest number of comments, and what are their corresponding channel names?")

    st.code(qry)
    dbcursor.execute(qry)
    qryres = dbcursor.fetchall()
    st.write(pd.DataFrame(qryres))