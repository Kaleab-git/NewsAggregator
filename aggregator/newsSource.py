from abc import ABC, abstractmethod


class NewsSource(ABC):
    def __init__(self, source):
        self.source = source

    @abstractmethod
    def tryLoadAndSaveNews(self):
        pass
