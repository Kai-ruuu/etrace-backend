from secrets import choice
from string import ascii_letters, digits
from passlib.context import CryptContext

from app.utils.env import envs

algorithm = envs("APP_ALGORITHM")
secret_key = envs("APP_SECRET_KEY")

safe_symbols = "!@#$%^&*-_=+?"

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str):
    return crypt_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)

def generate_password(length: int=8) -> str:
    return "".join(choice(ascii_letters + safe_symbols + digits) for _ in range(length))