from collections import UserDict
from datetime import datetime, timedelta
from typing import TypedDict

from contacts.fields import Birthday, Name, Phone


class UpcomingBirthday(TypedDict):
    name: str
    actual_date: str
    congratulation_date: str


class Record:
    """
    Represents a contact record containing a name and multiple phone numbers.
    """

    __name: Name
    __phones: list[Phone]
    __birthday: Birthday | None

    def __init__(self, name: str) -> None:
        self.__name = Name(name)
        self.__phones = []
        self.__birthday = None

    @property
    def name(self) -> str:
        return self.__name.value

    @property
    def phones_str(self) -> str:
        return "; ".join(phone.value for phone in self.__phones)

    @property
    def birthday_str(self) -> str | None:
        """
        Formatted birthday string or None if birthday is not set.
        """
        return str(self.__birthday) if self.__birthday else None

    def add_phone(self, phone: str) -> None:
        """
        Adds a new phone number to the list.

        Args:
            phone (str): The phone number to add.

        Raises:
            ValueError: If the phone number is invalid or already exists.
        """
        try:
            # Try to find an existing phone number
            self.find_phone(phone)
        except ValueError:
            # If the search failed - then add the new phone number
            self.__phones.append(Phone(phone))
            return

        # If the phone number already exists - raise an error
        raise ValueError(f"Phone number {phone} already exists")

    def remove_phone(self, phone: str) -> None:
        """
        Removes a phone number from the list.

        Args:
            phone (str): The phone number string to remove.

        Raises:
            ValueError: If the phone number is not found.
        """
        phone_to_remove = self.find_phone(phone)
        self.__phones.remove(phone_to_remove)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Replaces an existing phone number with a new one.

        Args:
            old_phone (str): The existing phone number to find.
            new_phone (str): The new valid phone number to set.

        Raises:
            ValueError: If the old_phone is not found or new_phone is invalid or already exists.
        """
        # Ensure the new phone does not already exist
        if self.phone_exists(new_phone):
            raise ValueError(f"Phone number {new_phone} already exists")

        old_phone_inst = self.find_phone(old_phone)
        old_phone_inst.value = new_phone

    def phone_exists(self, phone: str) -> bool:
        """
        Checks if a phone number exists in the record.

        Args:
            phone (str): The phone number to check.

        Returns:
            bool: True if the phone number exists, False otherwise.
        """
        try:
            self.find_phone(phone)
            return True
        except ValueError:
            return False

    def find_phone(self, phone: str) -> Phone:
        """
        Finds a Phone object by its number.

        Args:
            phone (str): The phone number to search for.

        Returns:
            Phone: The found Phone object.

        Raises:
            ValueError: If the phone number is not found in the list.
        """
        try:
            # We assume phone numbers are unique, therefore we return the first match.
            return next(
                (
                    iter_phone
                    for iter_phone in self.__phones
                    if iter_phone.value == phone
                )
            )
        except StopIteration:
            raise ValueError(f"Phone number {phone} was not found")

    def add_birthday(self, birthday: str) -> None:
        """
        Adds a birthday.

        Args:
            birthday (str): The valid birthday date.

        Raises:
            ValueError: If the birthday date is in an incorrect format.
        """
        self.__birthday = Birthday(birthday)

    def __str__(self) -> str:
        return (
            f"Contact name: {self.name}, "
            f"birthday: {self.birthday_str if self.birthday_str else 'not set'}, "
            f"phones: {'; '.join(p.value for p in self.__phones)}"
        )


class AddressBook(UserDict[str, Record]):
    """
    Represents an address book containing multiple records.
    """

    def add_record(self, record: Record) -> None:
        """
        Adds a new record to the address book.

        The record's name is used as the key.

        Args:
            record (Record): The record to add.
        """
        self.data[record.name] = record

    def find(self, name: str) -> Record:
        """
        Finds and returns a record by its name.

        Args:
            name (str): The name of the record to find.

        Returns:
            Record: The found Record object.

        Raises:
            KeyError: If no record with specified name is found.
        """
        return self.data[name]

    def exists(self, name: str) -> bool:
        """
        Checks if a record with the specified name exists in the address book.

        Args:
            name (str): The name of the record to check.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        return name in self.data

    def delete(self, name: str) -> None:
        """
        Deletes a record from the address book by its name.

        Args:
            name (str): The name of the record to delete.

        Raises:
            KeyError: If no record with that name is found.
        """
        del self.data[name]

    def get_upcoming_birthdays(self) -> list[UpcomingBirthday]:
        """
        Identify which users' birthdays occurring within the next 7 days,
        adjusting for weekends by moving celebrations to the following Monday.

        Returns:
            list[UpcomingBirthday]: A list of upcoming birthdays,
                where 'congratulation_date' is in the format "DD.MM.YYYY".
        """
        users = self.data.values()
        upcoming_birthdays: list[UpcomingBirthday] = []
        date_today = datetime.today().date()

        for user in users:
            birthday = user.birthday_str
            # Skip users without a birthday
            if not birthday:
                continue

            # Convert user's birthday to the current year, and assume that it is congratulation date
            congratulation_date = (
                datetime.strptime(birthday, Birthday.DATE_FORMAT)
                .replace(year=date_today.year)
                .date()
            )
            birthday_days_difference = (congratulation_date - date_today).days

            # Don't do anything if the birthday is not happening in the next 7 days
            if not (birthday_days_difference <= 7 and birthday_days_difference > -1):
                continue

            # Check if weekday is Saturday or Sunday
            if congratulation_date.weekday() > 4:
                # Transfer the congratulation day to the next Monday
                congratulation_date = congratulation_date + timedelta(
                    days=7 - congratulation_date.weekday()
                )

            upcoming_birthdays.append(
                {
                    "name": user.name,
                    "actual_date": birthday,
                    "congratulation_date": congratulation_date.strftime(
                        Birthday.DATE_FORMAT
                    ),
                }
            )

        return upcoming_birthdays
