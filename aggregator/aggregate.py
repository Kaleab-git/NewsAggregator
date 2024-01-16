import threading
from .fana import Fana
from .bbcAmharic import BBCAmharic


class Aggregator:
    def __init__(self):
        self.newsSources = []
        self.threads = []

    def AddNewsSources(self):
        self.newsSources.append(Fana())
        self.newsSources.append(BBCAmharic())

    def LoadAllNews(self):
        for newsSource in self.newsSources:
            thread = threading.Thread(target=newsSource.tryLoadAndSaveNews)
            self.threads.append(thread)
            thread.start()


        # Wait for all threads to complete for a maximum of 10 seconds
        for thread in self.threads:
            thread.join(timeout=10)

        # Terminate any threads that are still alive after the timeout
        for thread in self.threads:
            if thread.is_alive():
                thread.join()




    def run(self):
        self.AddNewsSources()
        self.LoadAllNews()
