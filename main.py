from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
from typing import List, OrderedDict
from tdigest import TDigest
import uvicorn 

app = FastAPI()
db = {}

class Order:
    def __init__ (self, order_id, items_list =[], customer = "unknow customer"):
        self.order_id = order_id
        self.items_list = []
        self.customer = customer
        
    def get_order_id(self):
        return self.order_id
    def add_item(self, item):
        self.items_list.append(item)
    def set_customer(self,customer):
        self.customer = customer
    def __str__(self):
        return self.__dict__
    
class Item:
    def __init__ (self, item_id, name ):
        self.item_id = item_id
        self.name = name

class _Order (BaseModel):
    order_id : int
    items_list : List[int]
    customer : str

class _Item (BaseModel):
    item_id : int
    name : str

@app.get('/')
def index():
	return {'msg','Api Alive'}

@app.post('/place_order')
def place_order(new_order: _Order)->str:
    order_id = new_order.order_id
    if order_id in db.keys():
        raise HTTPException(status_code=409, detail="Conflict, order_id already exist in database")
    db[order_id] = new_order


@app.get('/get_order')
def get_order(order_id: _Order.order_id)->dict:
    if order_id not in db.keys():
        raise HTTPException(status_code=404, detail="Cannot find order in DB")
    order = db[order_id]
    return order.__dict__
    
@app.get('/DB')
def getDB():
    '''

    '''
    return [db[key] for key in db.keys()]

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)