import datetime

import dateutil.parser
from dateutil.tz import tzlocal
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleCalendarEvents:
    def __init__(self, credentials: Credentials):
        self._credentials = credentials
        self._service = build('calendar', 'v3', credentials=self.credentials)
        self._selected_calendars = []
        self._available_calendars = [calendar[0] for calendar in
                                     self.list_calendars()]
        self._all_events = []

    @property
    def credentials(self):
        return self._credentials

    @property
    def selected_calendars(self):
        return self._selected_calendars

    def select_calendar(self, calendar_id: str):
        if calendar_id in self._available_calendars:
            self._selected_calendars.append(calendar_id)

    def list_calendars(self, max_result: int = 100):
        """
        Get a list of calendars with id and summary
        :param max_result:
        :return: List of pairs. Each pair contains id and summary
        """
        try:
            calendar_results = self._service.calendarList().list(
                maxResults=max_result).execute()
            calendars = calendar_results.get('items', [])
            self._available_calendars = [(calendar['id'], calendar['summary'])
                                         for calendar in calendars]
        except Exception as exception:
            print(exception)
        return self._available_calendars

    def get_sorted_events(self, max_results=10):
        """
        Events are sorted in time in ascending order
        :param max_results: Max amount of events to return
        :return: List of pairs. Each pair contains date of the event and text
        """
        # TODO: Handle read timeout
        all_events = []
        # 'Z' indicates UTC time
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            for calendar_id in self._selected_calendars:
                events = self._service.events().list(
                    calendarId=calendar_id,
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy='startTime').execute()
                events = events.get('items', [])
                for event in events:
                    start_time = event['start'].get('dateTime',
                                                    event['start'].get('date'))
                    summary = event['summary']
                    time_parsed = dateutil.parser.parse(start_time)
                    if time_parsed.tzinfo is None:
                        time_parsed = time_parsed.replace(tzinfo=tzlocal())
                    all_events.append(
                        (time_parsed.astimezone(tzlocal()), summary))
            all_events.sort(key=lambda e: e[0])
            if len(all_events) > max_results:
                all_events = all_events[:max_results]
            self._all_events = all_events
        except Exception as exception:
            print(exception)
        return self._all_events
