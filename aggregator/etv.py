import pytz
import requests
from .models import News
from bs4 import BeautifulSoup
from django.utils import timezone
from .newsSource import NewsSource
from datetime import datetime, timedelta
from .newsRepository import NewsRepository

nr = NewsRepository()


def get_duration_from_amharic_time(amharic_time):
    tokens = amharic_time.split()

    exponent = 0
    if tokens[1] == "ደቂቃ":
        exponent = 1
    elif tokens[1] == "ሰዓት":
        exponent = 2
    elif tokens[1] == "ቀን":
        exponent = 3

    return int(tokens[0]) * (60 ** exponent) + int()


class Etv(NewsSource):
    def __init__(self):
        super().__init__("Ethiopian Broadcasting Corporation")
        self.nr = NewsRepository()

    def tryLoadAndSaveNews(self):
        website_url = "https://www.ebc.et/archive.aspx"

        url_prefix = "https://www.ebc.et"

        response = requests.get(website_url)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the main container with class "blog-page-area"
        blog_page_area = soup.find('div', class_='blog-page-area')

        # Find the div with class "tab-content" inside the "blog-page-area"
        tab_content = blog_page_area.find('div', class_='tab-content')

        # Find all divs inside the "tab-content" with names like "content_tabJanuary", "content_tabFebruary", etc.
        months_divs = tab_content.find_all('div', recursive=False)

        latest_entry = nr.get_latest_by_source(self.source)

        for month_div in months_divs:
            # Find the div with class "row" inside the current month's div
            row_div = month_div.find('div', class_='row')

            # Find all the <li> elements inside the current month's div
            li_elements = row_div.find_all('li')

            for li in li_elements:
                # Extract the information from the <li> element
                link = url_prefix + '/' + li.find('a')['href']
                image_src = url_prefix + '/' + li.find('img')['src']
                title = li.find('h3').text.strip()
                date = li.find('span', class_='date').find('span', class_='date').text.strip()

                # Convert Etv's weird "3 ቀን በፊት" format to a datetime object
                total_duration_seconds = get_duration_from_amharic_time(date)
                current_datetime = datetime.now(pytz.timezone('UTC'))
                duration = timedelta(seconds=total_duration_seconds)
                result_datetime = current_datetime - duration

                if latest_entry:
                    print(result_datetime > latest_entry.pub_date, result_datetime, latest_entry.pub_date)
                else:
                    print("No latest entry")

                if not latest_entry or result_datetime > latest_entry.pub_date:
                    news = News(
                        title=title,
                        link=link,
                        pub_date=result_datetime,
                        source=self.source,
                        thumbnail=image_src,
                    )

                    news.save()