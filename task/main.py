from pathlib import Path
from model.addressBook import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            if len(args) > 0:
                return err.args[0]
            else:
                return err.__doc__
        except KeyError:
            return "Contact does not exist."
        except IndexError:
            return "Arguments are required."

    return inner


def get_contact_filepath():
    datapath = Path("./data/contacts.dat")
    if not datapath.exists():
        with open(datapath, "wb+"):
            return datapath

    return datapath


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("invalid params. The correct is: add ContactName PhoneNumber")

    name, *phones = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    for phone in phones:
        record.add_phone(phone)

    return message


@input_error
def add_phone(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError(
            "invalid params. The correct is: addphone ContactName PhoneNumber"
        )

    name, phone = args
    record: Record = book.find(name)
    if record == None:
        raise ValueError(f"Contact name {name} is not found.")
    record.add_phone(phone)
    return "Phone added."


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError(
            "invalid params. The correct is: add-birthday ContactName PhoneNumber"
        )

    name, birthday = args
    record: Record = book.find(name)
    if record == None:
        raise ValueError(f"Contact name {name} is not found.")
    record.add_birthday(birthday)
    return "Birhday added."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: show-birthday ContactName")
    name = args[0]

    record = book.find(name)
    if record == None:
        raise ValueError(f"Contact name {name} is not found.")
    return record.birthday


@input_error
def remove_phone(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError(
            "invalid params. The correct is: removephone ContactName PhoneNumber"
        )

    name, phone = args
    record: Record = book.find(name)
    if record == None:
        raise ValueError(f"Contact name {name} is not found.")
    record.remove_phone(phone)
    return "Phone removed."


@input_error
def update_phone(args, book: AddressBook):
    if len(args) != 3:
        raise ValueError(
            "invalid params. The correct is: updatephone ContactName oldphone newphone"
        )

    name, oldphone, newphone = args
    record: Record = book.find(name)
    if record == None:
        raise ValueError(f"Contact name {name} is not found.")
    record.edit_phone(oldphone, newphone)
    return "Phone updated."


@input_error
def remove_contact(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: remove ContactName")

    name = args[0]
    book.delete(name)
    return "Contact removed."


@input_error
def show_contacts(book):
    book.print()


def get_allowed_commands():
    return [
        "close",
        "exit",
        "add",
        "remove",
        "all",
        "phone",
        "addphone",
        "removephone",
        "updatephone",
        "add-birthday",
        "show-birthday",
        "findbyphone",
        "findbyname",
        "birthdays",
    ]


@input_error
def get_phones(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: phone ContactName")
    name = args[0]

    record = book.find(name)
    if record == None:
        raise ValueError(f"Contact name {name} is not found.")
    return f"{'; '.join(p.value for p in record.phones)}"


@input_error
def find_contacts(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: findbyphone phone")
    phone = args[0]

    records = book.find_record_by_phone(phone)
    for rec in records:
        print(rec)


@input_error
def find_bypattern(args, book: AddressBook):
    if len(args) != 1:
        raise ValueError("invalid params. The correct is: findbyname namepart")
    name = args[0]

    records = book.find_record_by_name(name)
    for rec in records:
        print(rec)


def main():
    print("Welcome to the assistant bot!")
    # get_contact_filepath()
    book = AddressBook(get_contact_filepath())
    # book.filepath =
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        match command:
            case "close":
                print("Good bye!")
                book.save_to_file()
                break
            case "exit":
                print("Good bye!")
                book.save_to_file()
                break
            case "add":
                print(add_contact(args, book))
            case "remove":
                print(remove_contact(args, book))
            case "all":
                show_contacts(book)
            case "phone":
                print(get_phones(args, book))
            case "addphone":
                print(add_phone(args, book))
            case "removephone":
                print(remove_phone(args, book))
            case "updatephone":
                print(update_phone(args, book))
            case "findbyphone":
                find_contacts(args, book)
            case "findbyname":
                find_bypattern(args, book)
            case "birthdays":
                print(*book.get_birthdays(), sep="\n")
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print
            case "help":
                print("Allowed commands:")
                print(get_allowed_commands())
            case "hello":
                print("Welcome to the assistant bot!")
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
