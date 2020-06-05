<h1 align="right">Final Project</h1>
<h6 align="right">MACS 30123: Large-Scale Computing for the Social Sciences | Spring 2020</h6>

<h1 align="center">Per-Block Building Capacity</h1>
<h2 align="center">Heuristics for Targeted Urban Infrastructure Investment</h2>

# Background 

# Architecture

## Overview

## Details: Upload

## Details: Hydration

-`setup.sql`
```SQL
-- sanity check 
select current_user;

-- create extensions
create extension postgis;
create extension fuzzystrmatch;
create extension postgis_topology;

-- in-band permissions
alter schema topology owner to rds_superuser;

CREATE FUNCTION exec(text) returns text language plpgsql volatile AS $f$ BEGIN EXECUTE $1; RETURN $1; END; $f$;

SELECT exec('ALTER TABLE ' || quote_ident(s.nspname) || '.' || quote_ident(s.relname) || ' OWNER TO rds_superuser;')
  FROM (
    SELECT nspname, relname
    FROM pg_class c JOIN pg_namespace n ON (c.relnamespace = n.oid) 
    WHERE nspname in ('topology') AND
    relkind IN ('r','S','v') ORDER BY relkind = 'S')
s; 

-- test 
select topology.createtopology('my_new_topo',26986,0.5);

-- make like a carpenter and build some tables 
create table blocks; 
create table buildings;

-- set up geospatial indices 
```

## Details: Querying

# Resources
- https://stackoverflow.com/questions/34758338/how-to-populate-a-postgresql-database-with-mrjob-and-hadoop
- https://www.youtube.com/watch?v=BzjeZFej_0k
- https://gis.stackexchange.com/questions/239198/adding-geopandas-dataframe-to-postgis-table
- https://www.classes.cs.uchicago.edu/archive/2013/spring/12300-1/labs/lab5/
- https://serverfault.com/questions/656079/unable-to-connect-to-public-postgresql-rds-instance
