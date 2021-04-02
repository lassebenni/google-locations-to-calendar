from __future__ import print_function
import datetime
import pickle
from googleapiclient.discovery import Resource, build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

TIMEZONE_AMS = "Europe/Amsterdam"
def authorize_using_token(token_bytes: bytes):
    creds = pickle.loads(token_bytes)
    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(service: Resource):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def insert_timeline_event(service: Resource):
    # 'yyyy-mm-dd' format
    today = datetime.datetime.today().strftime("%Y-%m-%d")

    event_body = {
        'summary': f'Timeline {today}. ',
        'location': f'{TIMELINE_LINK}{today}',
        'description': 'Timeline voor de dag.',
        'start': {
            'date': today,
            'timeZone': TIMEZONE_AMS,
        },
        'end': {
            'date': today,
            'timeZone': TIMEZONE_AMS,
        }
    }

    event = service.events().insert(
        calendarId=CAL_ID, body=event_body).execute()

    return event.get('htmlLink')
