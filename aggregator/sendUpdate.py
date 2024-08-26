import base64
import os
from collections import defaultdict
from datetime import datetime, time

from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from django.template import Context, Template
from django.template.loader import render_to_string
from .models import Schedule



SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def render_django_template(template_path, context):
    """Render a Django template with the provided context."""

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    template = Template(template_content)
    rendered_content = template.render(Context(context))
    return rendered_content


def authenticate_gmail():
    """Authenticate and authorize the application to access Gmail API."""
    creds = None

    current_directory = os.getcwd()

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.path.dirname(__file__), "credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def gmail_send_message(creds, body, subject, recipient):
    """Create and send an email message. Print the returned message id."""
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(body, subtype="html")
        message["To"] = recipient
        message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

    return send_message


def update_subscribers(updates):
    """
    Selects updates ready to be sent, deletes them from updates, and sends them over email
    :param updates: nested dictionary with updates generated from news collected so far
    has the following structure:
    {
        "emai1": {
            "keyword1": [News1, News2],
            "keyword2": [News2, News3]
        },
    }
    """
    credentials = authenticate_gmail()
    # Convert defaultdicts to dict
    updates = dict(updates)
    for key in updates:
        updates[key] = dict(updates[key])

    for email in updates:
        keywords_list = list(updates[email].keys())

        time_now = datetime.now().time()
        updates_ready_for_email = defaultdict()

        for keyword in keywords_list:
            schedule = Schedule.objects.get(email=email, keyword=keyword)

            if schedule:
                if schedule.schedule == "immediately":
                    updates_ready_for_email[keyword] = updates[email][keyword]
                elif schedule.schedule == "once_a_day":
                    # Regardless of when the server started, a 15min increment lands in 6pm - 6:15pm only once
                    # Send a 6pm update
                    if time(18, 00) <= time_now <= time(18, 14):
                        updates_ready_for_email[keyword] = updates[email][keyword]
                        del updates[email][keyword]
                elif schedule.schedule == "twice_a_day":
                    # Send a 12pm update
                    if time(12, 0) <= time_now <= time(12, 14):
                        updates_ready_for_email[keyword] = updates[email][keyword]
                        del updates[email][keyword]
                    # Send a 6pm update
                    if time(18, 0) <= time_now <= time(18, 14):
                        updates_ready_for_email[keyword] = updates[email][keyword]
                        del updates[email][keyword]

        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'email-template.html')

        context = {'client_update': updates[email]}
        html_content = render_to_string(template_path, context)

        email_subject = f"Check out new"
        gmail_send_message(credentials, html_content, email_subject, email)


def create_updates(news_list):
    updates = defaultdict(lambda: defaultdict(list))
    keywords_queryset = Schedule.objects.values_list('keyword', flat=True).distinct()
    keywords_set = set(keywords_queryset)
    for news in news_list:
        seen = set()
        for word in news.title.split():
            # TODO: since content is mostly amharic .lower() probably wont matter
            word_lower = word.lower()
            # Check if each word is a keyword(and has subscribers)
            # TODO: Removing punctuations
            if word_lower in keywords_set:
                # To avoid multiple updates by the same keyword and from the same new source
                seen.add(word_lower)
                emails = Schedule.objects.filter(keyword=word_lower).values_list('email', flat=True)
                # Create an update for each email
                for email in emails:
                    updates[email][word_lower].append(news)

    return updates
