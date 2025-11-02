import colorama

from contacts.address_book import AddressBook
from contacts_assistance_bot.command_funcs import (
    CommandFunc,
    add_birthday,
    add_contact,
    birthdays,
    change_contact,
    get_all,
    hello,
    show_birthday,
    show_phone,
)
from core.exceptions import ValidationError

type CommandInfo = tuple[CommandFunc, list[str]]


class CommandsManager:
    def __init__(self, book: AddressBook) -> None:
        self.__book = book
        # TODO ensure that arguments described here match the actual command functions.
        # This over-engineer madness has to stop...
        self.__commands: dict[str, CommandInfo] = {
            "hello": (hello, []),
            "add": (add_contact, ["[name]", "[phone]"]),
            "change": (change_contact, ["[name]", "[old_phone]", "[new_phone]"]),
            "phone": (show_phone, ["[name]"]),
            "all": (get_all, []),
            "add-birthday": (add_birthday, ["[name]", "[date]"]),
            "show-birthday": (show_birthday, ["[name]"]),
            "birthdays": (birthdays, []),
        }

    def __parse_input(self, user_input: str):
        """
        Parses user input into a command and its arguments.
        """
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def __execute(self, command_name: str, args: list[str]) -> str:
        # Check if the command exists
        if command_name not in self.__commands:
            all_hints = "\n".join(
                f"\t{cmd} {hint}" for cmd, (_, hint) in self.__commands.items()
            )
            return (
                f"{colorama.Fore.RED}Invalid command.{colorama.Style.RESET_ALL}\n"
                "Available commands and usage:\n"
                f"{all_hints}\n\tclose\n\texit"
            )

        command_func, command_required_args = self.__commands[command_name]

        # See if the number of arguments is correct
        if len(args) != len(command_required_args):
            return (
                f"{colorama.Fore.RED}Invalid arguments.{colorama.Style.RESET_ALL}\n"
                f"Usage: {command_name} {' '.join(command_required_args)}"
            )

        try:
            return command_func(args, self.__book)
        except ValidationError as ve:
            return (
                f"{colorama.Fore.RED}Invalid argument: {ve}{colorama.Style.RESET_ALL}"
            )
        except:
            # In case of an unhandled error
            return f"{colorama.Fore.RED}An unexpected error occurred.{colorama.Style.RESET_ALL}"

    def loop_user_input(self):
        print("Welcome to the assistant bot!")
        while True:
            try:
                user_input = input(
                    f"{colorama.Fore.YELLOW}Enter a command: {colorama.Style.RESET_ALL}"
                )

                try:
                    command, *args = self.__parse_input(user_input)
                except ValueError:
                    print("Empty input. Please enter a command.")
                    continue

                if command in ["close", "exit"]:
                    print("Good bye!")
                    break

                print(self.__execute(command, args))
            except KeyboardInterrupt:
                print("\nexiting...")
                break
