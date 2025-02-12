import pickle
from address_book import AddressBook, Record
from commands_book import commands
debug = True

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
    
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            command, *args = parse_input(user_input)
        except ValueError:
            continue
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        # тут виконується ітерація по всіх командах, якщо існує тоді виконуємо її
        elif command in str(commands):
            for get_command in commands:
                if str(get_command) == command:
                    print(get_command.execute(args, book))
                    break
        elif command == "hello":
            print("How can I help you?")
        else:
            print("Invalid command.")
    save_data(book)
            
if __name__ == "__main__":
    main()