import json
from typing import Union
import pymongo
from fastapi import Depends, FastAPI, HTTPException, status
from bson import ObjectId, json_util
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authentication import authenticate_user, verify_password, generate_access_token, generate_password_hash
from user_model import User
client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")# kết nối với pymongo
db = client["basketball"] # tạo database

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



# @app.on_event("startup")
# def tao_database():
#     try:
#         # user = db.create_collection("members")#tạo ra 1 collection
#         # db.members.insert_one({'ten': "Nguyen", 'tuoi': 20})#tạo ra 1 document
#         db.create_collection("users")
#         print("da ket noi")
#     except:
#         print("khong the ket noi")

@app.post("/add")
def add_new_user(name:str, birth:str, gender:bool, weight:float, height:float, level:str):
    try:
        db.members.insert_one({'name': name, 'birth': birth, 'gender': gender, 'weight': weight, 'height': height, 'level':level})
    except:
        raise HTTPException(status_code=400, detail="error")
    return {"OK": "thanh cong"}

@app.get("/get_one")
def get_one(name:str):
    try:
        user = db.members.find_one({'name':name})
        if user is None:
            raise HTTPException(status_code=400, detail="khong tim thay ten")
    except:
        raise HTTPException(status_code=400, detail="khong tim thay ten")
    return {
        "id":str(user['_id']),
        "name":user['name'],
        "birth":user['birth'],
        "gender":user['gender'],
        "weight":user['weight'],
        "height":user['height'],
        "level":user['level'],
        }

# @app.get("/get_many")
# def get_many(name:str, gender:bool, birth:str):
#     try:
#         users = db.members.find({'name':name, 'gender':gender, 'birth':birth})
#         if users is None:
#           raise HTTPException(status_code=400, detail="khong tim thay thong tin")
#         print(users)
#         res=json.dumps(list(users),default=str)
#         return res 
#     except:
#         raise HTTPException(status_code=400, detail="sai thong tin")

@app.delete("/delete")
def delete(name:str, is_admin = Depends(authenticate_user)):
    if is_admin is False:
        raise HTTPException(status_code=403, detail = "Forbidden")
    try: 
        user = db.members.find_one({'name':name})
        if user is None:
            raise HTTPException(status_code=400, detail="khong tim thay ten")
        db.members.delete_one({"_id":user['_id']})
    except:
        raise HTTPException(status_code=400, detail="sai thong tin")
    return {"Da xoa thong tin thanh vien"}
     
@app.get("/get_all")
def get_all():
    try:
        users=db.members.find({})
    except:
        raise HTTPException(status_code=400, detail="error")
    res=json.dumps(list(users),default=json_util.default)
    return res 
    
@app.put("/update")
def update(_id:str, name:str, birth:str, gender:bool, weight:float, height:float, level:str, is_admin = Depends(authenticate_user)):
      try:
        db.members.update_one({'_id':ObjectId(_id)}, {'$set':{'name': name, 'birth': birth, 'gender': gender, 'weight': weight, 'height': height, 'level':level}})       
      except:
          raise HTTPException(status_code=400, detail="error")
      return {"update thanh cong"}


@app.post("/register")
def register(username:str, password:str, is_admin:bool):
    try:
        user_collection = db.users
        check= user_collection.find_one({'username':username})
        if check is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="tai khoan da ton tai")
        hashedpassword = generate_password_hash(password + password[::-1])
        print(hashedpassword)
        user_collection.insert_one({
            "username":username,
            "hashed_password": hashedpassword,
            "is_admin": is_admin
        })
        jwt_token = generate_access_token({'username':username, 'is_admin':is_admin})
        return {"jwt_token":jwt_token}
    except:
        raise HTTPException(status_code=400, detail="khong the tao tai khoan")

    
@app.post("/login")
def login(username:str, password:str):
    try:
        user_collection = db.users
        check = user_collection.find_one({'username':username})
        if check is None:
            raise HTTPException(status_code=400, detail= "tai khoan khong ton tai")
        hashed_password = check['hashed_password']
        temp = password[::-1]
        check_login = verify_password(password + temp, hashed_password)
        if check_login is False:
            raise HTTPException(status_code=400, detail="sai mat khau")
        jwt_token = generate_access_token({'username':username, 'is_admin':check['is_admin']})
        return {"phan hoi":"dang nhap thanh cong", "jwt_token":jwt_token}
    except:
        raise HTTPException(status_code=400, detail="login error")


@app.post("/token")
def token(dataform:  OAuth2PasswordRequestForm = Depends()):
    try:
        user_collection = db.users
        response = user_collection.find_one({"username": dataform.username})
        if response is None:
           raise HTTPException(status_code=401, detail="Username or password is incorrect")
        if not verify_password(dataform.password + dataform.password[::-1], response['hashed_password']):
            raise HTTPException(status_code=401, detail="Username or password is incorrect")
        data = response.copy()
        data['_id'] = str(data['_id'])
        user = User(**data)
        jwt_token = generate_access_token({"username": user.username, "is_admin": user.is_admin})
    except:
         raise HTTPException(status_code=400, detail="Wrong username or password")
    return {"message": "login success", "access_token": jwt_token}

        

        

    

    

        


    
    

        


