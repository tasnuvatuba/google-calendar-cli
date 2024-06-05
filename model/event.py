from googleapiclient.discovery import build
from typing import List, Optional
from model.authenticator import Authenticator


class Event:
    def __init__(self, title, start_time, end_time, description=None, location=None,
                 daylong=False, attendees: Optional[List[str]] = None):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location
        self.daylong = daylong
        self.attendees = attendees if attendees else []

    def add_attendee(self, attendee: str):
        if attendee not in self.attendees:
            self.attendees.append(attendee)

    def remove_attendee(self, attendee: str):
        if attendee in self.attendees:
            self.attendees.remove(attendee)

    def to_json(self):
        event = {
            "summary": self.title,
            "description": self.description,
            "location": self.location,
            "start": {
                "dateTime": self.start_time.isoformat() if not self.daylong else None,
                "date": self.start_time.date().isoformat() if self.daylong else None,
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": self.end_time.isoformat() if not self.daylong else None,
                "date": self.end_time.date().isoformat() if self.daylong else None,
                "timeZone": "UTC"
            },
            "attendees": [{"email": attendee} for attendee in self.attendees]
        }

        if self.daylong:
            del event["start"]["dateTime"]
            del event["end"]["dateTime"]
        else:
            del event["start"]["date"]
            del event["end"]["date"]

        return event

    def add_event(self):
        auth = Authenticator()
        creds = auth.authenticate_google_calendar()
        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=self.to_json()).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    def __str__(self):
        attendees_str = ", ".join(self.attendees)
        event_details = (f"Event: {self.title}\n"
                         f"Description: {self.description}\n"
                         f"Location: {self.location}\n"
                         f"Attendees: {attendees_str}")
        if self.daylong:
            event_details += "\nThis is a day-long event"

        event_details += (f"\nStart: {self.start_time}\n"
                          f"End: {self.end_time}")
        return event_details
