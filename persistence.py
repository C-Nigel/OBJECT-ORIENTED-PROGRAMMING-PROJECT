import shelve
import uuid
import re

class User:
    def __init__(self, tag):
        self.__tag = tag
        self.__email = ''
        self.__Cname = ''
        self.__password = ''
        self.__contact = ''

    def get_tag(self):
        return self.__tag

    def get_email(self):
        return self.__email

    def get_Cname(self):
        return self.__Cname

    def get_password(self):
        return self.__password

    def get_contact(self):
        return self.__contact

    def set_email(self, email):
        self.__email = email

    def set_Cname(self, Cname):
        self.__Cname = Cname

    def set_password(self, password):
        self.__password = password

    def set_contact(self, contact):
        self.__contact = contact

users = shelve.open('user')

# Signup part
def create_user(email, Cname, password, contact):
    tag = str(uuid.uuid4())
    user = User(tag)
    user.set_email(email)
    user.set_Cname(Cname)
    user.set_password(password)
    user.set_contact(contact)
    users[tag] = user

# Login part
def get_user(email, password):
    klist = list(users.keys())
    for key in klist:
        user = users[key]
        print(user.get_email(), email, user.get_password(), password)
        if user.get_email() == email and user.get_password() == password:
            return user
    return None

# Update profile
def update_user(tag, user):
    users[tag] = user
    return users[tag]

# Admin clear user
def clear_user():
    klist = list(users.keys())
    for key in klist:
        del users[key]

# Admin add user?
def add_user(user):
    users[user.get_tag()] = user

# Clear user [ for admin, for now don't need ]
# def init_db():
#    clear_user()
#    for i in range(5):
#        create_user('user'+str(i), 'pass'+str(i))


u1 = User('xxx1')
u1.tag = 'xxx1'
u1.email = 'nihaoma@gmail.com'
u1.name = 'John'
u1.password = 'pass'
u1.contact = '9999'

# add to persistence
users[u1.email] = u1
users[u1.tag] = u1

# retrieve given the tag, xxx1
user = users['xxx1']

# update values
user.name = 'Mary'
users[user.tag] = u1

# delete
if user.tag in users:
    del users[user.tag]

