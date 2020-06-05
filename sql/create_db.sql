CREATE OR REPLACE PROCEDURE create_database(TEXT, TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    perform dblink_exec('dbname='||current_database()||' user='||current_user||' password='|| $2,
        'create database ' || $1 || ' with owner= '|| current_user);
END
$$;

CREATE OR REPLACE PROCEDURE install_dblink()
LANGUAGE plpgsql
AS $$
BEGIN
    create extension dblink;
END
$$;

CREATE OR REPLACE FUNCTION output_databases()
RETURNS TABLE (id name) AS $$
BEGIN
  RETURN QUERY  (SELECT datname FROM pg_database);
END;
$$ LANGUAGE plpgsql VOLATILE;