                     Mac
                      │
        ┌─────────────┼─────────────┐
        │             │             │
      :5432         :8085         :8087
        │             │             │
        ▼             ▼             ▼

 PostgreSQL 18     Adminer         MCPg

+ PostGIS 3.6                      │
  
       ▲                           │
       │                           │
       └──── mcpg_reader ──────────┘
              SELECT only

Adminer
http://127.0.0.1:8085

MCPg
http://127.0.0.1:8087/mcp

PostgreSQL
127.0.0.1:5432

## Adminer:

System:   PostgreSQL
Server:   postgis
Username: wateradmin
Password: wateradm1n
Database: waterdb

## ทดสอบสิทธิ์ MCP:

Username: mcpg_reader
Password: passward4MCp
Database: waterdb
