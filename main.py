from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math
from typing import List, OrderedDict
from tdigest import TDigest
import uvicorn 
import psycopg2
from config import db_config

db_connection = psycopg2.connect(host=db_config['host'],
    user=db_config['user'],        
    password=db_config['passwd'],  
    dbname=db_config['db_name'])     

db_cur = db_connection.cursor()   

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
    order_existed = db_cur.execute("""select 1 from "orderTbl" where order_id =%s""" % order_id)
    order_existed = db_cur.fetchall()

    if order_existed:
        raise HTTPException(status_code=409, detail="Conflict, order_id already exist in database")
    else:
        query = """
            insert into "orderTbl" (order_id,item_list,customer) 
            VALUES ('%s','%s','%s')
        """ % (new_order.order_id , new_order.items_list, new_order.customer)
        try:
            db_cur.execute(query)
            db_connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            raise HTTPException(status_code=500, detail="fail to insert into database")

    return "Order placed"


@app.get('/order/get_order')
async def get_order(order_id: int)->dict:
    query = """select order_id, item_list, customer from "orderTbl" where order_id = %s""" % order_id
    print(query)
    try:
        db_cur.execute(query)
        rv = db_cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        raise HTTPException(status_code=500, detail="can't find that in database")
    return rv if rv else "order not existed"

@app.post('/item/add_item')
async def add_item(new_item: _Item)->dict:
    item_id = new_item.item_id
    db_cur.execute("""select 1 from "itemTbl" where item_id =%s""" % item_id)
    item_existed = db_cur.fetchall()
    if item_existed:
        raise HTTPException(status_code=409, detail="Conflict, item_id already exist in database")
    else:
        query = """
            insert into "itemTbl" (item_id,name) 
            VALUES ('%s','%s')
        """ % (new_item.item_id , new_item.name)
        try:
            db_cur.execute(query)
            db_connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            raise HTTPException(status_code=500, detail="fail to insert into database")

    return "Item Added"

@app.get('/order/get_item')
async def get_item(item_id: int)->dict:
    query = """select item_id, name from "itemTbl" where item_id = '%s'""" % item_id
    try:
        db_cur.execute(query)
        rv = db_cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        raise HTTPException(status_code=500, detail="can't find that in database")
    return rv if rv else "item not existed"


@app.post('/item/update_item')
async def update_item(new_item: _Item)->dict:
    item_id = new_item.item_id
    db_cur.execute("""select 1 from "itemTbl" where item_id =%s""" % item_id)
    item_existed = db_cur.fetchall()

    if not item_existed:
        raise HTTPException(status_code=409, detail="Conflict, item_id not exist in database")
    query = """UPDATE "itemTbl" SET name = '%s' where item_id = '%s' """ % (new_item.name, new_item.item_id)
    try:
        db_cur.execute(query)
        db_connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        raise HTTPException(status_code=500, detail="fail to update in database")
    return "item updated"

if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)