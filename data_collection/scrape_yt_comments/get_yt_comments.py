from get_links import get_youtube_links

from googleapiclient.discovery import build
import pandas as pd
import getpass
from pytube import extract

entity = 'devara pre release cancel'



api_key = 'AIzaSyCW3EkzaxYQG40Ko5BaFI0prkfc-lYqZyI'

youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get replies for a specific comment
def get_replies(youtube, parent_id, video_id):  # Added video_id as an argument
    replies = []
    next_page_token = None

    while True:
        reply_request = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=10,
            pageToken=next_page_token
        )
        reply_response = reply_request.execute()

        for item in reply_response['items']:
            comment = item['snippet']
            replies.append({
                'VideoID': video_id,
                'Comment': comment['textDisplay']
            })

        next_page_token = reply_response.get('nextPageToken')
        if not next_page_token:
            break

    return replies

# Function to get all comments (including replies) for a single video
def get_comments_for_video(youtube, video_id):
    all_comments = []
    next_page_token = None

    while True:
        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token,
            textFormat="plainText",
            maxResults=10
        )
        comment_response = comment_request.execute()

        for item in comment_response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']
            all_comments.append({
                'VideoID': video_id,  # Directly using video_id from function parameter
                'Comment': top_comment['textDisplay']
            })

            # Fetch replies if there are any
            if item['snippet']['totalReplyCount'] > 0:
                all_comments.extend(get_replies(youtube, item['snippet']['topLevelComment']['id'], video_id))

        next_page_token = comment_response.get('nextPageToken')
        if not next_page_token:
            break

    return all_comments

all_comments = []
def get_comments(link) -> list:
    link_id = extract.video_id(link)

    # List to hold all comments from all videos
    video_comments = get_comments_for_video(youtube, link_id)
    all_comments.extend(video_comments)
    return video_comments

def get_yt_data(query):
    yt_links = get_youtube_links(query)

    for i, link in enumerate(yt_links):
        temp_comments = get_comments(link)
        print(f"Comments for Video {i+1}: {len(temp_comments)}")
        if i > 3:
            break

    comments_df = pd.DataFrame(all_comments)

    # Save the DataFrame to a CSV file
    filepath = r"../data/yt_comments.csv"
    comments_df.to_csv(filepath , index= True)
    return comments_df

if __name__ == "__main__":
    query = input("Enter a search query: ")
    get_yt_data(query)
    print(f"Comments saved to yt_comments_data.csv")