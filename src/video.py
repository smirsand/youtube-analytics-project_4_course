class Video:
    """
    Класс который инициализирует 'id видео'.
    """

    def __init__(self, id_video=None, video_title=None, video_url=None, views_count=0, likes_count=0):
        self.id_video = id_video
        self.video_title = 'GIL в Python: зачем он нужен и как с этим жить'
        self.video_url = video_url
        self.views_count = views_count
        self.likes_count = likes_count

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """
    Класс который инициализирует 'id плейлиста'.
    """

    def __init__(self, id_video=None, video_title=None, video_url=None, views_count=0, likes_count=0, id_playlist=None):
        super().__init__(id_video, video_title, video_url, views_count=views_count, likes_count=likes_count)
        self.video_title = 'MoscowPython Meetup 78 - вступление'
        self.id_playlist = id_playlist

    def __str__(self):
        return self.video_title
