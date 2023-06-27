from datetime import timedelta

import isodate

from src.video import PLVideo, Video, youtube


class MixinPlayList:
    """
    Mixin для плейлиста.
    """
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id


class PlayList(MixinPlayList, PLVideo, Video):
    """
    Класс плейлиста.
    """
    def __init__(self, playlist_id: str):
        super().__init__(playlist_id)
        self.parts = "snippet,contentDetails,statistics"
        playlist_response = youtube.playlists().list(part='snippet,contentDetails', id=self.playlist_id).execute()
        if playlist_response['items']:
            self.title = playlist_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self) -> timedelta:
        playlist_response = youtube.playlists().list(part='snippet,contentDetails', id=self.playlist_id).execute()
        if playlist_response['items']:
            self.title = playlist_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        while True:
            playlist_items_response = youtube.playlistItems().list(part='contentDetails',
                                                                   playlistId=self.playlist_id).execute()
            start_times = []
            for item in playlist_items_response['items']:
                video_id = item['contentDetails']['videoId']
                video_duration = youtube.videos().list(part='contentDetails', id=video_id).execute()
                duration = video_duration['items'][0]['contentDetails']['duration']
                start_times.append(duration)
            total = timedelta()
            for time in start_times:
                total += isodate.parse_duration(time)
            return total

    def show_best_video(self) -> str:
        best_likes = -1
        playlist_items = youtube.playlistItems().list(part='snippet,contentDetails',
                                                      playlistId=self.playlist_id, ).execute()
        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_response = youtube.videos().list(part='statistics', id=video_id).execute()
            video_likes = int(video_response['items'][0]['statistics']['likeCount'])
            if video_likes > best_likes:
                best_video_id = video_id

        return f"https://youtu.be/{best_video_id}"
