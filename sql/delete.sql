CREATE OR REPLACE PROCEDURE delete_by_name(TEXT)
LANGUAGE plpgsql AS $$
BEGIN
  DELETE FROM pictures WHERE name LIKE $1;
END$$;

CREATE OR REPLACE PROCEDURE delete_record(TEXT, INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
  IF $1 = 'pictures' THEN
    DELETE FROM pictures WHERE id = $2;
  ELSIF $1 = 'orders' THEN
    DELETE FROM orders WHERE id = $2;
  ELSIF $1 = 'delivery' THEN
    DELETE FROM delivery WHERE id = $2;
  END IF;
END$$;