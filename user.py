from hashlib import sha256

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String

from db import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    email = Column(String, nullable=False)

    password = Column(String, nullable=False)

    def confirm_password(self, password):
        return self.password == password


    @property
    def token(self):
        a = [self.email, self.email]
        return sha256('+'.join(a).encode('utf-8')).hexdigest()

    def confirm_token(self, t):
        return self.token == t
