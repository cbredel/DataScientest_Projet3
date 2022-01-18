--create database db_datascientest;

-- Creation de la table d'intégration des données
CREATE TABLE public.winemag (
	id text NULL,
	country text NULL,
	description text NULL,
	designation text NULL,
	points text NULL,
	price text NULL,
	province text NULL,
	region_1 text NULL,
	region_2 text NULL,
	taster_name text NULL,
	taster_twitter_handle text NULL,
	title text NULL,
	variety text NULL,
	winery text NULL
);


--Chargement des données CSv dans la table d'intégration

COPY public.winemag FROM 'winemag-data-130k-v2.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF-8';


--Création et aliementation des tables  de libellé 

--Pour les pays
select row_number() over () as country_id,
country
into country
from public.winemag group by country;

--Pour les provinces
select row_number() over () as prov_id,
province as prov_name
into province
from public.winemag group by province;

--Pour les gouteurs
select row_number() over () as t_id,
taster_name as t_name,
taster_twitter_handle as t_twitter
into taster
from public.winemag group by taster_name,taster_twitter_handle;

--Pour les Variétés
select row_number() over () as var_id,
variety as var_name
into variety
from public.winemag group by variety;


--Pour les région
select row_number() over () as r_id,
region_1 as reg_1,
region_2 as reg_2
into region
from public.winemag group by region_1,region_2;


-- Création et alimentation de la table des vins 
select 
	id::integer ,
	title,
	winery,
	description,
	designation,
	points::integer as points,
	price::real as price,
	country_id,
	prov_id,
	r_id,
	t_id,
	var_id
into wine
from public.winemag
	left join country on country.country=winemag.country 
	left join province on province.prov_name=province
	left join region on region.reg_1=region_1 and region.reg_2=region_2 
	left join taster on taster_name=t_name and taster_twitter_handle=t_twitter 
	left join variety on variety=var_name;


--suppression de la table d'intégration 
drop table public.winemag;

--Ajout des clés primaire pour chaque table
ALTER TABLE public.wine ADD CONSTRAINT wine_pk PRIMARY KEY (id);
ALTER TABLE public.country ADD constraint country_pk PRIMARY KEY (country_id);
ALTER TABLE public.province ADD constraint province_pk PRIMARY KEY (prov_id);
ALTER TABLE public.region ADD CONSTRAINT region_pk PRIMARY KEY (r_id);
ALTER TABLE public.taster ADD CONSTRAINT taster_pk PRIMARY KEY (t_id);
ALTER TABLE public.variety ADD CONSTRAINT variety_pk PRIMARY KEY (var_id);

--Ajout des clés étrangères à la table des vins
ALTER TABLE public.wine ADD CONSTRAINT wine_fk_country FOREIGN KEY (country_id) REFERENCES public.country(country_id);
ALTER TABLE public.wine ADD CONSTRAINT wine_fk_region FOREIGN KEY (r_id) REFERENCES public.region(r_id);
ALTER TABLE public.wine ADD CONSTRAINT wine_fk_taster FOREIGN KEY (t_id) REFERENCES public.taster(t_id);
ALTER TABLE public.wine ADD CONSTRAINT wine_fk_variety FOREIGN KEY (var_id) REFERENCES public.variety(var_id);
ALTER TABLE public.wine ADD CONSTRAINT wine_fk_province FOREIGN KEY (prov_id) REFERENCES public.province(prov_id);

--Ajout et configuration de séquences pour chacune des tables 
-- Tabe des vins
CREATE SEQUENCE wine_id_seq;
ALTER TABLE public.wine
        ALTER COLUMN id SET NOT NULL
        , ALTER COLUMN id SET DEFAULT nextval('wine_id_seq');
        
SELECT setval('wine_id_seq', MAX(id))
FROM public.wine;

--Table des pays
CREATE SEQUENCE country_id_seq;
ALTER TABLE public.country
        ALTER COLUMN country_id SET NOT NULL
        , ALTER COLUMN country_id SET DEFAULT nextval('country_id_seq');
        
SELECT setval('country_id_seq', MAX(country_id))
FROM public.country;

--Table des provinces
CREATE SEQUENCE province_id_seq;
ALTER TABLE public.province
        ALTER COLUMN prov_id SET NOT NULL
        , ALTER COLUMN prov_id SET DEFAULT nextval('province_id_seq');
        
SELECT setval('province_id_seq', MAX(prov_id))
FROM public.province;

--Table des régions
CREATE SEQUENCE region_id_seq;
ALTER TABLE public.region
        ALTER COLUMN r_id SET NOT NULL
        , ALTER COLUMN r_id SET DEFAULT nextval('region_id_seq');
        
SELECT setval('region_id_seq', MAX(r_id))
FROM public.region;


--Table des gouteurs
CREATE SEQUENCE taster_id_seq;
ALTER TABLE public.taster
        ALTER COLUMN t_id SET NOT NULL
        , ALTER COLUMN t_id SET DEFAULT nextval('taster_id_seq');
        
SELECT setval('taster_id_seq', MAX(t_id))
FROM public.taster;


--Table des variétés
CREATE SEQUENCE varitey_id_seq;
ALTER TABLE public.variety
        ALTER COLUMN var_id SET NOT NULL
        , ALTER COLUMN var_id SET DEFAULT nextval('varitey_id_seq');
        
SELECT setval('varitey_id_seq', MAX(var_id))
FROM public.variety;
