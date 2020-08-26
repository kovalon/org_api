import uuid

from app import db
from sqlalchemy.dialects.postgresql import UUID


class Employee(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    surname = db.Column(db.String(20), index=True, nullable=False)
    name = db.Column(db.String(20), index=False, nullable=False)
    patronymic = db.Column(db.String(30), index=False, nullable=False)
    position = db.Column(db.String(30), index=True)
    number = db.Column(db.Integer, index=True, unique=True)

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if key == '_sa_instance_state':
                continue
            if type(value) == UUID:
                result[key] = str(value)
            result[key] = value
        return result

    def __repr__(self):
        return '<Employee {} {} {}>'.format(self.surname, self.name, self.patronymic)
