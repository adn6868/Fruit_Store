from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
from typing import List, OrderedDict
from tdigest import TDigest
import uvicorn 

app = FastAPI()
order_db = {}
item_db = {}

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

@app.post('/order/place_order')
async def place_order(new_order: _Order)->str:
    order_id = new_order.order_id
    if order_id in order_db.keys():
        raise HTTPException(status_code=409, detail="Conflict, order_id already exist in database")
    order_db[order_id] = new_order
    return "Order placed"


@app.get('/order/get_order')
async def get_order(order_id: int)->dict:
    if order_id not in order_order_db.keys():
        raise HTTPException(status_code=404, detail="Cannot find order in order_db")
    order = order_db[order_id]
    return order.__dict__

@app.post('/order/place_order')
async def place_order(new_order: _Order)->str:
    order_id = new_order.order_id
    if order_id in order_db.keys():
        raise HTTPException(status_code=409, detail="Conflict, order_id already exist in database")
    order_db[order_id] = new_order
    return "Order placed"

@app.get('/item/add_item')
async def add_item(new_item: _Item)->dict:
    item_id = new_item.item_id
    if item_id in order_db.keys():
        raise HTTPException(status_code=409, detail="Conflict, item_id already exist in database")
    item_db[item_id] = new_item
    return "New Item Added"

@app.get('/order/get_item')
async def get_item(item_id: int)->dict:
    if item_id not in item_db.keys():
        raise HTTPException(status_code=404, detail="Cannot find item in item_db")
    item = item_db[item_id]
    return item.__dict__

@app.get('/item/update_item')
async def update_item(new_item: _Item)->dict:
    item_id = new_item.item_id
    if item_id not in order_db.keys():
        raise HTTPException(status_code=409, detail="Conflict, Item order not found Please use add_item to insert into db")
    item_db[item_id] = new_item
    return "Item Updated"

@app.get('/order_db')
def get_order_db():
    '''

    '''
    return [order_db[key] for key in order_db.keys()]

@app.get('/item_db')
def get_item_db():
    '''

    '''
    return [item_db[key] for key in item_db.keys()]

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)