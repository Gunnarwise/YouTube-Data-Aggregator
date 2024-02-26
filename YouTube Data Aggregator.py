# import nessecary libraries
from googleapiclient.discovery import build

# variables for API
API_KEY = "AIzaSyCI9CAwFxq6fjFOgIiJ6EM1KVlsaTAxKc4"
channel_id = "UC6107grRI4m0o2-emgoDnAA"
youtube = build('youtube', 'v3', developerKey=API_KEY)


### Function to get all stats ###
def get_channel_stats(youtube, channel_id):
    # requests the channel stats
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    return response['items']



### Function to get video list ###
def get_video_list(youtube, upload_id):
    
    # define list to return
    video_list = []
    
    # request the playlist of all uploaded videos (only can give 50 at once)
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=upload_id,
        maxResults=50
    )

    next_page = True

    # loop until it runs out of pages
    while next_page:
        response = request.execute()
        data = response['items']

        # add each video to video list
        for video in data:
            video_id = video['contentDetails']['videoId']

            if video_id not in video_list:
                video_list.append(video_id)
        
        # if there is a next page, update request to get next page
        if 'nextPageToken' in response.keys():
            next_page = True
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=upload_id,
                maxResults=50,
                pageToken=response['nextPageToken']
            )
        # if no next page, end while loop
        else:
            next_page = False
    
    # return list of all videos
    return video_list


### function to make list of all stats of all videos ###
def get_video_details(youtube, video_list):
    stats_list = []

    for i in range(0, len(video_list), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_list[i:i+50]
        )

        data = request.execute()

        for video in data['items']:
            title = video['snippet']['title']
            published = video['snippet']['publishedAt']
            description = video['snippet']['description']
            tag_count = len(video['snippet'].get('tags', []))
            view_count = video['statistics'].get('viewCount',0)
            like_count = video['statistics'].get('likeCount',0)
            dislike_count = video['statistics'].get('dislikeCount',0)
            comment_count = video['statistics'].get('commentCount',0)

            stats_dictionary = dict(
                title=title, 
                published=published,
                description=description,
                tag_count=tag_count,
                view_count=view_count,
                like_count=like_count,
                dislike_count=dislike_count,
                comment_count=comment_count
                )
            
            stats_list.append(stats_dictionary)
    
    return stats_list



### End of functions ###

# store the result of get_channel_stats in a variable
channel_stats = get_channel_stats(youtube, channel_id)

# JSON id of 'uploads' playlist
playlist_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']

# get list of all videos
video_list = get_video_list(youtube, playlist_id)



video_data = get_video_details(youtube, video_list)

print(video_data[0])