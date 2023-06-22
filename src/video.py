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
        video_info = self.video_info(id_video)
        self.video_title = video_info['video_title']
        self.video_url = video_info['video_url']
        self.views_count = video_info['views_count']
        self.likes_count = video_info['likes_count']

    @staticmethod
    def video_info(video_id):
        try:
            parts = 'snippet,statistics'
            video_response = youtube.videos().list(id=video_id, part=parts).execute()
            video_title = video_response['items'][0]['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            views_count = video_response['items'][0]['statistics']['viewCount']
            likes_count = video_response['items'][0]['statistics']['likeCount']

            return {
                'id_video': video_id,
                'video_title': video_title,
                'video_url': video_url,
                'views_count': views_count,
                'likes_count': likes_count
            }
        except HttpError as error:
            print('An error occurred: %s', error)
            return None

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """
    Класс инициализирует 'id плейлиста'.
    """

    def __init__(self, id_video, playlist_id):
        super().__init__(id_video)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.video_title
