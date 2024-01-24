import base64
import os
from collections import defaultdict

from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from .models import News, Subscription
from django.template import Context, Template
from django.template.loader import render_to_string

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


def update_subscribers(updates, news_source):
    credentials = authenticate_gmail()
    # Convert defaultdicts to dict
    updates = dict(updates)
    for key in updates:
        updates[key] = dict(updates[key])

    for email in updates:
        keywords_list = list(updates[email].keys())
        keywords = ""
        if len(keywords_list) == 1:
            keywords = keywords_list[0]
        elif len(keywords_list) == 2:
            keywords = keywords_list[0] + " and " + keywords_list[1]
        elif len(keywords_list) == 3:
            keywords = keywords_list[0] + ", " + keywords_list[1] + ", and " + keywords_list[2]
        elif len(keywords_list) >= 4:
            keywords = keywords_list[0] + ", " + keywords_list[1] + ", and more"

        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'email-template.html')

        context = context = {'client_update': updates[email]}
        html_content = render_to_string(template_path, context)
        email_subject = f"{news_source} just posted about news about {keywords}"
        gmail_send_message(credentials, html_content, email_subject, email)


def update_admin(keywords_found, news_source):
    credentials = authenticate_gmail()
    body_text = f"New keywords found from {news_source}"
    email_subject = f"{len(keywords_found)} keywords found from {news_source}"
    gmail_send_message(credentials, body_text, email_subject, "kaleab@a2sv.org")


def create_updates(news_source, news_list):
    keywords_count = defaultdict(int)
    updates = defaultdict(lambda: defaultdict(list))
    keywords_queryset = Subscription.objects.values_list('keyword', flat=True).distinct()
    keywords_set = set(keywords_queryset)
    for news in news_list:
        seen = set()
        for word in news.title.split():
            word_lower = word.lower()
            # Check if each word is a keyword(and has subscribers)
            # TODO: Removing punctuations
            if word_lower in keywords_set:
                # To avoid multiple updates by the same keyword and from the same new source
                seen.add(word_lower)
                keywords_count[word_lower] += 1
                emails = Subscription.objects.get(keyword=word_lower).subscribers
                # Create an update for each email
                for email in emails:
                    updates[email][word_lower].append(news)

    if len(news_list) > 0:
        update_admin(keywords_count, news_source)
        update_subscribers(updates, news_source)
