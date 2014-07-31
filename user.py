from hashlib import sha256

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from db import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    email = Column(String)

    password = Column(String)

    def confirm_password(self, password):
        return self.password == password

    def confirm_token(self, token):
        return self.token == token

    @property
    def token(self):
        l = [self.password, str(self.id), self.email]
        h = '*'.join(l)
        return sha256(h.encode('utf-8')).hexdigest()
