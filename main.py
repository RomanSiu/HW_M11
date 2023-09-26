from collections import UserDict
from datetime import datetime

def input_error(func):
    def Inner(*args):
        try:
            res = func(*args)
        except KeyError:
            print("Use valid contact!")
            exit()
        except ValueError:
            print("Write valid phone number")
            exit()
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
    def __init__(self, value = None):
        self._value = value
        
    def get_phone(self):
        return self._value

    def set_phone(self, new_value):
        if len(new_value) == 10 and new_value.isdigit():
            self._value = new_value
            pass
        else:
            print("Use valid phone format.")
            
    value = property(get_phone, set_phone)            
            
class Birthday(Field):
    def __init__(self, value = None):
        self._value = value
        
    def get_bday(self):
        return str(self._value.date())

    def set_bday(self, new_value):
        try:
            self._value = datetime.strptime(new_value, "%d.%m.%Y")
        except ValueError:
            print("Use birthday format dd.mm.yyyy!")
            exit()
            
    value = property(get_bday, set_bday)
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone = None, birthday = None):
        p = Phone()
        p.value = phone
        if p.value != None:
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
        p = Phone()
        p.value = new_phone
        self.phone = p
        if p.value != None:
            self.phones.pop(old_phone_indx)
            self.phones.insert(old_phone_indx, self.phone)
        
    def find_phone(self, phone):
        new_list = [p.value for p in self.phones]
        try:
            p_indx = new_list.index(phone)
        except ValueError:
            print("This contact doesn't have such a phone.")
            exit()
        return self.phones[p_indx]
    
    @input_error        
    def remove_phone(self, phone):
        new_list = [p.value for p in self.phones] 
        phone_indx = new_list.index(phone)
        self.phones.pop(phone_indx)

    def __str__(self):
        if self.birthday and self.phones:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        elif self.phones:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    @input_error    
    def find(self, name):
        for k in self.data.keys():
            if k == name:
                return self.data[k]
        print("There is no such contact in the address book")

    @input_error
    def delete(self, name):        
        self.data.pop(name)

    def iterator(self, n_on_page):
        list_notes = []
        for v in self.data.values():
            if v.birthday:
                new_v = f"Contact name: {v.name.value}, phones: {'; '.join(p.value for p in v.phones)}, birthday: {v.birthday.value}"
            else:
                new_v = f"Contact name: {v.name.value}, phones: {'; '.join(p.value for p in v.phones)}"
            list_notes.append(new_v) 
            if len(list_notes) == n_on_page:
                yield list_notes
                list_notes = []   
                
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890", "01.04.1998")
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
