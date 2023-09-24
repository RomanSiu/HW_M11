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
            exit()
    
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
        p = Phone()
        p.value = new_phone
        self.phone = p
        if p.value != "None":
            self.phones.pop(old_phone_indx)
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
        self.phones.pop(phone_indx)

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
