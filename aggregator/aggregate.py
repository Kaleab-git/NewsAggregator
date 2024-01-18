import threading
from .fana import Fana
from .esat import Esat
from .etv import Etv


class Aggregator:
    def __init__(self):
        self.newsSources = []
        self.threads = []

    def AddNewsSources(self):
        self.newsSources.append(Etv())
        self.newsSources.append(Esat())
        self.newsSources.append(Fana())

    def LoadAllNews(self):
        for newsSource in self.newsSources:
            newsSource.tryLoadAndSaveNews()

    def run(self):
        self.AddNewsSources()
        self.LoadAllNews()
