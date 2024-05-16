from .fana import Fana
from .esat import Esat
from .etv import Etv
from .bbc_amharic import BBCAmharic


class Aggregator:
    def __init__(self):
        self.newsSources = []
        self.threads = []

    def AddNewsSources(self):
        self.newsSources.append(Etv())
        self.newsSources.append(Esat())
        self.newsSources.append(Fana())
        self.newsSources.append(BBCAmharic())

    def LoadAllNews(self):
        news_list = []
        for newsSource in self.newsSources:
            news_list.extend(newsSource.tryLoadAndSaveNews())

        return news_list

    def run(self):
        self.AddNewsSources()
        return self.LoadAllNews()
