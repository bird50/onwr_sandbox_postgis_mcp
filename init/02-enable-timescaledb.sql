-- Runs only when initializing a new PostgreSQL data directory.
-- For an existing waterdb, execute this file explicitly after restarting
-- with the TimescaleDB image and shared_preload_libraries setting.
CREATE EXTENSION IF NOT EXISTS timescaledb VERSION '2.30.2';
