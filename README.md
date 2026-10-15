## สร้าง MCPs สำหรับ postgis สำหรับใช้ในการบริหารจัดการน้ำ

### 1. สร้างระบบโดยใช้ docker-compose

    จะได้ ระบบ 3 ระบบคือ

    Adminer

http://127.0.0.1:8085

MCPg

http://127.0.0.1:8087/mcp

PostgreSQL + PostGIS + TimescaleDB

127.0.0.1:5432

### TimescaleDB

บริการ `postgis` ใช้ image `water-postgis-timescaledb:18-3.6-2.30.2-1`
สร้างจาก `postgis/postgis:18-3.6` และติดตั้ง TimescaleDB `2.30.2`
สำหรับ PostgreSQL 18 บน Debian 13 โดยยังใช้ volume `postgres_data`
ที่ `/var/lib/postgresql` และชื่อ host/container เดิม

```bash
docker-compose config --quiet
docker-compose build postgis
docker-compose up -d --no-deps postgis
```

สำหรับ volume ใหม่ `init/02-enable-timescaledb.sql` จะเปิด extension ให้อัตโนมัติ
สำหรับฐานข้อมูลเดิม ให้สำรองด้วย `pg_dump -Fc` ก่อนเปลี่ยน container แล้วเปิด extension:

```bash
docker exec water-postgis psql -U wateradmin -d waterdb -v ON_ERROR_STOP=1 -f /docker-entrypoint-initdb.d/02-enable-timescaledb.sql
docker exec water-postgis psql -U wateradmin -d waterdb -c "SELECT extname, extversion FROM pg_extension;"
```

Compose กำหนด `shared_preload_libraries=timescaledb` จึงต้อง restart/recreate
เมื่อเปลี่ยนการตั้งค่านี้ หากเพิ่ม extension ที่ต้อง preload ในอนาคต ให้รวมชื่อในรายการเดียวกัน
MCPg ยังคงใช้บัญชี `mcpg_reader` ในโหมดอ่านอย่างเดียว
ตาราง GIS และสถานีเดิมยังเป็นตารางปกติ การสร้าง hypertable สำหรับข้อมูลตรวจวัดตามเวลา
ต้องออกแบบคอลัมน์เวลาและ key ให้เหมาะสมก่อน

สำรองก่อนเปลี่ยนระบบครั้งนี้ไว้ใน `backups/waterdb-before-timescaledb-20261015.dump`
(ไม่รวมใน Git) เป็น backup เฉพาะฐานข้อมูล `waterdb` ไม่รวม roles ทั้ง cluster
หากต้องย้อน image ก่อนเปิด extension สามารถใช้ image เดิม `postgis/postgis:18-3.6`
และนำ command preload ออกได้ หลังเปิด extension แล้วต้องวางแผนย้อนกลับจาก backup
ห้ามลบ volume ด้วย `docker-compose down -v`

แหล่งอ้างอิง: [TimescaleDB releases](https://github.com/timescale/timescaledb/releases/tag/2.30.2)
และ [แพ็กเกจทางการ](https://packagecloud.io/timescale/timescaledb)

สถานะเมื่อ 2026-10-15: build และนำไปใช้กับ container `water-postgis` แล้ว
เปิด extension ใน `waterdb` สำเร็จ: PostgreSQL 18.6, PostGIS 3.6.4,
TimescaleDB 2.30.2; healthcheck ผ่าน และ MCP `water-postgis` เชื่อมต่อได้
ทดสอบ restore backup, สร้าง hypertable และเรียก `time_bucket` ใน container ชั่วคราวผ่าน
จำนวนข้อมูลหลังเปลี่ยนระบบ: สถานี 7,470 แถว, ลุ่มน้ำหลัก 1 แถว, ลุ่มน้ำย่อย 10 แถว
เท่ากับก่อนเปลี่ยนระบบ โดยยังไม่ได้แปลงตารางจริงเป็น hypertable

### 2. นำเข้าข้อมูล GIS ผ่าน postgis

### 3. ระบุ Layer ให้ AI รู้จักผ่าน meta.md

### 4. เชื่อม MCPs กับ AI

      เช่น codex mcp add water-postgis --url http://127.0.0.1:8087/mcp

### 5. ทดลองAI สั่งการ




