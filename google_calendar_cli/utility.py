from datetime import datetime, timedelta
import pytz


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
