from abc import ABC, abstractmethod
from address_book import Record


def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except Exception as exception:
            print(f"[INPUT_ERROR] {exception}")
            return ""
    return inner

# загальний приклад для створення команди
class ConsoleCommand(ABC):
    @input_error
    @abstractmethod
    def execute(self, args, book):
        pass

class GetAll(ConsoleCommand):
    # тут вказуємо назву команди
    def __repr__(self):
        return "all"
    # виконуємо команду
    def execute(self, args, book):
        if not args:
            return book
        else:
            raise Exception("Function 'all' don't receive any arguments")

class ShowPhone(ConsoleCommand):
    def __repr__(self):
        return "show"

    def execute(self, book, args):
        name, = args
        record = book.find(name)
        if record:
            return record.show_phones()
        else:
            return f"Contact '{name}' not in the list"
        
class ChangeContact(ConsoleCommand):
    def __repr__(self):
        return "change"
    
    def execute(self, args, book):
        name, old_phone, new_phone, *_ = args
        record = book.find(name)
        message = f"Contact '{name}' successfully changed {old_phone} = {new_phone}."
        if record:
            record.edit_phone(old_phone, new_phone)
        else:
            message = f"Contact '{name}' not in the list"
        return message

class AddContact(ConsoleCommand):
    def __repr__(self):
        return "add"
    def execute(self, args, book):        
        name, phone, *_ = args
        record = book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

class AddBirthday(ConsoleCommand):
    def __repr__(self):
        return "add-birthday"
    def execute(self, args, book):
        name, date, *_ = args
        record = book.find(name)
        message = f"Contact '{name}' successfully get birthday date: {date}."
        if record:
            record.add_birthday(date)
        else:
            message = f"Contact '{name}' not in the list"
        return message

class ShowBirthday(ConsoleCommand):
    def __repr__(self):
        return "birthday"
    def execute(self, args, book):
        name, = args
        record = book.find(name)
        if record:
            return record.show_birthday()
        else:
            return f"Contact '{name}' not in the list"

class Birthdays(ConsoleCommand):
    def __repr__(self):
        return "birthdays"
    def execute(self, args, book):
        days = None
        if args:
            days, = args
            return book.get_upcoming_birthdays(days)
        else:
            return book.get_upcoming_birthdays()

commands = [Birthdays(), ShowBirthday(), AddBirthday(), AddContact(), ShowPhone(), ChangeContact(), GetAll()]