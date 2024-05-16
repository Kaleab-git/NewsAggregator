import pytz
import requests
from .models import News
from bs4 import BeautifulSoup
from datetime import datetime
from .newsSource import NewsSource
from .newsRepository import NewsRepository

from .sendUpdate import create_updates

nr = NewsRepository()


class BBCAmharic(NewsSource):
    def __init__(self):
        super().__init__("BBC News Amharic", 'https://www.bbc.com/amharic/topics/c7zp57r92v5t')
        self.nr = NewsRepository()

    def tryLoadAndSaveNews(self):

        try:
            # Replace 'your_url' with the actual URL of the website you want to scrape
            response = requests.get(self.url)
            news_list = []
            news_count = 0
            latest_entry = nr.get_latest_by_source(self.source)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')

                # Find the div with id=root
                root_div = soup.find('div', id='root')

                # Find the div with id=main-wrapper inside the root div
                main_wrapper_div = root_div.find('div', id='main-wrapper')

                # Find the first div inside the main tag
                main_div = main_wrapper_div.find('main').find('div')

                # Find the div with data-testid=curation-grid-normal
                curation_grid_div = main_div.find('div', {'data-testid': 'curation-grid-normal'})

                # Find the ul tag inside the curation-grid-normal div
                ul_tag = curation_grid_div.find('ul')

                # Iterate through li tags under the ul tag
                for li_tag in ul_tag.find_all('li'):
                    # Process each li tag as needed
                    news_div = li_tag.find('div')
                    # Find the sibling div with class name 'promo-text'
                    text_div = news_div.find('div', class_='promo-text')

                    time_tag = text_div.find('time')
                    date_string = time_tag.get('datetime')

                    h2_tag = text_div.find('h2')
                    a_tag = h2_tag.find('a')
                    link = a_tag.get('href')
                    title = a_tag.get_text(strip=True)

                    image_div = news_div.find('div', class_='promo-image').find('div').find('div')
                    picture_tag = image_div.find('picture')
                    img_tag = picture_tag.find('img')
                    src_value = img_tag['src']

                    timezone = pytz.timezone('UTC')
                    string_as_datetime = datetime.strptime(date_string, '%Y-%m-%d')
                    string_as_datetime = string_as_datetime.replace(tzinfo=timezone)

                    if not latest_entry or string_as_datetime > latest_entry.pub_date:
                        news = News(
                            title=title,
                            link=link,
                            pub_date=string_as_datetime,
                            source=self.source,
                            thumbnail=src_value,
                        )

                        news.save()
                        news_list.append(news)
                        news_count += 1

                # create_updates(self.source, news_list)
                print(f"          {self.source}: added {news_count}")
                return news_list

            else:
                print(f"Failed to fetch {self.source}. Status code: {response.status_code}")

        except Exception as e:
            print(f"Exception occurred while fetching from {self.source}: {e}")
            return []
