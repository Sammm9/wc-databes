from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_migrate import Migrate



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    major = db.relationship('Major', backref='users', lazy=True)
    academic_year = db.Column(db.Integer, nullable=False)
    classes = db.relationship('Class', backref='user', lazy=True)
    class_percent = db.Column(db.String(50), nullable=False)
    selected_options = db.Column(db.PickleType)

    @property
    def major_classes(self):
        return [mc.name for mc in self.major.major_classes]

    def __repr__(self):
        return f"User('{self.email}', '{self.first_name}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    major_classes = db.relationship('MajorClass', backref='major', lazy=True)

    def __repr__(self):
        return f"Major('{self.name}')"


class MajorClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)

    def __repr__(self):
        return f"MajorClass('{self.name}')"
    
class ClassPercentage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major_class_id = db.Column(db.Integer, db.ForeignKey('major_class.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    percent = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"ClassPercentage('{self.major_class_id}', '{self.user_id}', '{self.percent}')"


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Class {self.name}>'
    
class SelectedOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    option = db.Column(db.String)

    def __repr__(self):
        return f'<SelectedOption {self.option}>'