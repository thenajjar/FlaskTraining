from src.configModule.create_app import db


class UsersDb(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    phone = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, name, username, email, password, phone, role):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.role = role

    def __repr__(self):
        return f"<User {self.user_id}>"
