from datetime import datetime, timedelta

import pytz
from googleapiclient.discovery import build
from model.authenticator import Authenticator


def get_event_list(option):
    time_min, time_max = get_time_ranges(option)
    auth = Authenticator()
    creds = auth.authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)
    print('Getting events from time_min to time_max')
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return events


def get_time_ranges(option):
    now = datetime.utcnow()
    if option == 'd':  # Today
        start_time = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.UTC)
        end_time = start_time + timedelta(days=1) - timedelta(seconds=1)
    elif option == 'w':  # This week
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.UTC)
        start_time = start_of_today - timedelta(days=start_of_today.weekday())
        end_time = start_time + timedelta(days=7) - timedelta(seconds=1)
    elif option == 'm':  # This month
        start_time = datetime(now.year, now.month, 1, 0, 0, 0, tzinfo=pytz.UTC)
        if now.month == 12:
            start_of_next_month = datetime(now.year + 1, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        else:
            start_of_next_month = datetime(now.year, now.month + 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        end_time = start_of_next_month - timedelta(seconds=1)
    else:
        raise ValueError("Invalid option. Please choose 'd' for today, 'w' for this week, or 'm' for this month.")

    return [start_time.isoformat(), end_time.isoformat()]
