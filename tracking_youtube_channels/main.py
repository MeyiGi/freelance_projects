import os
import time
import smtplib
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Set your API key, email credentials, and notification conditions
API_KEY = "AIzaSyBIIpTj0aFYlrSJt5POOaqP_82BD5Ya45c"
EMAIL_ADDRESS = "kanybekovdaniel6@gmail.com"
EMAIL_API = "zffr hyso tjrh zdim"
TO_EMAIL = "kanybekovdaniel369@gmail.com"
NOTIFY_THRESHOLD_VIEWS = 1000  # X1 in views
TRACK_DURATION = timedelta(hours=1)  # X2 in hours
CHECK_INTERVAL = 60  # Check every minute

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to load tracked channels
def load_tracked_channels(filename="tracked_youtube_channels.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Function to send an email notification
def send_email_notification(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_API)
        server.send_message(msg)
    print("Email notification sent.")

# Function to get the latest video for a channel
def get_latest_video(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    response = request.execute()
    if response["items"]:
        video = response["items"][0]
        video_id = video["id"].get("videoId")
        video_title = video["snippet"]["title"]
        return video_id, video_title
    return None, None

# Function to check video statistics
def check_video_stats(video_id):
    request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    response = request.execute()
    if response["items"]:
        stats = response["items"][0]["statistics"]
        return int(stats.get("viewCount", 0)), int(stats.get("likeCount", 0))
    return 0, 0

# Main monitoring function
def monitor_channels():
    tracked_channels = load_tracked_channels()
    last_checked_videos = {}
    notified_videos = set()  # To track notified videos

    while True:
        for channel_id in tracked_channels:
            video_id, video_title = get_latest_video(channel_id)

            if video_id:
                # Check if the last checked video is the same as the current video
                if channel_id in last_checked_videos and last_checked_videos[channel_id]["id"] == video_id:
                    print(f"Skipping {channel_id}: no new video.")
                    continue  # Skip further processing for this channel

                # New video detected
                last_checked_videos[channel_id] = {"id": video_id, "title": video_title, "time": datetime.now()}
                print(f"New video detected: {video_title} ({video_id})")

                # Check if the video was notified and within the track duration
                if (datetime.now() - last_checked_videos[channel_id]["time"] <= TRACK_DURATION and 
                        video_id not in notified_videos):
                    view_count, _ = check_video_stats(video_id)
                    if view_count >= NOTIFY_THRESHOLD_VIEWS:
                        send_email_notification(
                            f"Video reached {NOTIFY_THRESHOLD_VIEWS} views!",
                            f"'{video_title}' by channel {channel_id} has reached {view_count} views."
                        )
                        notified_videos.add(video_id)  # Mark this video as notified

        # Wait for the next check
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_channels()
