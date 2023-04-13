import json
from typing import Union
import pymongo
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# @app.on_event("startup")
# def tao_database():
#     try:
#         client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")#kết nối với pymongo
#         db = client["basketball"]#tạo database
#         # user = db.create_collection("members")#tạo ra 1 collection
#         db.members.insert_one({'ten': "Nguyen", 'tuoi': 20})#tạo ra 1 document
#         print("da ket noi")
#     except:
#         print("khong the ket noi")
@app.post("/add")
def add_new_user(name:str, birth:str, gender:bool, weight:float, height:float, level:str):
    try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        a=db.members.insert_one({'name': name, 'birth': birth, 'gender': gender, 'weight': weight, 'height': height, 'level':level})
        print(a.inserted_id)
    except:
        raise HTTPException(status_code=400, detail="sai thong tin")
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

@app.get("/get_many")
def get_many(name:str, gender:bool, birth:str):
    try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        users = db.members.find({'name':name, 'gender':gender, 'birth':birth})
        if users is None:
          raise HTTPException(status_code=400, detail="khong tim thay thong tin")
        print(users)
        res=json.dumps(list(users),default=str)
        return res 
    except:
        raise HTTPException(status_code=400, detail="sai thong tin")

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
    


    


 