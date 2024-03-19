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
from urllib.error import HTTPError
import datetime
import isodate 
import datetime
from dateutil import parser
import pandas as pd
class YoutubeDataApi:
    def __init__(self):
        dotenv_path = Path('.env')  # Get DATA From .env file of your project
        load_dotenv(dotenv_path=dotenv_path)
        self.API_SERVICE_NAME = os.getenv("API_SERVICE_NAME")
        self.API_VERSION = os.getenv("API_VERSION")
        self.API_KEY = os.getenv("API_KEY")
        self.pil = os.getenv("playlistitemsperpage")
        self.max_comments_limit = os.getenv("max_comments")
        try:    # connect with your Youtube Data API
            self._youtube = googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION, developerKey=self.API_KEY)
        except:
            st.error("Youtube Data API exceeded daily usage limit, Please try tomorrow")
    def channel_details(self,channel_id):   # Get Channel information for a given channel_id
        try:
            _channel_request = self._youtube.channels().list(
                        part="snippet,contentDetails,statistics,status",
                       id=channel_id
                    )
            self._channel_response = _channel_request.execute()
            return self._channel_response
        except HTTPError as e:
            st.error(e)
            error_status_code = e.response.status_code
    def playlist_items(self,playlist_id,next_page_token):   # Get playlist details of a Youtube Channel
        _playlist_request = self._youtube.playlistItems().list(
                            part="contentDetails,id,status",
                            playlistId=playlist_id,
                            maxResults=self.pil,
                            pageToken=next_page_token)
        self._playlist_response = _playlist_request.execute()
        return self._playlist_response
    def video_comment_details(self,video_id):   # Get Video Details of a video ID in a channel.
        self.pil = int(self.pil)
        comment_count = []
        ivdetails = {}
        vd = self._youtube.videos().list(
                part="contentDetails,id,snippet,statistics,status",
                id = video_id
        )
        res_video_details = vd.execute()
        ivdetails['video_id'] = res_video_details['items'][0]['id']
        ivdetails['video_title'] = res_video_details['items'][0]['snippet']['title']
        ivdetails['video_description'] = res_video_details['items'][0]['snippet']['description']
        if 'tags' in res_video_details['items'][0]['snippet']:
            ivdetails['tags'] = res_video_details['items'][0]['snippet']['tags']
        ivdetails['publishedAt'] = res_video_details['items'][0]['snippet']['publishedAt']
        ivdetails['view_count'] = res_video_details['items'][0]['statistics']['viewCount']
        if 'likeCount' in res_video_details['items'][0]['statistics']:
            ivdetails['like_count'] = res_video_details['items'][0]['statistics']['likeCount']
        ivdetails['favorite_count'] = res_video_details['items'][0]['statistics']['favoriteCount']
        #ivdetails['dislike_count'] = res_video_details['items']['statistics']['dislikeCount'] # Only for video owner

        ivdetails['duration'] = pd.Timedelta(isodate.parse_duration(res_video_details['items'][0]['contentDetails']['duration'])).total_seconds()
        ivdetails['thumbnail'] = res_video_details['items'][0]['snippet']['thumbnails']['high']['url']
        ivdetails['caption_status'] = res_video_details['items'][0]['contentDetails']['caption']

        #if 'commentCount' in res_video_details['items'][0]['statistics'] and type(res_video_details['items'][0]#['statistics']['commentCount']) == 'int' and res_video_details['items'][0]['statistics']['commentCount'] > 0:
        if 'commentCount' in res_video_details['items'][0]['statistics'] and int(res_video_details['items'][0]['statistics']['commentCount']) > 0:
            ivdetails['comment_count'] = res_video_details['items'][0]['statistics']['commentCount']

            comment_details = self._youtube.commentThreads().list(
                            part = "snippet",
                            videoId = ivdetails['video_id'],
                            maxResults = self.max_comments_limit
                            )
            res_comment_details = comment_details.execute()
            try:
                if len(res_comment_details['items']) > 0:
                    ivdetails['comments'] = {}
                    for citem in range(0,len(res_comment_details['items'])):
                        comment_id = res_comment_details['items'][citem]['snippet']['topLevelComment']['id']
                        ivdetails['comments'][comment_id] = {}
                        ivdetails['comments'][comment_id]['comment_id'] = comment_id
                        ivdetails['comments'][comment_id]['comment_text'] = res_comment_details['items'][citem]['snippet']['topLevelComment']['snippet']['textDisplay']
                        ivdetails['comments'][comment_id]['author'] = res_comment_details['items'][citem]['snippet']['topLevelComment']['snippet']['authorDisplayName']
                        ivdetails['comments'][comment_id]['publishedAt'] = res_comment_details['items'][citem]['snippet']['topLevelComment']['snippet']['publishedAt']
            except:
                pass
        #pprint(comment_count)
        return ivdetails