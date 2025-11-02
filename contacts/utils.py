from random import randint

from faker import Faker

from contacts.address_book import AddressBook, Record
from contacts.fields import Birthday


def add_faked_records(book: AddressBook, count: int):
    faker = Faker()

    for _ in range(count):
        rec = Record(faker.first_name())
        rec.add_phone(faker.numerify("##########"))
        if randint(0, 1):
            rec.add_birthday(faker.date(Birthday.DATE_FORMAT))
        book.add_record(rec)
