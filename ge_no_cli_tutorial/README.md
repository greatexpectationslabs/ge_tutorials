## 1. Start the Database used in this example

This example uses the same Postgres database as the [Getting started with Great Expectations tutorial](ge_getting_started_tutorial#getting-started-with-great-expectations-tutorial), so follow those instructions to run `docker-compose up` to start the database, e.g.

```
cd ge_getting_started_tutorial
docker-compose up
```

## 2. Install great expectations

Use pip to install great expectations and additional depedencies to connect to the Postgres database: 

```
pip install great_expectations SQLAlchemy psycopg2-binary
```

## 3. Run the example

```
python example.py
```
