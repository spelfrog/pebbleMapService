import json
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Any

import requests


@dataclass
class Slot:
    start: datetime
    end: datetime
    participants: int
    capacity: int

    def __init__(self, start: Union[int, datetime], end: Union[int, datetime], participants: int,
                 capacity: int) -> None:
        super().__init__()

        self.start = start if isinstance(start, datetime) else datetime.fromtimestamp(start)
        self.end = end if isinstance(end, datetime) else datetime.fromtimestamp(end)
        self.participants = participants
        self.capacity = capacity

    def __lt__(self, other):
        return self.start < other.start


class BookingAPI:
    MOZILLA_USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'

    @staticmethod
    def slots(start: datetime, end: datetime, course_id: int) -> list[Slot]:
        raise NotImplemented()

    @staticmethod
    def occupancy(start: datetime, end: datetime, course_id: int) -> list[Slot]:
        raise NotImplemented()


class Plano(BookingAPI):
    ENDPOINT = 'https://backend.dr-plano.com/courses_dates?'

    @staticmethod
    def data(start: datetime, end: datetime, course_id: int) -> Any:
        r = requests.get(Plano.ENDPOINT,
                         headers={'User-Agent': Plano.MOZILLA_USER_AGENT},
                         params={
                             'id': course_id,
                             'start': int(start.timestamp() * 1000),
                             'end': int(end.timestamp() * 1000)
                         })
        r.raise_for_status()
        return r.json()

    @staticmethod
    def fake_data(start: datetime, end: datetime, course_id: int, fallback_to_real_api=True):
        path = Path("tests/data/plano.raw.json")
        if not path.exists() and fallback_to_real_api:
            path.parent.mkdir(exist_ok=True)
            data = Plano.data(start, end, course_id)
            with open(path, "w") as file:
                json.dump(data, file)
            return data
        else:
            with open(path, "r") as file:
                return json.load(file)

    @staticmethod
    def slots(start: datetime, end: datetime, course_id: int) -> list[Slot]:
        return [
            Slot(
                start=slot['dateList'][0]['start'] / 1000,
                end=slot['dateList'][0]['end'] / 1000,
                participants=slot['currentCourseParticipantCount'],
                capacity=slot['maxCourseParticipantCount'])
            for slot in Plano.data(start, end, course_id)
        ]

    @staticmethod
    def occupancy(start: datetime, end: datetime, course_id: int) -> list[Slot]:
        slots = Plano.slots(start, end, course_id)
        segments = list(set([s.start for s in slots]).union([s.end for s in slots]))
        segments.sort()
        segments_occupancy = []

        for i, segment in enumerate(segments):
            if i + 1 == len(segments):
                break

            occupancy = Slot(segment, segments[i + 1], 0, 0)
            for slot in slots:
                if slot.start < occupancy.end and slot.end > occupancy.start:
                    occupancy.capacity += slot.capacity
                    occupancy.participants += slot.participants
            segments_occupancy.append(occupancy)
        return segments_occupancy
