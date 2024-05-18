from collections import UserList
from datetime import datetime
from datetime import date
from model.helpers import DateHelper
import pickle
import re
from pathlib import Path


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.value = name

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, phone):
        self.setphone(phone)

    def __str__(self):
        return str(self.value)

    def setphone(self, phone):
        if not re.match(r"^\d{10}$", phone):
            raise ValueError("phone must be in XXXXXXXXXX format")
        self.value = phone


class Birthday(Field):
    def __init__(self, value):
        try:
            if type(value) is str:
                self.value = datetime.strptime(value, "%d.%m.%Y").date()
            if type(value) is datetime:
                self.value = value.date()
            if type(value) is date:
                self.value = value

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if type(phone) is Phone:
            self.phones.append(phone)
        else:
            if len(list(filter(lambda x: x.value == phone, self.phones))) > 0:
                return
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phones = list(filter(lambda x: x.value == phone, self.phones))
        if len(phones) == 0:
            raise ValueError(f"Phone number {phone} is not found.")
        self.phones = list(filter(lambda x: x.value != phone, self.phones))

    def edit_phone(self, oldphone, newphone):
        phones = list(filter(lambda x: x.value == oldphone, self.phones))
        if len(phones) == 0:
            raise ValueError(f"Phone number {oldphone} is not found.")
        phones[0].setphone(newphone)

    def find_phone(self, phone):
        phones = list(filter(lambda x: x.value == phone, self.phones))
        if len(phones) == 0:
            raise ValueError(f"Phone number {phone} is not found.")
        return phones[0]

    def add_birthday(self, value):
        if value != None:
            self.birthday = Birthday(value)
        else:
            self.birthday = value

    def __str__(self):
        if self.birthday == None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, birthday: {self.birthday.value.strftime('%d.%m.%Y')}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserList):
    def __init__(self, filepath=None):
        self.data = []
        self.filepath = filepath
        if self.filepath != None:
            self.load_from_file()

    def add_record(self, record):
        if (
            len(list(filter(lambda x: x.name.value == record.name.value, self.data)))
            > 0
        ):
            raise ValueError(f"Contact name {record.name.value} already exist.")
        self.append(record)

    def delete(self, contactname):
        self.data = list(filter(lambda x: x.name.value != contactname, self.data))

    def find(self, contactname):
        foundlist = list(filter(lambda x: x.name.value == contactname, self.data))
        if len(foundlist) == 0:
            return None

        return foundlist[0]

    def load_from_file(self):
        with open(self.filepath, "rb") as file:
            try:
                self.data = pickle.load(file)
            except EOFError:
                self.data = []

    def save_to_file(self):
        if self.filepath == None:
            return
        with open(self.filepath, "wb") as file:
            pickle.dump(self.data, file)

    def find_record_by_name(self, name: str):
        foundlist = list(filter(lambda x: x.name.value.__contains__(name), self.data))
        return foundlist

    def find_record_by_phone(self, phone: str):
        foundlist = list(
            filter(
                lambda x: len(list(filter(lambda y: y.value == phone, x.phones))) != 0,
                self.data,
            )
        )
        return foundlist

    def print(self):
        for rec in self.data:
            print(rec)

    def get_upcoming_birthdays(self):
        today = date.today()
        upcomming_contacts_bday = []
        for contact in list(filter(lambda x: x.birthday != None, self.data)):
            next_contact_birthday = DateHelper.get_next_birthday(
                contact.birthday.value, today
            )

            diffcoef = (next_contact_birthday - today).days
            if diffcoef in range(0, 7):
                upcomming_contacts_bday.append(
                    f"Contact name: {contact.name.value}, congratulation date: {DateHelper.get_formated_workday(next_contact_birthday)}"
                )

        return upcomming_contacts_bday
