from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, is_creator):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_creator = is_creator
