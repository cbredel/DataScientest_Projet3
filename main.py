# -*- coding: utf-8 -*-
"""
Created on Jan. 18 

@author: Christophe BREDEL 



"""

from fastapi import Depends, FastAPI, Response, HTTPException, Request
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from pydantic import BaseModel
from typing import Optional

import pickle

import json
import psycopg2
from psycopg2.extras import RealDictCursor

class country2(BaseModel):
    country_id:  int 
    country: str

class Wine(BaseModel):
    id:  Optional[int] = None
    title: str
    winery:Optional[str] = None 
    description: Optional[str] = None
    designation:Optional[str] = None
    points:Optional[int] = None
    price:Optional[float] = None
    country_id:Optional[int] = None
    prov_id:Optional[int] = None
    r_id:Optional[int] = None
    t_id:Optional[int] = None
    var_id:Optional[int] = None

class QueryString(BaseModel):
	mystr : str
    
class QueryId(BaseModel):
	myid : int

app = FastAPI(    title="Wines API",
    description="Projet 3 Formation DataScientest.",
    version="0.1")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


security=HTTPBasic()
#Definition des variables de connection à la base
myuser="postgres"
mypassword="postgres"
myhost="localhost"
myport="5432"
mydb="db_datascientest"

def get_connection():
	return psycopg2.connect(user=myuser,
							password=mypassword,
							host=myhost,
							port=myport,
							database=mydb)


def query_to_json(myquery):
	print("Dans la fonction")
	try:
		print("Dans le try")
		connection=psycopg2.connect(user=myuser,
							password=mypassword,
							host=myhost,
							port=myport,
							database=mydb)
		print("oka")
		cursor=connection.cursor(cursor_factory=RealDictCursor)
		print("ok1")
		#myreq="select per_id,per_nom ||' ' ||per_prenom as per_nom_complet from agape_gt.ges_personnel where per_actif='OUI' order by per_nom_complet"
		cursor.execute(myquery)
		print("ok2")
		meslignes=cursor.fetchall()
		print("ok3")
		#print("requete faite")
		#for row in meslignes:
		#	print(row[0])
		print(json.dumps(meslignes))
		print("ok4")
		#return	json.dumps(meslignes)
		return meslignes
	except(Exception, psycopg2.Error) as error:
		print("Erreur", error)
	finally:
		#if (connection):
		#	cursor.close()
		#	connection.close()
		print("Connection fermé")

@app.get("/",tags=['System'])
async def root():
    return {"message": "Welcome in the Wine APIs"}


@app.get("/countries",tags=['Variables'], name='Give country list')
async def list_countries():
    myreq="select * from public.country"
    return query_to_json(myreq)

@app.get("/provinces",tags=['Variables'], name='Give provinces list')
async def list_provinces():
    myreq="select * from public.province"
    return query_to_json(myreq)

@app.get("/regions",tags=['Variables'], name='Give region list')
async def list_regions():
    myreq="select * from public.region"
    return query_to_json(myreq)

@app.get("/tasters",tags=['Variables'], name='Give taster list')
async def list_tasters():
    myreq="select * from public.taster"
    return query_to_json(myreq)

@app.get("/varieties",tags=['Variables'], name='Give varieties list')
async def list_varieties():
    myreq="select * from public.variety"
    return query_to_json(myreq)

@app.get("/wines",tags=['Wines'], name='Give Wine list')
async def list_wines():
    myreq="select * from public.wine"
    return query_to_json(myreq)


@app.get("/wine/get/{wine_id}",tags=['Wines'], name='Give wines information form Id')
async def get_wine(wine_id):
    myreq="select * from public.wine where id="+wine_id
    return query_to_json(myreq)


@app.put("/country/{country_name}",tags=['Variables'], name='Add a country')
async def create_country(country_name):
	print(country_name)
	try:
		connection=get_connection()
		cursor=connection.cursor()
		cursor.execute("insert into public.country (country) values ('"+country_name+"');")
		connection.commit()
		return	0
	except(Exception, psycopg2.Error) as error:
		print("Erreur", error)
	finally:
		if (connection):
			cursor.close()
			connection.close()
	return templates.TemplateResponse("add_wine.html", {"request": request})

@app.post("/wine/add",tags=['Wines'], name='Add Wine')	
async def  win_add(wine: Wine):
	print("hello pour l'ajout2")
	print(wine)
	l_fld=[]
	l_val=[]
	mySQL="INSERT INTO public.wine (title, winery, description, designation, points, price, country_id, prov_id, r_id, t_id, var_id) VALUES( '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s)" % (wine.title, wine.winery, wine.description, wine.designation, wine.points, wine.price, wine.country_id, wine.prov_id, wine.r_id, wine.t_id, wine.var_id)
	mySQL=mySQL.replace('None','NULL')
	mySQL=mySQL.replace("'None'",'NULL')
	print(mySQL)

	try:
		connection=get_connection()
		cursor=connection.cursor()
		cursor.execute(mySQL)
		#cursor.execute("insert into public.country2 (country) values  (%s)",country_name )
		connection.commit()
		return	0
	except(Exception, psycopg2.Error) as error:
		print("Erreur", error)
	finally:
		if (connection):
			cursor.close()
			connection.close()
	return {"message": "Wine recorded"}

@app.post("/wine/search/bytitle",tags=['Wines'],name='Search wine by name')
async def get_wine(q:QueryString):
    myreq="select * from public.wine where title ilike '%"+q.mystr+"%'"
    print(myreq)
    return query_to_json(myreq)


@app.post("/wine/search/bycountryname",tags=['Wines'],  name='Search wine by name of the country')
async def get_wine(q:QueryString):
    myreq="select * from public.wine where country_id =(select country_id from public.country where country ilike '"+q.mystr+"')"
    print(myreq)
    return query_to_json(myreq)	

@app.post("/wine/search/bycountryid",tags=['Wines'], name='Search wine by ID of the country')
async def get_wine(q:QueryId):
    myreq="select * from public.wine where country_id="+str(q.myid)+""
    print(myreq)
    return query_to_json(myreq)		

