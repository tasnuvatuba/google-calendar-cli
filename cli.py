import datetime
from googleapiclient.discovery import build
from model.authenticator import Authenticator

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']


def list_events():
    auth = Authenticator(SCOPES)
    creds = auth.authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
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


if __name__ == '__main__':
    list_events()
