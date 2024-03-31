FROM postgres:latest

# Copy the .create_db.sql file from the local directory to the /docker-entrypoint-initdb.d/
# directory in the container. PostgreSQL will automatically execute any SQL scripts found
# in this directory when the container starts up for the first time.
COPY create_table.sql /docker-entrypoint-initdb.d/

