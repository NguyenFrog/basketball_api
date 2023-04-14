import datetime
from jose import jwt
from passlib.context import CryptContext
password_object = CryptContext(schemes=["bcrypt"],default='bcrypt')
def hashed_password(password:str):
    temp = password[::-1]
    return password_object.hash(password+temp)

def verify_password(password:str, hashed_password:str):
    password_object.verify(password, hashed_password)

def generate_jwt(data: dict):
    payload = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes = 60*24)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, 'kjashuenfuehfewis34', algorithm='HS256')
    return encoded_jwt
    

    


    
    

