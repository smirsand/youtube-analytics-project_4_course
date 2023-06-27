from datetime import timedelta

import isodate
from googleapiclient.errors import HttpError

from src.video import PLVideo, Video, youtube


class MixinPlayList:
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None


class PlayList(MixinPlayList, PLVideo, Video):
    def __init__(self, playlist_id: str):
        super().__init__(playlist_id)
        self.parts = "snippet,contentDetails,statistics"
        playlist_response = youtube.playlists().list(part='snippet,contentDetails', id=self.playlist_id).execute()
        if playlist_response['items']:
            self.title = playlist_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self) -> timedelta:
        total = timedelta()
        try:
            playlist_response = youtube.playlists().list(part='snippet,contentDetails', id=self.playlist_id).execute()
            playlist_items = playlist_response['items'][0]['contentDetails']['itemCount']
            if playlist_response['items']:
                self.title = playlist_response['items'][0]['snippet']['title']
                self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
                print(self.title)
                print(self.url)

            next_page_token = None
            while True:
                playlist_items_response = youtube.playlistItems().list(part='contentDetails',
                                                                       playlistId=self.playlist_id, maxResults=50,
                                                                       pageToken=next_page_token).execute()

                start_times = []  # перезаписывается на каждой итерации, содержит продолжительности видео
                for item in playlist_items_response['items']:
                    video_id = item['contentDetails']['videoId']
                    video_duration = youtube.videos().list(part='contentDetails', id=video_id).execute()
                    duration = video_duration['items'][0]['contentDetails']['duration']
                    start_times.append(duration)
                    print(start_times)

                total = timedelta()
                for time in start_times:
                    total += isodate.parse_duration(time)

                print(str(total))
                next_page_token = playlist_items_response.get('nextPageToken')
                if next_page_token is None:
                    break

            return total

        except HttpError as error:
            print(f'An error occurred: {error}')
            return total

    def show_best_video(self) -> str:
        try:
            playlist_items = youtube.playlistItems().list(part="snippet", playlistId=self.playlist_id,
                                                          maxResults=50).execute()
            best_video = playlist_items['items'][0]['snippet']['resourceId']['videoId']
            best_likes = 0

            for item in playlist_items['items']:
                video_id = item["snippet"]["resourceId"]["videoId"]
                rating_response = youtube.videos().getRating(id=video_id).execute()
                likes = rating_response['items'][0]['rating'].get('likeCount', 0)

                if likes > best_likes:
                    best_likes = likes
                    best_video = f"https://www.youtube.com/watch?v={video_id}"

            return best_video

        except HttpError as error:
            print(f'An error occurred: {error}')
            return "Video not found"
