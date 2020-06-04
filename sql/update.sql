CREATE OR REPLACE FUNCTION update_price_on_picture()
RETURNS TRIGGER AS $pictures_updater$
BEGIN
    UPDATE orders
    SET cost = CASE
        WHEN NEW.cost is NULL OR OLD.cost is NULL
        THEN 0
        ELSE cost - OLD.cost + NEW.cost
        END
    WHERE NEW.id = picture_id;
    RETURN NEW;
END;
$pictures_updater$ LANGUAGE plpgsql VOLATILE;

CREATE OR REPLACE FUNCTION update_price_on_delivery()
RETURNS TRIGGER AS $delivery_updater$
BEGIN
    UPDATE orders
    SET cost = CASE
        WHEN NEW.cost is NULL OR OLD.cost is NULL
        THEN 0
        ELSE cost - OLD.cost + NEW.cost
        END
    WHERE NEW.id = address;
    RETURN NEW;
END;
$delivery_updater$ LANGUAGE plpgsql VOLATILE;

CREATE TRIGGER delivery_updater
AFTER INSERT OR UPDATE OR DELETE ON delivery
FOR EACH ROW EXECUTE PROCEDURE update_price_on_delivery();

CREATE TRIGGER pictures_updater
AFTER INSERT OR UPDATE OR DELETE ON pictures
FOR EACH ROW EXECUTE PROCEDURE update_price_on_picture();