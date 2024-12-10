from fastapi import HTTPException
from utils.database import Database

session = Database().get_session()

def say_hello():
    return "Hello"
