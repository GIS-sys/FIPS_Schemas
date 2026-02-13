TODO config.yaml?

# Structure

## main

TODO

## test

### Create local database

- extract original database using get_database_data.py

- create test database:

```bash
sudo -u postgres psql
```

```bash
-- Create user with password
CREATE USER fips_test_user WITH PASSWORD 'fips_test_pass';

-- Create database
CREATE DATABASE fips_test_db OWNER fips_test_user;

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE fips_test_db TO fips_test_user;

-- Grant creating database rights
ALTER USER fips_test_user CREATEDB;

exit
```

- fill test database with data from original using fill_database_data.py

### Start testing stream

TODO





# TODO

docker run -it -v "$(pwd):/app" -w /app python:3.11 sh -c "pip install psycopg2 tabulate && python analyze.py" > test_analyze.txt

add if-else block

```bash
-- Create tables
CREATE TABLE table_2col (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL);
CREATE TABLE table_3col (id SERIAL PRIMARY KEY, product VARCHAR(50) NOT NULL, price DECIMAL(10,2));
CREATE TABLE table_5col (id SERIAL PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), active BOOLEAN DEFAULT true);

-- Insert data into table_2col
INSERT INTO table_2col (name) VALUES ('Alice'), ('Bob'), ('Charlie'), ('Diana'), ('Eve');

-- Insert data into table_3col
INSERT INTO table_3col (product, price) VALUES 
    ('Laptop', 999.99), ('Mouse', 29.99), ('Keyboard', 79.99), 
    ('Monitor', 299.99), ('Headphones', 89.99), ('Webcam', 69.99), 
    ('USB Cable', 9.99);

-- Insert data into table_5col
INSERT INTO table_5col (first_name, last_name, email, active) VALUES 
    ('John', 'Smith', 'john.smith@email.com', true),
    ('Jane', 'Doe', 'jane.doe@email.com', true),
    ('Bob', 'Johnson', 'bob.johnson@email.com', false),
    ('Alice', 'Williams', 'alice.w@email.com', true),
    ('Charlie', 'Brown', 'charlie.b@email.com', true),
    ('Diana', 'Prince', 'diana.p@email.com', true),
    ('Evan', 'Davis', 'evan.d@email.com', false),
    ('Fiona', 'Garcia', 'fiona.g@email.com', true);

-- Verify the data
SELECT 'table_2col' as table_name, count(*) as rows FROM table_2col
UNION ALL
SELECT 'table_3col', count(*) FROM table_3col
UNION ALL
SELECT 'table_5col', count(*) FROM table_5col;
```

