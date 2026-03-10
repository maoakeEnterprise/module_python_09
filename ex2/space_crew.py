from enum import Enum
from pydantic import BaseModel, Field, model_validator  # type: ignore
from datetime import datetime
import json


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUT = "lieutenant"
    CAPT = "captain"
    COMMAN = "commander"


class CrewError(Exception):
    def __init__(self, mess) -> None:
        super().__init__(f"CrewError: {mess}")


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True

    def print_info(self) -> None:
        print(f"- {self.name} ({self.rank.value}) - {self.specialization}")


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=1365)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1, le=10000)

    @model_validator(mode="after")
    def check_after(self):
        if not self.mission_id.startswith("M"):
            raise NameError("The mission ID should start with a M")
        crew = [member for member in self.crew
                if member.rank in [Rank.CAPT, Rank.COMMAN]]
        if crew == []:
            raise CrewError("You should get in the crew at least "
                            "one captain or one commander")
        crew = [member for member in self.crew if member.years_experience >= 5]
        res = float(len(crew) / len(self.crew))
        if res < 0.5 and self.duration_days > 365:
            raise CrewError("You should get at least 50%"
                            " of your crew with 5 years experiences")
        crew = [member for member in self.crew if not member.is_active]
        if crew != []:
            raise CrewError("Every member should be active")
        return self

    def print_info(self) -> None:
        print("=========================================")
        print("Valid mission created:")
        print(f"Mission: {self.mission_name}")
        print(f"ID: {self.mission_id}")
        print(f"Destination: {self.destination}")
        print(f"Duration: {self.duration_days} days")
        print(f"Budget: ${self.budget_millions}M")
        print(f"Crew size: {len(self.crew)}")
        print("Crew members:")
        for member in self.crew:
            member.print_info()
        print("\n=========================================")


def create_crew(crew: list) -> list[CrewMember]:
    res: list[CrewMember] = []
    for member in crew:
        try:
            res.append(CrewMember(**member))
        except Exception as e:
            print(f"Type Error: {e.__class__.__name__}")
            print(f"Message : {e}")
    return res


def get_from_json(path: str):
    res = []
    try:
        with open(path, "r") as file:
            res = json.load(file)
            for var in res:
                var["crew"] = create_crew(var["crew"])
    except Exception as e:
        print(f"Type Error: {e.__class__.__name__}")
        print(f"Message Error: {e}")
    return res


def print_missions(missions: list[SpaceMission]) -> None:
    for mission in missions:
        mission.print_info()


def create_space_Mission(missions: list) -> list[SpaceMission]:
    res: list[SpaceMission] = []
    for mission in missions:
        try:
            res.append(
                SpaceMission(**mission)
            )
        except Exception as e:
            print(f"Type Error: {e.__class__.__name__}")
            print(f"Message : {e}")
    return res


def main() -> None:
    print("==============================")
    print("Space Mission Crew Validation")
    data = get_from_json("../generated_data/space_missions.json")
    missions = create_space_Mission(data)
    print_missions(missions)
    wrong_data = get_from_json("../generated_data/invalid_missions.json")
    create_space_Mission(wrong_data)


if __name__ == "__main__":
    main()
