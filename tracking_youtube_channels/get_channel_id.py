from googleapiclient.discovery import build

# -----------------------------------------------------------

API_KEY = 'AIzaSyBIIpTj0aFYlrSJt5POOaqP_82BD5Ya45c'       # youtube api
channels = ["HowdyhoNet", "CNBC-TV18", "NDTVProfitIndia"]

# -----------------------------------------------------------
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(username):
    request = youtube.search().list(
        part="snippet",
        q=username,
        type="channel",
        maxResults=1
    )
    response = request.execute()
    
    # Проверяем, найден ли канал
    if 'items' in response and response["items"]:
        return response["items"][0]["snippet"]["channelId"]
    else:
        print(f"Channel '{username}' not found.")
        return None

for channel in channels:
    channel_id = get_channel_id(channel)
    if channel_id:
        print(channel_id)
