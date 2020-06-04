CREATE OR REPLACE PROCEDURE clear_all_tables()
LANGUAGE plpgsql AS $$
BEGIN
  TRUNCATE pictures;
  TRUNCATE delivery;
  TRUNCATE orders;
END$$;

CREATE OR REPLACE PROCEDURE clear(TEXT)
LANGUAGE plpgsql AS $$
BEGIN
  execute
    'TRUNCATE ' || $1;
END$$;