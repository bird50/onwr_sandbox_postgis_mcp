# Metadata ของเลเยอร์

## MainBasin_Hydro_BPK

| รายการ | รายละเอียด |
|---|---|
| ชื่อเลเยอร์ | `MainBasin_Hydro_BPK` |
| ความหมาย | เลเยอร์ขอบเขตลุ่มน้ำบางปะกง |
| ฐานข้อมูล | `waterdb` |
| Schema | `public` |
| ตาราง | `public."MainBasin_Hydro_BPK"` |
| คอลัมน์เชิงพื้นที่ | `geom` |
| ชนิด Geometry | `MultiPolygon` |
| SRID | `32647` |
| MCP | `water-postgis` |

### คอลัมน์

| ชื่อ | ชนิดข้อมูล |
|---|---|
| `id` | `integer` |
| `geom` | `geometry(MultiPolygon,32647)` |
| `mb_code` | `varchar(5)` |
| `mbasin_t` | `varchar(40)` |
| `mbasin_e` | `varchar(45)` |
| `area_sqkm` | `double precision` |
| `mb_code2` | `varchar(2)` |

### ที่มาและข้อสังเกต

- ความหมายของเลเยอร์ยืนยันโดยผู้ใช้เมื่อวันที่ 2026-10-14
- ชื่อตาราง ชนิดคอลัมน์ และสิทธิ์ SELECT ของ `mcpg_reader` ตรวจสอบผ่าน MCPg เมื่อวันที่ 2026-10-14
- ณ วันที่ตรวจสอบ ไม่พบรายการของเลเยอร์นี้ใน `public."GisLayer"` แต่มีตารางเชิงพื้นที่จริงในฐานข้อมูล
- ยังไม่ได้ยืนยันผู้ผลิตข้อมูล วันที่จัดทำข้อมูล ความละเอียด หรือความครบถ้วนของขอบเขต
- Metadata นี้เป็นข้อมูลอ้างอิง ณ วันที่ตรวจสอบ ควรตรวจ schema จริงอีกครั้งก่อนใช้งานที่ขึ้นกับโครงสร้างปัจจุบัน

## SubBasin_Hydro_BPK

| รายการ | รายละเอียด |
|---|---|
| ชื่อเลเยอร์ | `SubBasin_Hydro_BPK` |
| ความหมาย | เลเยอร์ขอบเขตลุ่มน้ำย่อยของลุ่มน้ำบางปะกง |
| เลเยอร์ลุ่มน้ำหลักที่เกี่ยวข้อง | `MainBasin_Hydro_BPK` |

### ที่มาและข้อสังเกต

- ความหมายของเลเยอร์ยืนยันโดยผู้ใช้เมื่อวันที่ 2026-10-14
- ยังไม่ได้ตรวจสอบชื่อตาราง Schema คอลัมน์เชิงพื้นที่ ชนิด Geometry และ SRID ของเลเยอร์นี้ผ่าน MCP จึงควรตรวจสอบก่อนวิเคราะห์ข้อมูล

## thai_water_station

| รายการ | รายละเอียด |
|---|---|
| ชื่อเลเยอร์ | `thai_water_station` |
| ความหมาย | ชั้นข้อมูลสถานีวัดน้ำของประเทศไทย |
| แหล่งอ้างอิง | ระบบ `tws.onwr.go.th` |
| ข้อมูล ณ วันที่ | 15 ตุลาคม 2569 (2026-10-15) |
| ฐานข้อมูล | `waterdb` |
| Schema | `public` |
| ตาราง | `public.thai_water_station` |
| คอลัมน์เชิงพื้นที่ | `geom` |
| ชนิด Geometry | `Point` (2 มิติ) |
| SRID | `4326` |
| จำนวนแถวที่บัญชีอ่านได้ | 7,470 แถว ตรวจสอบล่าสุด ณ วันที่ 2026-10-15 |
| MCP | `water-postgis` |

### คอลัมน์

