import calendar
import datetime
from typing import List, Tuple


def get_month_str() -> str:
    return calendar.month_name[datetime.datetime.today().month]


def get_calendar_days() -> Tuple[List[int], Tuple[int, int]]:
    """
    Get calendar grid of dates as well as starting week index and weekday index
    """
    today = datetime.date.today()
    year = today.year
    month = today.month
    weekday_idx = (today.weekday() + 1) % 7

    # week start on Sunday
    calendar_lib = calendar.Calendar(firstweekday=6)
    weeks: List[List[datetime.date]] = calendar_lib.monthdatescalendar(
        year, month)
    week_idx: int = 0
    for week in weeks:
        if week[weekday_idx] == today:
            break
        week_idx += 1
    if week_idx >= 5:
        month += 1
        if month > 12:
            month = 1
            year += 1
        weeks = calendar_lib.monthdatescalendar(year, month)
        week_idx = 0
    if len(weeks) >= 5:
        weeks = weeks[:5]
    week_list: List[datetime.date] = sum(weeks, [])
    return list(map(lambda date: date.day, week_list)), (week_idx, weekday_idx)
