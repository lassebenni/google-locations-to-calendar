import logging
import pickle
from typing import Any, Dict

from dataclasses import dataclass, field
from googleapiclient.discovery import Resource, build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TIMEZONE_AMS = "Europe/Amsterdam"

# This is the main prefix used for logging
LOGGER_BASENAME = """locationsharinglib"""
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


@dataclass
class CalendarEvent:
    id: str = ""
    summary: str = ""
    description: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    start: Dict[str, str] = field(
        default_factory=lambda: {"date": "", "timeZone": TIMEZONE_AMS}
    )
    end: Dict[str, str] = field(
        default_factory=lambda: {"date": "", "timeZone": TIMEZONE_AMS}
    )
    body: Dict[str, Any] = field(default_factory=lambda: {})
    colorId: str = "1"

    def __post_init__(self):
        if self.start_date:
            self.start["date"] = self.start_date
        else:
            self.start_date = self.start["date"]

        if self.end_date:
            self.end["date"] = self.end_date
        else:
            self.end_date = self.end["date"]

    def to_dict(self):
        return {
            key: getattr(self, key)
            for key in ("summary", "description", "location", "start", "end", "colorId")
        }


class Calendar(object):
    """Wrapper for Google Calendar API"""

    service: Resource = None
    calendar_id: str = ""

    def __init__(self, calendar_id: str, auth_token: bytes):
        logger_name = u"{base}.{suffix}".format(
            base=LOGGER_BASENAME, suffix=self.__class__.__name__
        )
        self._logger = logging.getLogger(logger_name)
        self.service = self._authorize_using_token(auth_token)
        self.calendar_id = calendar_id

    def _authorize_using_token(self, token_bytes: bytes):
        creds = pickle.loads(token_bytes)
        service = build("calendar", "v3", credentials=creds)
        if not service:
            self._logger.info("Connecting to the Google Calendar service failed.")
            return None

        return service

    def list_events(
        self, query: str = "", min_datetime: str = "", max_datetime: str = ""
    ):
        result = []
        response = (
            self.service.events()
            .list(calendarId=self.calendar_id, q=query, timeMin=min_datetime)
            .execute()
        )

        for event in response["items"]:
            result.append(
                CalendarEvent(
                    id=event["id"],
                    location=event["location"],
                    summary=event["summary"],
                    start=event["start"],
                    end=event["end"],
                    body=event,
                )
            )

        return result

    def create_calendar_event(
        self,
        summary: str = "",
        description: str = "",
        location: str = "",
        start_date: str = "",
        end_date: str = "",
    ):
        return CalendarEvent(
            summary=summary,
            description=description,
            location=location,
            start_date=start_date,
            end_date=end_date,
        )

    def insert_calender_event(self, calendar_event: CalendarEvent):
        response = (
            self.service.events()
            .insert(calendarId=self.calendar_id, body=calendar_event.to_dict())
            .execute()
        )

        return response.get("htmlLink")

    def update_event(self, calendar_event: CalendarEvent):
        return (
            self.service.events()
            .update(
                eventId=calendar_event.id,
                body=calendar_event.body,
                calendarId=self.calendar_id,
            )
            .execute()
        )

    def delete_event(self, calendar_event: CalendarEvent):
        return (
            self.service.events()
            .delete(eventId=calendar_event.id, calendarId=self.calendar_id)
            .execute()
        )
