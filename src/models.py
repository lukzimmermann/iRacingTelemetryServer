from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(60), nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    update_at = Column(DateTime, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)

    friendships = relationship(
        "Friendship",
        primaryjoin="or_(User.id == Friendship.user_id, User.id == Friendship.friend_id)",
        backref="user"
    )

    def __repr__(self):
        return f"id: {self.id}, name: {self.email}, hash: {self.password_hash[:10]}..."
 
class Friendship(Base):
    __tablename__ = "friendship"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    confirmed = Column(Boolean, default=False, nullable=False)  # Indicates if the friendship is mutual/confirmed

    def __repr__(self):
        return f"Friendship(id: {self.id}, user_id: {self.user_id}, friend_id: {self.friend_id}, confirmed: {self.confirmed})"

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
    

class AccessToken(Base):
    __tablename__ = "access_token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    token = Column(String(500), nullable=False)
    
    def __repr__(self):
        return f'user_id: {self.user_id} create_at: {self.create_at}'