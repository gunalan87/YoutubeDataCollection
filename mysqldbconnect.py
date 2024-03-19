import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from pprint import pprint
class mysqldbconnect:
    def __init__(self):
        dotenv_path = Path('.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.mysql_user = os.getenv("mysql_user")
        self.mysql_password = os.getenv("mysql_password")
        self.mysql_host = os.getenv("mysql_host")
        self.mysql_database = os.getenv("mysql_database")
        try:
            # Reference URL : https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
            self._dbconn  = mysql.connector.connect(user = self.mysql_user,password = self.mysql_password,host = self.mysql_host,database = self.mysql_database)
            #Creating a cursor object using the cursor() method
            self._cursor = self._dbconn.cursor()
        except mysql.connector.Error as err:
            print(err)
    def add_channel_details(self,data):

        #pprint(type(data))
        # Parse dict to get mysql db table params
        # Add Channel Data
        channel_name = data['channel_name']
        publish_time = data['publish_time']
        channel_id = data['channel_id']
        #video_count = data['video_count']
        subscriber_count = data['subscriber_count']
        description = data['description']
        total_views = data['total_views']
        channel_status = data['status']

        add_channel_qry = "INSERT INTO channels(channel_id,channel_name,subscriber_count,publish_time,channel_view,channel_description,channel_status) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        add_channel_val = (channel_id,channel_name,subscriber_count,publish_time,total_views,description,channel_status)
        self._cursor.execute(add_channel_qry,add_channel_val)
        self._dbconn.commit()
        
        channel_insert_id = self._cursor.lastrowid
        # Add Playlist Data
        playlist_id = data['playlist_id']

        add_playlist_qry = "INSERT INTO playlist(cid,playlist_id) VALUES (%s,%s)"
        add_playlist_val = (channel_insert_id,playlist_id)
        self._cursor.execute(add_playlist_qry,add_playlist_val)
        self._dbconn.commit()
        playlist_insert_id = self._cursor.lastrowid
        

        # Add Videos Data
        for i in data['videos'].values():
            video_id = i['video_id']
            video_title = i['video_title']
            video_description = i['video_description']
            video_publish_time = i['publishedAt']
            v_view_count = i['view_count']
            v_like_count = 0
            try:
                v_like_count = i['like_count']
            except:
                pass
            v_fav_count = i['favorite_count']
            v_thumbnail = i['thumbnail']
            caption_status = i['caption_status']
            duration = i['duration']
            #v_com_count = data['videos'][i]['comment_count']

            add_video_qry = "INSERT INTO videos(playlist_id,video_name,video_id,video_description,published_date,view_count,like_count,favourite_count,duration,thumbnail,caption_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            add_video_val = (playlist_insert_id,video_title,video_id,video_description,video_publish_time,v_view_count,v_like_count,v_fav_count,duration,v_thumbnail,caption_status)
            #pprint(add_video_val)
            #exit()

            self._cursor.execute(add_video_qry,add_video_val)
            self._dbconn.commit()
            video_insert_id = self._cursor.lastrowid

            if 'comments' in i:
                for j in i['comments'].values():

                    comment_id = j['comment_id']
                    comment_text = j['comment_text']
                    comment_author = j['author']
                    comment_publish_time = j['publishedAt']

                    add_comment_qry = "INSERT INTO comments(comment_id,video_id,comment_text,comment_author,comment_published_date) VALUES (%s,%s,%s,%s,%s)"
                    add_comment_val = (comment_id,video_insert_id,comment_text,comment_author,comment_publish_time)
                    self._cursor.execute(add_comment_qry,add_comment_val)
                    self._dbconn.commit()