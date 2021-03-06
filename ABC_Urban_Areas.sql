/*
public.geocodingdata112617
public.ne_10m_urban_areas
public.ne_10m_admin_0_countries
public.ne_10m_roads
*/


--Project your data
create table abc_projected as
select *, ST_Transform(geom, 4258) as the_geom
from public.geocodingdata112617;

create table roads_projected as
select *, ST_Transform(geom, 4258) as the_geom
from public.ne_10m_roads;

create table countries_projected as
select *, ST_Transform(geom, 4258) as the_geom
from public.ne_10m_admin_0_countries;

create table urban_projected as
select *, ST_Transform(geom, 4258) as the_geom
from public.ne_10m_urban_areas;


--clip data to europe
SELECT *
INTO public.Europe
FROM countries_projected
WHERE region_un = 'Europe';

create table public.UrbanCountries as
select europe.name, urban_projected.gid, urban_projected.the_geom
FROM europe, urban_projected
where ST_Intersects(europe.the_geom, urban_projected.the_geom);

create table public.EuropeABC as
select abc_projected.*, europe.name
FROM europe, abc_projected
where ST_Intersects(europe.the_geom, abc_projected.the_geom);

create table public.Europeroads as
select roads_projected.*
FROM europe, roads_projected
where ST_Intersects(europe.the_geom, roads_projected.the_geom);




--how many TT customers in urban areas?
create table public.EuropeTT1 as
select EuropeABC.*
FROM UrbanCountries, EuropeABC
where EuropeABC.tt_graduat = 1;

create table public.EuropeDT as
select EuropeABC.*
FROM UrbanCountries, EuropeABC
where EuropeABC.dt_graduat = 1;

create table public.EuropeCT as
select EuropeABC.*
FROM UrbanCountries, EuropeABC
where EuropeABC.ct_graduat = 1;





--sum customers by country
create table public.TT_Sum as
SELECT name, SUM(tt_graduat) AS TTCount
FROM EuropeTT1
GROUP BY name

create table public.DT_Sum as
SELECT name, SUM(dt_graduat) AS DTCount
FROM EuropeDT
GROUP BY id

create table public.CT_Sum as
SELECT name, SUM(ct_graduat) AS CTCount
FROM EuropeCT
GROUP BY id





--How many customers within 5 miles of roads?
create table public.roadsABC as
select geocodingdata112617.*
FROM Europeroads, geocodingdata112617
where ST_Dwithin(Europeroads.geom, geocodingdata112617.geom, 8046.72);
