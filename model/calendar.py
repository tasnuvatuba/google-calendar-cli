import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import SCOPES
from model.event import Event
from model.recurring_event import RecurringEvent
from utility import get_time_ranges


class Calendar:
    def __init__(self, scopes=None):
        self.scopes = scopes if scopes else SCOPES

    def authenticate_google_calendar(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_event_list(self, option):
        time_min, time_max = get_time_ranges(option)
        creds = self.authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        json_events = events_result.get('items', [])
        events = []
        for json_event in json_events:
            if "recurringEventId" in json_event:
                events.append(RecurringEvent.from_json(json_event))
            else:
                events.append(Event.from_json(json_event))
        return events

    def fetch_event_by_id(self, event_id):
        creds = self.authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)
        json_event = service.events().get(calendarId='primary', eventId=event_id).execute()
        print(json_event)
        if "recurringEventId" in json_event:
            event = (RecurringEvent.from_json(json_event))
        else:
            event = (Event.from_json(json_event))
        return event

    def add_event(self, event: Event):
        creds = self.authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)
        json_event = service.events().insert(calendarId='primary', body=event.to_json()).execute()
        return json_event

    def update_event(self, event):
        creds = self.authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)
        json_event = service.events().update(calendarId='primary', eventId=event.event_id, body=event.to_json()).execute()
        return json_event

    def add_attendees_to_event(self, event, attendees):
        creds = self.authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)
        new_attendees = []
        for attendee in event.attendees:
            new_attendees.append({'email': attendee})
        for attendee in attendees:
            new_attendees.append({'email': attendee})
        json_event = service.events().patch(calendarId='primary', eventId=event.event_id,
                                             body=new_attendees).execute()
        return json_event

