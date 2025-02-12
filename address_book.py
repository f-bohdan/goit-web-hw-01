from collections import UserDict
from datetime import date, datetime
import upcoming_birthday

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
    

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Довжина номеру повинна = 10")

class Birthday(Field):
    def __init__(self, value):
        try: 
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        self.value = value
    
    def date(self):
        return datetime.strptime(self.value, "%d.%m.%Y").date()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу
    def add_phone(self, phone_str):
        if phone_str:
            self.phones.append(Phone(phone_str))

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def edit_phone(self, old_phone, new_phone):
        # перевірка чи введений номер телефону знаходиться в списку
        if old_phone not in [phone.value for phone in self.phones]:
            raise ValueError("Old phone not exist")
        else:
            # в іншому випадку проходимось по всіх елементах і змінюємо старий на новий
            self.phones = [phone if phone.value != old_phone else Phone(new_phone) for phone in self.phones]

    def find_phone(self, find_phone):
        # пошук 
        for phone in self.phones:
            if phone.value == find_phone:
                return phone
        return None

    def remove_phone(self, str_phone):
        # перевірка чи введений номер телефону знаходиться в списку
        if str_phone not in [phone.value for phone in self.phones]:
            raise ValueError("Phone not exist")
        else:
            self.phones.remove(self.find_phone(str_phone))
            
    def show_birthday(self):
        return f"Birthday date: {self.birthday}"

    def show_phones(self):
        return f"Phones: {'; '.join(p.value for p in self.phones)}"

    def __str__(self):
        return f"Contact name: {self.name.value}, \n\t\tPhones: {'; '.join(p.value for p in self.phones)}{f" \n\t\tBirthday Date: {self.birthday}" if self.birthday else ""}"

class AddressBook(UserDict):
    def add_record(self, record):
        # додаємо значення до власного списку
        self.data[record.name.value] = record

    def find(self, args):
        # пошук 
        if args in self.data:
            return self.data[args]

    def delete(self, name):
        # видалення
        del self.data[name]

    def __str__(self):
        # створюємо рядок для красивого виведення 
        returning = "--------- Address book ---------\n"
        for line in self.data.values():
            returning += f"{line}\n"
        returning += "--------------------------------"
        return returning
    
    def get_upcoming_birthdays(self, days = 7):
        upcoming_birthdays = []
        today = date.today()

        for contact in self.data.values():
            if not contact.birthday:
                continue
            birthday_this_year = contact.birthday.date().replace(year=today.year)
            if (birthday_this_year - today).days<-350:
                birthday_this_year = contact.birthday.date().replace(year=today.year+1)
            birthday_this_year = upcoming_birthday.adjust_for_weekend(birthday_this_year)
            
            if 0 <= (birthday_this_year - today).days <= days:
                congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                upcoming_birthdays.append({"name": contact.name.value, "birthday": congratulation_date_str})
        
        return upcoming_birthdays