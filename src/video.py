import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = os.getenv('API_KEY_YOUTUBE')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """
    Класс инициализирует 'id видео' и получает информацию с канала.
    """

    def __init__(self, id_video):
        self.id_video = id_video

        try:
            video_response = youtube.videos().list(id=id_video, part='snippet,statistics').execute()
            self.video_title = video_response['items'][0]['snippet']['title']
            self.video_url = f"https://www.youtube.com/watch?v={id_video}"
            self.views_count = video_response['items'][0]['statistics']['viewCount']
            self.likes_count = video_response['items'][0]['statistics']['likeCount']

        except HttpError as error:
            print('An error occurred: %s', error)

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """
    Класс инициализирует 'id плейлиста'.
    """

    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id

        try:
            playlist_response = youtube.playlists().list(part='snippet', id=playlist_id).execute()
            playlist_title = playlist_response['items'][0]['snippet']['title']
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        except HttpError as error:
            print('An error occurred: %s' % error)

    def __str__(self):
        return self.video_title
