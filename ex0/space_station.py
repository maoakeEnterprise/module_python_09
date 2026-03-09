from pydantic import BaseModel, Field  # type: ignore
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(gt=0, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(max_length=200)

    def print_info(self) -> None:
        print("========================================")
        print("Valid station created:")
        print(f"ID: {self.station_id}")
        print(f"Name: {self.name}")
        print(f"Crew: {self.crew_size} people")
        print(f"Power: {self.power_level}%")
        print(f"Oxygen: {self.oxygen_level}%")
        print(f"Status: {'Operational' if self.is_operational else 'Nope'}")
        print("\n========================================")


def create_data(data: list) -> list:
    tab = []
    try:
        for station in data:
            tab.append(SpaceStation(**station))
        return tab
    except Exception as e:
        print(f"Type Error {e.__class__.__name__}")
        print(f"Message Error: {e}")
    finally:
        return tab


def print_data(data: list[SpaceStation]):
    for station in data:
        station.print_info()


def main() -> None:
    data = [
        {
            'station_id': 'LGW125',
            'name': 'Titan Mining Outpost',
            'crew_size': 6,
            'power_level': 76.4,
            'oxygen_level': 95.5,
            'last_maintenance': '2023-07-11T00:00:00',
            'is_operational': True,
            'notes': None
        },
        {
            'station_id': 'QCH189',
            'name': 'Deep Space Observatory',
            'crew_size': 3,
            'power_level': 70.8,
            'oxygen_level': 88.1,
            'last_maintenance': '2023-08-24T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'ISS674',
            'name': 'Europa Research Station',
            'crew_size': 11,
            'power_level': 82.0,
            'oxygen_level': 91.4,
            'last_maintenance': '2023-10-21T00:00:00',
            'is_operational': True,
            'notes': None
        },
        {
            'station_id': 'ISS877',
            'name': 'Mars Orbital Platform',
            'crew_size': 9,
            'power_level': 79.7,
            'oxygen_level': 87.2,
            'last_maintenance': '2023-10-06T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'LGW194',
            'name': 'Deep Space Observatory',
            'crew_size': 21,
            'power_level': 80.2,
            'oxygen_level': 89.9,
            'last_maintenance': '2023-10-25T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'ISS847',
            'name': 'Solar Wind Monitor',
            'crew_size': 11,
            'power_level': 73.6,
            'oxygen_level': 98.1,
            'last_maintenance': '2023-12-11T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'QCH400',
            'name': 'Asteroid Belt Relay',
            'crew_size': 12,
            'power_level': 75.5,
            'oxygen_level': 86.0,
            'last_maintenance': '2023-07-15T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'ERS891',
            'name': 'Titan Mining Outpost',
            'crew_size': 4,
            'power_level': 94.4,
            'oxygen_level': 97.3,
            'last_maintenance': '2023-09-25T00:00:00',
            'is_operational': True,
            'notes': 'All systems nominal'
        },
        {
            'station_id': 'ABR266',
            'name': 'Asteroid Belt Relay',
            'crew_size': 8,
            'power_level': 76.0,
            'oxygen_level': 88.8,
            'last_maintenance': '2023-07-10T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        },
        {
            'station_id': 'LGW723',
            'name': 'Mars Orbital Platform',
            'crew_size': 11,
            'power_level': 90.8,
            'oxygen_level': 87.3,
            'last_maintenance': '2023-09-25T00:00:00',
            'is_operational': False,
            'notes': 'System diagnostics required'
        }
    ]
    print("Space Station Data Validation")
    station_space = create_data(data)
    print_data(station_space)


if __name__ == "__main__":
    main()
