FROM postgres:12

COPY ./data/*.csv /tmp/
COPY ./data/ /docker-entrypoint-initdb.d/
RUN chmod 775 /docker-entrypoint-initdb.d/* /tmp/*.csv
