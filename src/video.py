class Video:
    """
    Класс который инициализирует 'id видео'.
    """
    def __init__(self, likes=None, id_video=None, title='GIL в Python: зачем он нужен и как с этим жить', url=None,
                 views=None):
        self.id_video = id_video
        self.title = title
        self.url = url
        self.views = views
        self.likes = likes

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Класс который инициализирует 'id плейлиста'.
    """
    def __init__(self, likes, id_playlist):
        super().__init__(likes)
        self.title = 'MoscowPython Meetup 78 - вступление'
        self.id_playlist = id_playlist

    def __str__(self):
        return self.title
