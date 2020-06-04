
CREATE OR REPLACE PROCEDURE create_tables()
LANGUAGE plpgsql AS $$
BEGIN  
    CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    name TEXT,
    artist TEXT,
    cost REAL
    );

    CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    picture_id INTEGER,
    address INTEGER,
    cost REAL
    );

    CREATE TABLE delivery (
    id SERIAL PRIMARY KEY,
    name TEXT,
    cost REAL
    );

    CREATE INDEX picture_index ON pictures(name);
END;
$$
