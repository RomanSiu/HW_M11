from collections import UserDict
from datetime import datetime

def input_error(func):
    def Inner(*args):
        try:
            res = func(*args)
        except KeyError:
            print("Use valid contact!")
            exit
        except ValueError:
            print("Write valid phone number")
            exit
        else:
            return res
    return Inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self):
        self._value = None
        
    @property
    def value(self):
        return str(self._value)

    @value.setter
    def value(self, new_value):
        int(new_value)
        if len(new_value) == 10:
            self._value = new_value
        else:
            print("Use valid phone format.")

class Birthday(Field):
    def __init__(self):
        self._value = None
        
    @property
    def value(self):
        return str(self._value.date())

    @value.setter
    def value(self, new_value):
        try:
            self._value = datetime.strptime(new_value, "%d.%m.%Y")
        except ValueError:
            print("Use birthday format dd.mm.yyyy!")
            exit
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone, birthday = None):
        p = Phone()
        p.value = phone
        if p.value != "None":
            self.phone = p
            self.phones.append(self.phone)
        if birthday:
            b = Birthday()
            b.value = birthday
            self.birthday = b
            
    def days_to_birthday(self):
        today_date = datetime.now()
        contact_bd = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(year=today_date.year)
        if today_date.date() > contact_bd.date():
            res = contact_bd.replace(year=today_date.year + 1).date() - today_date.date()
        else:
            res = contact_bd.replace(year=today_date.year).date() - today_date.date()
        return f"{res.days} days until {self.name}'s birthday."
    
    @input_error    
    def edit_phone(self, old_phone, new_phone):
        new_list = [p.value for p in self.phones] 
        old_phone_indx = new_list.index(old_phone)
        new_list.remove(old_phone)
        _ = self.phones.pop(old_phone_indx)
        p = Phone()
        p.value = new_phone
        self.phone = p
        self.phones.insert(old_phone_indx, self.phone)
    
    @input_error    
    def find_phone(self, phone):
        new_list = [p.value for p in self.phones]
        p_indx = new_list.index(phone)
        return self.phones[p_indx]
    
    @input_error        
    def remove_phone(self, phone):
        new_list = [p.value for p in self.phones] 
        phone_indx = new_list.index(phone)
        _ = self.phones.pop(phone_indx)

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    @input_error    
    def find(self, name):
        for k in self.data.keys():
            if k == name:
                return self.data[k]
        print("There is no such contct in the address book")

    @input_error
    def delete(self, name):
        _ = self.data.pop(name)
        

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890", "23.09.2004")
john_record.add_phone("5555555555")

print(john_record.days_to_birthday())

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")