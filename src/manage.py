import os
import jwt
import argparse
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from models import AccessToken, User
from cryptography.fernet import Fernet
from utils.database import Database

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv('SECRET_KEY')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')  # Generate using Fernet.generate_key() and store securely
cipher_suite = Fernet(ENCRYPTION_KEY)

session = Database().get_session()

def create_app_access_token(email: str):
    user = get_user(email)
    if user:
        data = {"email": email, "type": "app"}
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=10*365)  # 10 years expiry
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"Token: {encoded_jwt}")
        encrypted_jwt = encrypt_token(encoded_jwt)
        store_access_token(user.id, encrypted_jwt)
    else:
        print(f"Error: User doesn't exists")

def get_user(email: str):
    user = session.query(User).filter(User.email == email).first()
    return user

def encrypt_token(token: str) -> str:
    encrypted_token = cipher_suite.encrypt(token.encode('utf-8'))
    return encrypted_token.decode('utf-8')

def store_access_token(user_id, token):
    access_token = AccessToken(user_id=user_id, token=token)
    session.add(access_token)
    session.commit()
    print("Successfully")



def create_user(first_name, last_name, email, password):
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.password_hash = pwd_context.hash(password)

    session.add(user)
    session.commit()

    print(f"User {email} created successfully!")
    return user


def main():
    parser = argparse.ArgumentParser(description="Manage users and tokens")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    user_parser = subparsers.add_parser('create_user', help='Create a new user')
    user_parser.add_argument('first_name', type=str, help='First name of the user')
    user_parser.add_argument('last_name', type=str, help='Last name of the user')
    user_parser.add_argument('email', type=str, help='Email address of the user')
    user_parser.add_argument('password', type=str, help='Password for the user')

    token_parser = subparsers.add_parser('create_token', help='Create a new access token')
    token_parser.add_argument('email', type=str, help='Email address of the user to generate the token')

    args = parser.parse_args()

    if args.command == 'create_user':
        create_user(args.first_name, args.last_name, args.email, args.password)

    elif args.command == 'create_token':
        create_app_access_token(args.email)

    else:
        print("No valid command provided.")

if __name__ == "__main__":
    main()
