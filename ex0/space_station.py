from pydantic import BaseModel, Field  # type: ignore
from datetime import datetime
from typing import Optional
import json


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


def get_from_json(path: str) -> list:
    res = []
    try:
        with open(path) as file:
            res = json.load(file)
    except Exception as e:
        print(f"Type Error: {e.__class__.__name__}")
        print(f"Message Error: {e}")
    return res


def main() -> None:
    print("Space Station Data Validation")
    data = get_from_json("../generated_data/space_stations.json")
    station_space = create_data(data)
    print_data(station_space)
    wrong_data = get_from_json("../generated_data/invalid_stations.json")
    create_data(wrong_data)
    print("==================")


if __name__ == "__main__":
    main()
