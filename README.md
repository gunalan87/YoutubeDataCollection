# YoutubeDataCollection
Get Youtube channel data via Youtube Data API, and store the data in MongoDB and MySQL.

**Techologies used:**
1. Python
2. MySQL
3. MongoDB
4. Youtube Data API

**Workflow:**
1. Enter a Youtube channel id in application's main page to retrieve channel details via Youtube Data API and store it in Datalake MongoDB.
2. The unstructured/semi-structured data of Youtube channel can be migrated to MySQL Database.
3. From MySQL Database we can analyze all the channels data.

**Youtube Data API info:**
Kindly go through the below link to get started in Youtube Data API implementation.
https://developers.google.com/youtube/v3/getting-started

Used .env file to store important static information in order to separate code from configuration settings.
