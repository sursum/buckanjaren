CREATE DATABASE buckanjaren;
CREATE USER buckanjaren WITH PASSWORD 'sursum';
ALTER DATABASE buckanjaren OWNER TO buckanjaren;
ALTER ROLE buckanjaren SET client_encoding TO 'utf8';
ALTER ROLE buckanjaren SET default_transaction_isolation TO 'read committed';
ALTER ROLE buckanjaren SET timezone TO 'Europe/Stockholm';
GRANT ALL PRIVILEGES ON DATABASE buckanjaren TO buckanjaren;
