import feedparser
from .models import News
from bs4 import BeautifulSoup
from datetime import datetime
from .newsSource import NewsSource
from .newsRepository import NewsRepository

nr = NewsRepository()

class Esat(NewsSource):
    def __init__(self):
        super().__init__("The Ethiopian Satellite Television and Radio")
        self.nr = NewsRepository()

    def tryLoadAndSaveNews(self):
        url = 'https://ethsat.com/feed/'

        feed = feedparser.parse(url)

        latest_entry = nr.get_latest_by_source(self.source)

        for entry in feed.entries:
            content_html = entry.content[0].value
            soup = BeautifulSoup(content_html, 'html.parser')

            # Convert the string to a datetime object
            formatted_published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

            # print(formatted_published_date, latest_entry.pub_date, formatted_published_date > latest_entry.pub_date)
            if not latest_entry or formatted_published_date > latest_entry.pub_date:
                news = News(
                    title=entry.title,
                    link=entry.link,
                    description=entry.content[0].value,
                    pub_date=formatted_published_date,
                    source=self.source)

                news.save()
