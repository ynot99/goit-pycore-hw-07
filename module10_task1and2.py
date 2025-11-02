from contacts.address_book import AddressBook
from contacts.utils import add_faked_records
from contacts_assistance_bot.commands_manager import CommandsManager


def main():
    book = AddressBook()

    add_faked_records(book, 10)

    commands_manager = CommandsManager(book)
    commands_manager.loop_user_input()


if __name__ == "__main__":
    main()
