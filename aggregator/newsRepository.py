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
            {
                "id": item.id,
                "title": item.title,
                "pub_date": item.pub_date,
                "source": item.source,
                "thumbnail": item.thumbnail,
                "is_verified": item.is_verified
            }
            for item in search_results_queryset
        ]
        return results

    @staticmethod
    def get_latest_by_source(source):
        latest_entry = News.objects.filter(source=source).order_by('-pub_date').first()
        return latest_entry
