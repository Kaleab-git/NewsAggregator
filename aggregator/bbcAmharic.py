from .newsSource import NewsSource


class BBCAmharic(NewsSource):
    def __init__(self):
        super().__init__("BBC News Amharic")

    def tryLoadAndSaveNews(self):
        print("Trying to load BBC Amharic news...")
