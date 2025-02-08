#!/usr/bin/python
import sys
import csv
import random
from faker import Faker
from datetime import datetime
from dataclasses import dataclass, field, asdict


f = Faker()
f.seed_instance(1)

@dataclass
class Event:
    id: str
    channel: str = field(default_factory=lambda: random.choice(["web", "mobile"]))
    timestamp: str = field(
        default_factory=lambda: str(
            datetime.isoformat(
                f.date_time_between(
                    start_date=datetime.fromisoformat("2024-01-01T00:00:00"),
                    end_date=datetime.fromisoformat("2024-01-01T23:59:59"),
                )
            )
        )
    )
    ipaddress: str = field(default_factory=lambda: str(f.ipv4()))

    def as_dict(self):
        return asdict(self)

    @staticmethod
    def fieldnames():
        return Event(id="0").as_dict().keys()


if __name__ == '__main__':
    total_row = int(sys.argv[1])
    csv_file_path = f"datasets/random_data_{total_row}.csv"
    random_events = [Event(id=str(i)).as_dict() for i in range(1, total_row+1)]

    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=Event.fieldnames())
        writer.writeheader()
        writer.writerows(random_events)

    print(f"Random events saved into {csv_file_path}")
