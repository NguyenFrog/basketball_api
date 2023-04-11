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

@app.on_event("startup")
def viet_nam():
    try:
        client=pymongo.MongoClient("mongodb+srv://nguyen:Nguyencony02@database.rcdfbvy.mongodb.net/?retryWrites=true&w=majority")
        db = client["basketball"]
        # user = db.create_collection("members")
        db.members.insert_one({'ten': "Nguyen", 'tuoi': 20})
        print("da ket noi")
    except:
        print("khong the ket noi")