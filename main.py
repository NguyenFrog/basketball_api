from typing import Union
import pymongo
from fastapi import FastAPI

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
        print("loi")
    return {"OK": "thanh cong"}
