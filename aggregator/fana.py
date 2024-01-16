import requests

from .models import News
from .newsRepository import NewsRepository
from .newsSource import NewsSource
import xml.etree.ElementTree as ET
from lxml import html
from datetime import datetime


class Fana(NewsSource):
    def __init__(self):
        super().__init__("Fana Broadcasting Corporate")
        self.nr = NewsRepository()

    def tryLoadAndSaveNews(self):
        rss_feed_url = 'https://www.fanabc.com/english/category/localnews/feed/'
        response = requests.get(rss_feed_url)

        if response.status_code != 200:
            print(f"Failed to retrieve the RSS feed. Status code: {response.status_code}")

        # Parse the XML content
        root = ET.fromstring(response.content)

        # Iterate through each 'item' element and extract title and link
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text

            description_html = item.find('description').text
            description = html.fromstring(description_html).text_content()

            pub_date_str = item.find('pubDate').text
            pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")

            source = self.source

            thumbnail = item.find('description').text.split('" class=')[0].split('src="')[1]

            news = News(
                title=title,
                link=link,
                description=description,
                pub_date=pub_date,
                source=source,
                thumbnail=thumbnail)

            news.save()
