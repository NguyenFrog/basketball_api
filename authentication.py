import datetime
from fastapi import Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pymongo

from user_model import User
password_object = CryptContext(schemes=["bcrypt"],default='bcrypt')
auth = OAuth2PasswordBearer(tokenUrl="token")
client = pymongo.MongoClient( "mongodb+srv://tuanpluss02:Tuan2002@stormx.kretsz3.mongodb.net/?retryWrites=true&w=majority")  # ket noi den mongoDB
db = client['Basketball']


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

def authenticate_user(token: str = Depends(auth)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid Token")
    try:
        payload = jwt.decode(
            token, 'asfdsfgdsfasfweqweweq213123sad21edf23edaaqw21w', algorithms=['HS256'])
        username = payload.get("username")
        username = str(username)
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        user = get_user_from_mongo(username)
        return user.is_admin
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")


def get_user_from_mongo(username: str):
    user_collection = db.users
    response = user_collection.find_one({"username": username})
    if response is None:
        raise HTTPException(status_code=401, detail="Invalid Token")
    data = response.copy()
    data['_id'] = str(data['_id'])
    user = User(**data)
    return user
    
def verify_user(username: str, password: str) -> User:
    user_collection = db.users
    response = user_collection.find_one({"username": username})
    if response is None:
        raise HTTPException(
            status_code=401, detail="Username or password is incorrect")
    print(response)
    data = response.copy()
    data['_id'] = str(data['_id'])
    user = User(**data)
    print(user)
    if not verify_password(password + password[::-1], user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Username or password is incorrect")
    return user

    


    
    

