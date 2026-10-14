# PostGIS overlay ผ่าน water-postgis

ใช้ image `water-mcpg-postgis:0.8.2-1` ที่ build จาก `ghcr.io/devopam/mcpg:0.8.2`
โดยเพิ่มรายชื่อฟังก์ชันใน `postgis_allowlist.py` ลงในนโยบาย SQL ของ upstream
ไม่มีการปิด validator หรือเปลี่ยนเป็น unrestricted และยังใช้ `mcpg_reader`
พร้อม read-only transaction และ timeout เดิม

## Build และตรวจสอบ

รันจาก root ของโปรเจกต์:

```bash
docker-compose build mcpg
docker run --rm --network none --entrypoint python water-mcpg-postgis:0.8.2-1 /opt/water-postgis/test_policy.py
docker-compose up -d --no-deps mcpg
python3 mcpg/smoke_test.py
```

การ recreate MCPg ทำให้ session MCP เดิมหมดอายุ ให้เชื่อมต่อใหม่
เมื่อเปลี่ยนเวอร์ชัน base image ต้องตรวจนโยบาย SQL และรันทดสอบใหม่

## เรียกผ่านเครื่องมือ run_select

ไม่ได้เพิ่มชื่อ MCP tool ใหม่ ใช้ `run_select` พร้อม SQL ได้โดยตรง
รองรับชื่อฟังก์ชันแบบ `ST_Intersection(...)` และ `public.ST_Intersection(...)`
เฉพาะรายชื่อที่ระบุใน `postgis_allowlist.py` ไม่เปิดทุกฟังก์ชัน `ST_*`

| งาน | ฟังก์ชันหลัก |
|---|---|
| Clip / Intersect | `ST_Intersection` |
| Union / Dissolve | `ST_Union`, `ST_UnaryUnion`, `ST_Collect` |
| Erase | `ST_Difference` |
| Symmetric difference | `ST_SymDifference` |
| Spatial join / กรองตำแหน่ง | `ST_Intersects`, `ST_Within`, `ST_Contains`, `ST_Covers`, `ST_CoveredBy` |
| ความสัมพันธ์อื่น | `ST_Disjoint`, `ST_Touches`, `ST_Overlaps`, `ST_Equals`, `ST_DWithin` |
| Buffer / วัดขนาด | `ST_Buffer`, `ST_Area`, `ST_Length`, `ST_Distance` |
| ตรวจและเตรียม geometry | `ST_IsValid`, `ST_IsValidReason`, `ST_IsEmpty`, `ST_MakeValid`, `ST_SRID`, `ST_Transform`, `ST_GeometryType`, `ST_CollectionExtract`, `ST_Multi` |
| สร้าง geometry / ส่งออก | `ST_GeomFromText`, `ST_MakeEnvelope`, `ST_AsText`, `ST_AsGeoJSON` |

ก่อน overlay ให้ตรวจ SRID และ validity ของทั้งสองเลเยอร์ ปรับ SRID ให้ตรงกัน
ด้วย `ST_Transform` เมื่อจำเป็น `ST_MakeValid` เปลี่ยนรูปทรงของผลลัพธ์ได้
จึงไม่ควรเรียกอัตโนมัติโดยไม่ตรวจผล การคำนวณพื้นที่จาก geometry ใช้หน่วยของ CRS
และการส่งออก GeoJSON เพื่อใช้บนแผนที่ควรแปลงเป็น EPSG:4326 ก่อน

### พื้นที่ลุ่มน้ำบางปะกง (ไร่)

```sql
SELECT ST_Area(ST_Union(geom)) / 1600.0 AS area_rai
FROM public."MainBasin_Hydro_BPK";
```

### Clip เลเยอร์อื่นด้วยขอบเขตลุ่มน้ำ

แทนที่ `your_layer`, `id`, `geom` ให้ตรงกับตารางจริง ตัวอย่างนี้สมมติว่า
ทั้งสองเลเยอร์ใช้ SRID เดียวกันและ geometry ถูกต้อง:

```sql
WITH basin AS (
  SELECT ST_Union(geom) AS geom
  FROM public."MainBasin_Hydro_BPK"
)
SELECT a.id,
       ST_AsGeoJSON(ST_Transform(ST_Intersection(a.geom, b.geom), 4326)) AS geometry
FROM public.your_layer a
JOIN basin b ON ST_Intersects(a.geom, b.geom)
LIMIT 100;
```

`ST_Intersects` รวมกรณีสัมผัสขอบ ผล intersection จึงอาจเป็นเส้นหรือจุดด้วย
หากต้องการเฉพาะพื้นที่ polygon ให้ใช้ `ST_CollectionExtract(..., 3)`
และตัดผลว่างออกตามงาน ไม่บันทึกผลลงตารางด้วยบัญชี read-only

## ย้อนกลับ

คืนค่า service `mcpg` เป็น `image: ghcr.io/devopam/mcpg:0.8.2` และลบ `build`
จากนั้นใช้ `docker-compose up -d --no-deps mcpg` ข้อมูล PostGIS ไม่ถูกเปลี่ยน
