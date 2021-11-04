from fastapi import FastAPI
from pydantic import BaseModel
import math
from typing import List, OrderedDict
from tdigest import TDigest
import uvicorn 

app = FastAPI()
db = {}

class Order:
    def __init__ (self, order_id, items =[], customer = "unknow customer"){
        self.order_id = order_id
        self.items = []
        self.customer = customer
    }
    def get_order_id(self):
        return self.order_id
    def add_item(self, item):
        self.items.append(item)
    def set_customer(self,customer):
        self.customer = customer
    
class Item:
    def __init__ (self, item_id, name ):
        self.item_id = item_id
        self.name = name

class _Order (BaseModel):
    order_id : int
    items : List[int]
    customer : str

class _Item (BaseModel):
    item_id : int
    name : str