| ชื่อ | ชนิดข้อมูล |
|---|---|
| `id` | `integer` |
| `geom` | `geometry(Point,4326)` |
| `station_type_th` | `character varying` |
| `operation_type_th` | `character varying` |
| `station_code` | `character varying` |
| `station_name_th` | `character varying` |
| `water_source` | `character varying` |
| `location_detail` | `character varying` |
| `tambon_name_th` | `character varying` |
| `amphoe_name_th` | `character varying` |
| `province_name_th` | `character varying` |
| `basin_name_th` | `character varying` |
| `latitude` | `character varying` |
| `longitude` | `character varying` |
| `parameter_name_th` | `character varying` |
| `measurement_interval` | `character varying` |
| `has_forecast_result` | `character varying` |
| `is_used_in_forecast` | `character varying` |
| `station_status` | `character varying` |
| `remarks` | `character varying` |
| `agency_name_th` | `character varying` |

### ที่มาและข้อสังเกต

- ผู้ใช้ยืนยันเมื่อวันที่ 2026-10-15 ว่า `thai_water_station` คือชั้นข้อมูลสถานีวัดน้ำของประเทศไทย อ้างอิงจากระบบ `tws.onwr.go.th` ณ วันที่ 15 ตุลาคม 2569 (2026-10-15)
- แหล่งอ้างอิงและวันที่ข้อมูลข้างต้นบันทึกตามคำยืนยันของผู้ใช้ ไม่ใช่ผลการตรวจสอบเว็บไซต์โดยตรง
- ชื่อตาราง โครงสร้างคอลัมน์ ชนิด Geometry, SRID และจำนวนแถว ตรวจสอบผ่าน MCP `water-postgis` ด้วยคำสั่งอ่านอย่างเดียวเมื่อวันที่ 2026-10-15
- พบเป็นตารางจริงใน PostgreSQL catalog และบัญชี `mcpg_reader` มีสิทธิ์ SELECT; ยังไม่ได้ตรวจรายการของเลเยอร์นี้ใน `public."GisLayer"`
- ตรวจนับล่าสุดผ่าน MCP `water-postgis` ด้วยคำสั่ง SELECT แบบอ่านอย่างเดียวเมื่อวันที่ 2026-10-15 พบ 7,470 แถว แทนค่าที่บันทึกเดิม 8,003 แถว (ลดลงสุทธิ 533 แถว); ยังไม่ได้ตรวจสอบสาเหตุของความแตกต่าง จึงไม่สรุปว่าเกิดจากการลบหรือการปรับปรุงข้อมูลแบบใด
- ประเภทสถานีใน `station_type_th` จากการตรวจนับล่าสุด: สถานีตรวจวัดน้ำฝน 3,496 แถว, สถานีตรวจวัดน้ำฝนและน้ำท่า 2,151 แถว, สถานีตรวจวัดน้ำท่า 866 แถว และสถานีตรวจอากาศ 957 แถว รวม 7,470 แถว
- จำนวนแถวไม่ใช่จำนวนสถานีไม่ซ้ำ เนื่องจากยังไม่ได้ตรวจความซ้ำของ `station_code`
- `id` ไม่อนุญาต NULL และมีค่าเริ่มต้นจาก sequence; คอลัมน์อื่นอนุญาต NULL ตาม schema
- `latitude` และ `longitude` เก็บเป็นข้อความ รวมถึงฟิลด์ `has_forecast_result` และ `is_used_in_forecast` ซึ่งไม่ได้เป็นชนิด boolean
- SRID ต่างจาก `MainBasin_Hydro_BPK` (`32647`); ต้องแปลงระบบพิกัดให้ตรงกันก่อน overlay และใช้ระบบพิกัดหรือชนิดข้อมูลที่เหมาะสมก่อนคำนวณระยะทาง
- ยังไม่ได้ตรวจสอบความครบถ้วนของสถานี หรือความถูกต้องและความครบถ้วนของพิกัด
- Metadata นี้เป็นข้อมูลอ้างอิง ณ วันที่ตรวจสอบ ควรตรวจ schema จริงอีกครั้งก่อนใช้งานที่ขึ้นกับโครงสร้างปัจจุบัน
