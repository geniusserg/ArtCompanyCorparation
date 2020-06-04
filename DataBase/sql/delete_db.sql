CREATE OR REPLACE PROCEDURE delete_database(TEXT, TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    perform
        pg_terminate_backend(pid)
    FROM
        pg_stat_activity
    WHERE
        pid <> pg_backend_pid() AND datname = $1 ;
    perform dblink_exec('dbname='||current_database()||' user='||current_user||
        ' password='|| $2, 'DROP DATABASE IF EXISTS ' || $1);
END$$;