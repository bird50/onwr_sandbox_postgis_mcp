FROM postgis/postgis:18-3.6

ARG TIMESCALEDB_VERSION=2.30.2~debian13-1806

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
    && curl -fsSL https://packagecloud.io/timescale/timescaledb/gpgkey \
       | gpg --dearmor -o /usr/share/keyrings/timescaledb.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/timescaledb.gpg] https://packagecloud.io/timescale/timescaledb/debian/ trixie main' \
       > /etc/apt/sources.list.d/timescaledb.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       timescaledb-2-postgresql-18=${TIMESCALEDB_VERSION} \
       timescaledb-2-loader-postgresql-18=${TIMESCALEDB_VERSION} \
    && rm -rf /var/lib/apt/lists/*
