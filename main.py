import json
from typing import Union
import pymongo
from fastapi import FastAPI, HTTPException
from bson import ObjectId, json_util


from authentication import generate_jwt, hashed_password

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



# @app.on_event("startup")
# def tao_database():
#     try:
#         client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")#kết nối với pymongo
#         db = client["basketball"]#tạo database
#         # user = db.create_collection("members")#tạo ra 1 collection
#         # db.members.insert_one({'ten': "Nguyen", 'tuoi': 20})#tạo ra 1 document
#         db.create_collection("users")
#         print("da ket noi")
#     except:
#         print("khong the ket noi")

@app.post("/add")
def add_new_user(name:str, birth:str, gender:bool, weight:float, height:float, level:str):
    try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        db.members.insert_one({'name': name, 'birth': birth, 'gender': gender, 'weight': weight, 'height': height, 'level':level})
    except:
        raise HTTPException(status_code=400, detail="error")
    return {"OK": "thanh cong"}

@app.get("/get_one")
def get_one(name:str):
    try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
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
#         client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
#         db = client["basketball"]
#         users = db.members.find({'name':name, 'gender':gender, 'birth':birth})
#         if users is None:
#           raise HTTPException(status_code=400, detail="khong tim thay thong tin")
#         print(users)
#         res=json.dumps(list(users),default=str)
#         return res 
#     except:
#         raise HTTPException(status_code=400, detail="sai thong tin")

@app.delete("/delete")
def delete(name:str):
    try: 
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
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
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        users=db.members.find({})
    except:
        raise HTTPException(status_code=400, detail="error")
    res=json.dumps(list(users),default=json_util.default)
    return res 
    
@app.put("/update")
def update(_id:str, name:str, birth:str, gender:bool, weight:float, height:float, level:str):
      try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        db.members.update_one({'_id':ObjectId(_id)}, {'$set':{'name': name, 'birth': birth, 'gender': gender, 'weight': weight, 'height': height, 'level':level}})       
      except:
          raise HTTPException(status_code=400, detail="error")
      return {"update thanh cong"}
    
@app.post("/register")
def register(username:str, password:str, is_admin:bool):
    hashedpassword = hashed_password(password)
    try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        user_collection = db.users
        check= user_collection.find_one({'username':username})
        if check is not None:
            raise HTTPException(status_code=400, detail="error")
        user_collection.insert_one({
            "username":username,
            "hashed_password": hashedpassword,
            "is_admin": is_admin
        })
        jwt_token = generate_jwt({'username':username, 'is_admin':is_admin})
        return {"jwt_token":jwt_token}
    except:
        raise HTTPException(status_code=400, detail="khong the tao tai khoan")
    

    

    

        


    
    

        


