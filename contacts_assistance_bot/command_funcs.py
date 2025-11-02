from typing import Callable

from contacts.address_book import AddressBook, Record

type Args = list[str]
type Message = str
type CommandFunc = Callable[[Args, AddressBook], Message]


def hello(args: Args, book: AddressBook) -> Message:
    """
    Greets the user.
    """
    return "Hello! How can I assist you today?"


def add_contact(args: Args, book: AddressBook) -> Message:
    """
    Adds a new contact with a phone number.

    If the contact already exists, adds the phone number to the existing contact.
    """
    name, phone = args

    if not book.exists(name):
        new_record = Record(name)
        new_record.add_phone(phone)
        book.add_record(new_record)
        return "A new contact is added."

    existing_record = book.find(name)
    if existing_record.phone_exists(phone):
        return "The phone number already exists for this contact."

    existing_record.add_phone(phone)
    return "The phone is added to the specified contact."


def get_all(args: Args, book: AddressBook) -> Message:
    """
    Returns a string of all saved contacts.
    """
    return "\n".join(f"{record}" for _, record in book.items())


def show_phone(args: Args, book: AddressBook) -> Message:
    """
    Returns the all phone numbers of the specified contact.
    """
    (name,) = args

    if not book.exists(name):
        return "Contact not found."

    return book.find(name).phones_str


def change_contact(args: Args, book: AddressBook) -> Message:
    """
    Changes the phone number of an existing contact.
    """
    name, old_phone, new_phone = args[0], args[1], args[2]

    if not book.exists(name):
        return "Contact not found."

    existing_contact = book.find(name)

    if not existing_contact.phone_exists(old_phone):
        return "The old phone number was not found for this contact."

    if existing_contact.phone_exists(new_phone):
        return "The new phone number already exists for this contact."

    existing_contact.edit_phone(old_phone, new_phone)
    return f"The phone was updated from {old_phone} to {new_phone} for {name}."


def add_birthday(args: Args, book: AddressBook) -> Message:
    """
    Adds a birthday to a specified contact.
    """
    name, date = args[0], args[1]

    if not book.exists(name):
        return "Contact not found."

    record = book.find(name)
    record.add_birthday(date)
    return f"Birthday for {name} is added."


def show_birthday(args: Args, book: AddressBook) -> Message:
    """
    Shows the birthday of a specified contact.
    """
    name = args[0]

    if not book.exists(name):
        return "Contact not found."

    birthday = book.find(name).birthday_str

    if not birthday:
        return "Birthday is not set for this contact."

    return birthday


def birthdays(args: Args, book: AddressBook) -> Message:
    """
    Returns a list of contacts with upcoming birthdays.
    """
    upcoming_birthdays = book.get_upcoming_birthdays()

    if len(upcoming_birthdays) == 0:
        return "No upcoming birthdays found."

    return "\n".join(
        [
            f"{rec['name']}: birthday {rec['actual_date']}, congratulation {rec['congratulation_date']}"
            for rec in upcoming_birthdays
            if rec['congratulation_date']
        ]
    )
