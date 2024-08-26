import time
import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from .models import Schedule
from django.http import JsonResponse
from django.core.serializers import serialize
from .aggregate import Aggregator
from .newsRepository import NewsRepository
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .sendUpdate import create_updates, update_subscribers

nr = NewsRepository()


def merge_updates(updates, new):
    """
    Expects both dictionaries to have the following structure
    {
        "emai1": {
            "keyword1": [News1, News2],
            "keyword2": [News2, News3]
        },
        "email2": {
            "keyword3": [News1, News4]
        }
    }
    """

    if not updates:
        return new

    for email in new:
        if email not in updates:
            updates[email] = new[email]
        else:
            for keyword in new[email]:
                if keyword not in updates[email]:
                    updates[email][keyword] = new[email][keyword]
                else:
                    # TODO: This might cause duplicate news to show up on updates under a keyword
                    updates[email][keyword].extend(new[email][keyword])

    return updates


def print_updates(updates):
    """
        Expects updates to have the following structure
        {
            "emai1": {
                "keyword1": [News1, News2],
                "keyword2": [News2, News3]
            },
            "email2": {
                "keyword3": [News1, News4]
            }
        }
    """
    for email in updates:
        print(f"Email: {email}")
        for keyword in updates[email]:
            print(f"\t A keyword with {len(updates[email][keyword])} news")


def search(request):
    query = request.GET.get('query', '')
    results = nr.search(query)
    return JsonResponse({"results": results})


@csrf_exempt
def verify(request, _id, status):
    nr.verify_news(_id, status)
    if status.lower() not in ["true", "false"]:
        return HttpResponseBadRequest("Invalid status")

    return HttpResponse("Status Updated Successfully")


@csrf_exempt
def subscribe(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    total_subscriptions = Schedule.objects.count()
    if total_subscriptions > 100:
        return HttpResponseForbidden({'message': 'Subscription limit reached. Cannot accept new subscriptions.'})

    json_data = json.loads(request.body.decode('utf-8'))

    keyword = json_data.get('keyword', '').lower()
    email = json_data.get('email', '')
    schedule = json_data.get('schedule', '').lower()

    if len(keyword.split()) > 1:
        return HttpResponseForbidden({'message': 'Keyword can only be one word'})

    subscription = Schedule.objects.filter(keyword=keyword, email=email).first()

    if not subscription:
        allowed_schedules = {"immediately", "once_a_day", "twice_a_day", "once_a_week"}
        if schedule not in allowed_schedules:
            return HttpResponseForbidden({'message': 'No such schedule'})

        new_subscription = Schedule(
            keyword=keyword,
            email=email,
            schedule=schedule
        )

        new_subscription.save()
        return HttpResponse(f'Successfully subscribed to "{keyword}".')
    else:
        return HttpResponseBadRequest(f'Already subscribed to "{keyword}".')


# TODO: Maybe benchmark this. It might make the server slow
@csrf_exempt
def test(request):
    updates = None
    current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p")
    print(f"Starting Aggregator at: {current_time}")
    iteration = 0
    while True:
        print(f"Iteration {iteration}")
        a = Aggregator()
        news_list = a.run()
        curr_updates = create_updates(news_list)
        updates = merge_updates(updates, curr_updates)
        print_updates(updates)
        update_subscribers(updates)
        time.sleep(15 * 60)
        iteration += 1
