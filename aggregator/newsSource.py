from abc import ABC, abstractmethod


class NewsSource(ABC):
    def __init__(self, source, url):
        self.source = source
        self.url = url

    @abstractmethod
    def tryLoadAndSaveNews(self):
        pass
