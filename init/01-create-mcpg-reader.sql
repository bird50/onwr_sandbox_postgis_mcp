-- Create MCP read-only user
CREATE USER mcpg_reader
WITH PASSWORD 'passward4MCp';

-- Allow connection to waterdb
GRANT CONNECT ON DATABASE waterdb TO mcpg_reader;

-- Allow access to public schema
GRANT USAGE ON SCHEMA public TO mcpg_reader;

-- Read existing tables
GRANT SELECT ON ALL TABLES
IN SCHEMA public
TO mcpg_reader;

-- Read existing sequences if needed
GRANT SELECT ON ALL SEQUENCES
IN SCHEMA public
TO mcpg_reader;

-- Automatically allow reading tables created later
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT ON TABLES
TO mcpg_reader;

ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT ON SEQUENCES
TO mcpg_reader;