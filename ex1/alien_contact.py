from enum import Enum
from datetime import datetime
from typing import Optional
import json
from pydantic import BaseModel, Field, model_validator  # type: ignore


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELE = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_id(self) -> None:
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id should start with AC")
        if not self.is_verified and self.contact_type == ContactType.PHYSICAL:
            raise ValueError("The contact should be verified")
        if self.witness_count < 3 and self.contact_type == ContactType.TELE:
            raise ValueError("You should have 3 witnesses at least")
        if self.signal_strength > 7 and not self.message_received:
            raise ValueError("When the signal is upper 7.0 "
                             "you should received a message")

    def print_info(self) -> None:
        print("======================================")
        print("Valid contact report:")
        print(f"ID: {self.contact_id}")
        print(f"Type: {self.contact_type}")
        print(f"Location: {self.location}")
        print(f"Signal: {self.signal_strength}/10")
        print(f"Duration: {self.duration_minutes} minutes")
        print(f"Witnesses: {self.witness_count}")
        print(f"Message: '{self.message_received}'")
        print("\n======================================")


def get_data_from_json(path: str) -> list:
    data = []
    try:
        with open(path) as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Type Error: {e.__class__.__name__}")
        print(f"Message Error: {e}")
    finally:
        return data


def create_contact(contacts: list) -> list:
    data = []
    for var in contacts:
        try:
            data.append(AlienContact(**var))
        except Exception as e:
            print(f"Type Error: {e.__class__.__name__}")
            print(f"Message Error: {e}")
    return data


def print_contats(contacts: list[AlienContact]) -> None:
    for contact in contacts:
        contact.print_info()


def print_json(data: list):
    print("""
=====================
START
=====================
""")
    for contact in data:
        for key, value in contact.items():
            print(f"{key} : {value}")
        print("=================")


def main() -> None:
    print("==============================")
    print("Alien Contact Log Validation")
    print("==============================")
    data = get_data_from_json("../generated_data/alien_contacts.json")
    contacts = create_contact(data)
    print_contats(contacts)


if __name__ == "__main__":
    main()
