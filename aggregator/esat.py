import feedparser
from .models import News
from bs4 import BeautifulSoup
from datetime import datetime
from .newsSource import NewsSource
from .newsRepository import NewsRepository

from .sendUpdate import create_updates


nr = NewsRepository()


class Esat(NewsSource):
    def __init__(self):
        super().__init__("The Ethiopian Satellite Television and Radio", 'https://ethsat.com/feed/')
        self.nr = NewsRepository()

    def tryLoadAndSaveNews(self):
        try:
            feed = feedparser.parse(self.url)

            latest_entry = nr.get_latest_by_source(self.source)

            news_list = []
            news_count = 0
            for entry in feed.entries:
                content_html = entry.content[0].value
                soup = BeautifulSoup(content_html, 'html.parser')

                # Convert the string to a datetime object
                formatted_published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

                if not latest_entry or formatted_published_date > latest_entry.pub_date:
                    news = News(
                        title=entry.title,
                        link=entry.link,
                        description=entry.content[0].value,
                        pub_date=formatted_published_date,
                        source=self.source)

                    news.save()
                    news_list = []
                    news_count += 1

            create_updates(self.source, news_list)
            print(f"          {self.source}: added {news_count}")

        except Exception as e:
            print(f"Exception occurred while fetching from {self.source}: {e}")



