from enum import Enum
from pydantic_core import Url
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(Integer)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(60), nullable=False)
    job_title = Column(String(50), nullable=True)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    update_at = Column(DateTime, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.email}, hash: {self.password_hash[:10]}..."

 
class Organisation(Base):
    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)


class UserOrganisation(Base):
    __tablename__ = "user_organisation"

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    organisation_id = Column(Integer, ForeignKey('organisation.id', ondelete='CASCADE'), primary_key=True)
    join_date = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", backref=backref("organisations", cascade="all, delete"))
    organisation = relationship("Organisation", backref=backref("users", cascade="all, delete"))

    def __repr__(self):
        return f"user_id: {self.user_id}, organisation_id: {self.organisation_id}, join_date: {self.join_date}"


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    level = Column(Integer, nullable=False)
    url = Column(String(512), nullable=True)
    method = Column(String(32), nullable=True)
    process_time = Column(Float, nullable=True)
    response_code = Column(Integer, nullable=True)
    user = Column(String(255), nullable=True)
    body = Column(String(4096), nullable=True)
    
    def __repr__(self):
        return f'id: {self.id} create_at: {self.create_at} level: {self.level} url: {self.url} method: {self.method} response_code: {self.response_code} process_time: {self.process_time}'