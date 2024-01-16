from .models import News
from django.db.models import Q

class NewsRepository:
    @staticmethod
    def save_news(title, description, content, pub_date, source, link, thumbnail, is_verified):
        news = News(
            title=title,
            description=description,
            content=content,
            pub_date=pub_date,
            source=source,
            link=link,
            thumbnail=thumbnail,
        )
        news.save()


    @staticmethod
    def verify_news(news_id, status_string):
        news = News.objects.get(id=news_id)
        if status_string == "true" or status_string == "True":
            status = True
        else:
            status = False

        news.is_verified = status
        news.save()

    @staticmethod
    def search(query):
        search_results_queryset = News.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query)
        )

        results = [
        {"title": item.title, "content": item.content}
        for item in search_results_queryset
    ]
        return results

    @staticmethod
    def get_latest(self):
        return []