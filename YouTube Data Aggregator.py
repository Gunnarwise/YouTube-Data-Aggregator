# import nessecary libraries
from googleapiclient.discovery import build
import time

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

    # loop through each video in video list and request the stats
    for i in range(0, len(video_list), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_list[i:i+50]
        )

        data = request.execute()

        # in each video, grab the stats that are wanted
        for video in data['items']:
            title = video['snippet']['title']
            published = video['snippet']['publishedAt']
            description = video['snippet']['description']
            tag_count = len(video['snippet'].get('tags', []))
            view_count = video['statistics'].get('viewCount',0)
            like_count = video['statistics'].get('likeCount',0)
            dislike_count = video['statistics'].get('dislikeCount',0)
            comment_count = video['statistics'].get('commentCount',0)

            # dictionary of each individual video stats
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
            
            # add each dictionary to a list of dictionaries
            stats_list.append(stats_dictionary)
    
    # return list of stats
    return stats_list



### function to display given video stats in a readable way ###
def display_video_stats(video_stats):

    # format the published date
    timestamp = video_stats["published"]
    ts = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")

    # print all stats
    print("\n" * 10 + "-" * 50)
    print("Video Stats For:\n")
    print(video_stats["title"] + "\n")
    print("posted on: " + time.strftime("%m/%d/%Y", ts))
    print("views: " + str(video_stats["view_count"]))
    print("likes: " + str(video_stats["like_count"]))
    print("comments: " + str(video_stats["comment_count"]))
    print("-" * 50 + "\n\n")
    input("Press Enter to go back to main menu: ")




def display_channel_stats(channel_stats):
    # format the published date
    timestamp = channel_stats[0]["snippet"]["publishedAt"]
    ts = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")

    # print all stats
    print("\n" * 10 + "-" * 50)
    print("Channel Stats For:\n")
    print(channel_stats[0]["snippet"]["title"] + "\n")
    print("channel created on: " + time.strftime("%m/%d/%Y", ts))
    print("subscribers: " + str(channel_stats[0]["statistics"]["subscriberCount"]))
    print("total views: " + str(channel_stats[0]["statistics"]["viewCount"]))
    print("videos posted: " + str(channel_stats[0]["statistics"]["videoCount"]))
    print("-" * 50 + "\n\n")
    input("Press Enter to go back to main menu: ")


def display_top_5(top_5_stat):
    print("\n" * 10)
    print(f"{'Top 5 ' + top_5_stat + 's' : ^150}\n")
    print("+" + "-" * 150 + "+")
    print(f"|{'#1 ' + top_5_stat + ":" : ^74}|{'#2 ' + top_5_stat + ":" : ^74} |")
    print("|" + " " * 74 + "|" + " " * 75 + "|")
    print(f"|{'TITLE OF VIDEO' : ^74}|{'TITLE OF VIDEO' : ^74} |")
    print("|" + " " * 74 + "|" + " " * 75 + "|")
    print(f"|{'posted on:' : ^74}|{'posted on:' : ^74} |")
    print(f"|{'views:' : ^74}|{'views:' : ^74} |")
    print(f"|{'likes:' : ^74}|{'likes:' : ^74} |")
    print(f"|{'comments:' : ^74}|{'comments:' : ^74} |")
    print("|" + " " * 74 + "|" + " " * 75 + "|")
    print("+" + "-" * 150 + "+")
    print(f"|{'#3 ' + top_5_stat + ":" : ^49}|{'#4 ' + top_5_stat + ":" : ^49}|{'#5 ' + top_5_stat + ":" : ^49} |")
    print("|" + " " * 49 + "|"+ " " * 49 + "|"+ " " * 50 + "|")
    print(f"|{'TITLE OF VIDEO' : ^49}|{'TITLE OF VIDEO' : ^49}|{'TITLE OF VIDEO' : ^49} |")
    print("|" + " " * 49 + "|"+ " " * 49 + "|"+ " " * 50 + "|")
    print(f"|{'posted on:' : ^49}|{'posted on:' : ^49}|{'posted on:' : ^49} |")
    print(f"|{'views:' : ^49}|{'views:' : ^49}|{'views:' : ^49} |")
    print(f"|{'likes:' : ^49}|{'likes:' : ^49}|{'likes:' : ^49} |")
    print(f"|{'comments:' : ^49}|{'comments:' : ^49}|{'comments:' : ^49} |")
    print("|" + " " * 49 + "|"+ " " * 49 + "|"+ " " * 50 + "|")
    print("+" + "-" * 150 + "+")
    input("Press Enter to go back to main menu: ")





# displays options for data visualization
def display_menu_and_get_choice():
    print("\n" * 10 + "-" * 50)
    print(f"\n{'Menu Options:' : ^30}\n")
    print(f"{'1: channel stats' : <30}")
    print(f"{'2: stats for most recent video' : <30}")
    print(f"{'3: top 5 liked videos  (not fully implemented)' : <30}")
    print(f"{'4: top 5 viewed videos  (not fully implemented)' : <30}")
    print(f"{'5: top 5 commented videos  (not fully implemented)' : <30}")
    print(f"{'6: show filter options  (not implemented yet)' : <30}\n")
    print("-" * 50 + "\n")
    choice = input("type the number of your choice, or press Enter to quit: ")
    return choice

# looks at menu choice and runs correct method
def run_menu_choice(choice, channel_stats, video_stats):
    if choice == "1":
        display_channel_stats(channel_stats)
        return False
    elif choice == "2":
        display_video_stats(video_stats[0])
        return False
    elif choice == "3":
        display_top_5("liked video")
        return False
    elif choice == "4":
        display_top_5("viewed video")
        return False
    elif choice == "5":
        display_top_5("commented video")
        return False
    elif choice == "6":
        print(6)
        return False
    elif choice == "":
        print("quit program")
        return True
    else:
        print("invalid input, please try again")
        new_choice = input("type the number of your choice, or press enter to quit: ")
        return run_menu_choice(new_choice, channel_stats, video_data)



### End of functions ###

# store the result of get_channel_stats in a variable
channel_stats = get_channel_stats(youtube, channel_id)

# JSON id of 'uploads' playlist
playlist_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']

# get list of all videos
video_list = get_video_list(youtube, playlist_id)


# get list of all video stats
video_data = get_video_details(youtube, video_list)
 

# display stats of most recent video
#display_video_stats(video_data[0])  


choice = display_menu_and_get_choice()
end_program = run_menu_choice(choice, channel_stats, video_data)

while not end_program:
    choice = display_menu_and_get_choice()
    end_program = run_menu_choice(choice, channel_stats, video_data)


