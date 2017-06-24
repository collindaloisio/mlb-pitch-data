CREATE DATABASE mlbdb
-- OWNER =  role_name
-- TEMPLATE = template
-- ENCODING = encoding
-- LC_COLLATE = collate
-- LC_CTYPE = ctype
-- TABLESPACE = tablespace_name
-- CONNECTION LIMIT = max_concurrent_connection
;

CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);