import re
from datetime import datetime
from typing import Generic, TypeVar

from core.exceptions import ValidationError

T = TypeVar("T")


class Field(Generic[T]):
    """
    A generic field class to store a value of one type.

    The value is managed through getter and setter properties.

    For extra validation, subclasses can override the setter.
    """

    _value: T

    def __init__(self, value: T) -> None:
        self.value = value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        self._value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field[str]):
    """
    A field for storing a name.
    """

    pass


class Phone(Field[str]):
    """
    A field for storing a phone number.

    Validates that the phone number consists of exactly 10 digits.
    """

    @Field.value.setter
    def value(self, value: str) -> None:
        """
        Sets the phone number after validating its format.

        Args:
            value (str): The phone number to set (must be 10 digits).

        Raises:
            ValidationError: If the phone number is not exactly 10 digits.
        """
        if not re.fullmatch(r"^\d{10}$", value):
            raise ValidationError(
                f"Wrong phone number was passed {value}, expected format 10 digits: 0123456789"
            )
        self._value = value


class Birthday(Field[datetime]):
    """
    A field for storing a birthday date.

    Validates that the date is in the format DD.MM.YYYY.
    """

    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value: str) -> None:
        # We override Field.__init__ to accept a string instead of T type.
        self.value = value

    @Field.value.setter
    def value(self, value: str) -> None:
        """
        Sets the birthday date after validating its format.

        Args:
            value (str): The birthday date to set (format DD.MM.YYYY).

        Raises:
            ValidationError: If the date is not in the correct format.
        """

        try:
            self._value = datetime.strptime(value, Birthday.DATE_FORMAT)
        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime(Birthday.DATE_FORMAT)
