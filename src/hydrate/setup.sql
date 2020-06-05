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