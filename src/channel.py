import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY_YOUTUBE')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """
    Класс для ютуб-канала
    """

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id

        service = Channel.get_service()
        parts = 'snippet,statistics'
        result = service.channels().list(id=channel_id, part=parts).execute()
        channel = result['items'][0]['snippet']
        statistics = result['items'][0]['statistics']

        self.id = channel_id
        self.title = channel['title']
        self.description = channel['description']
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subscriber_count = statistics['subscriberCount']
        self.video_count = statistics['videoCount']
        self.view_count = statistics['viewCount']

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return youtube

    def to_json(self, filename):
        """
        Сохраняет в файл значения атрибутов экземпляра Channel
        """
        data = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
