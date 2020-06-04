CREATE OR REPLACE PROCEDURE insert_delivery( v_id INTEGER, v_target TEXT, v_price REAL)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO delivery (id, name, cost)
    VALUES (v_id, v_target, v_price)
      ON CONFLICT ("id") DO UPDATE SET
      name=EXCLUDED.name,
      cost=EXCLUDED.cost;
END$$;

CREATE OR REPLACE PROCEDURE insert_pictures( v_id INTEGER, v_name TEXT, v_artist TEXT, v_price REAL)
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO pictures (id, name, artist, cost)
    VALUES (v_id, v_name, v_artist, v_price)
      ON CONFLICT ("id") DO UPDATE SET
      name=EXCLUDED.name,
      artist=EXCLUDED.artist,
      cost=EXCLUDED.cost;
END$$;

CREATE OR REPLACE PROCEDURE insert_orders(v_id INTEGER, v_picture_id INTEGER,  v_delivery_id INTEGER)
LANGUAGE plpgsql AS $$
DECLARE
    delivery_price REAL;
    picture_price REAL;
    total_price REAL;
BEGIN
    delivery_price = (select cost from delivery where delivery.id = v_delivery_id);
    picture_price  = (select cost from pictures where pictures.id = v_picture_id);
    IF v_delivery_id is NULL OR delivery_price is NULL THEN delivery_price = 0; END IF;
    IF v_picture_id is NULL OR picture_price is NULL THEN picture_price = 0; END IF;
    total_price = delivery_price + picture_price;

    INSERT INTO orders (id, picture_id, address, cost)
    VALUES (v_id, v_picture_id, v_delivery_id, total_price)
      ON CONFLICT("id") DO UPDATE SET
        id = excluded.id,
        picture_id = excluded.picture_id,
        address = excluded.address;
END$$