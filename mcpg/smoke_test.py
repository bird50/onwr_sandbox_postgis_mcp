"""Read-only MCP integration test. Usage: python3 mcpg/smoke_test.py [URL]."""
import json
import http.client
import math
import sys
import time
import urllib.error
import urllib.request


class Client:
    def __init__(self, url):
        self.url = url
        self.session = None
        self.request_id = 0
        result = self.request("initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "water-postgis-smoke-test", "version": "1.0"},
        })
        self.protocol = result["protocolVersion"]
        self.request("notifications/initialized", {}, notification=True)

    def request(self, method, params, notification=False):
        body = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notification:
            self.request_id += 1
            body["id"] = self.request_id
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        if hasattr(self, "protocol"):
            headers["MCP-Protocol-Version"] = self.protocol
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=45) as response:
            self.session = response.headers.get("Mcp-Session-Id", self.session)
            raw = response.read().decode()
        if notification:
            return None
        if raw.lstrip().startswith("{"):
            payload = json.loads(raw)
        else:
            events = [json.loads(line[6:]) for line in raw.splitlines()
                      if line.startswith("data: ")]
            payload = next(event for event in events if event.get("id") == body["id"])
        if "error" in payload:
            raise RuntimeError(payload["error"])
        return payload["result"]

    def select(self, sql):
        result = self.request("tools/call", {
            "name": "run_select", "arguments": {"sql": sql, "max_rows": 10},
        })
        if result.get("isError"):
            raise RuntimeError(result["content"])
        return result["structuredContent"]["rows"]


if __name__ == "__main__":
    # Container startup can take a few seconds, particularly under emulation.
    for attempt in range(15):
        try:
            client = Client(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8087/mcp")
            break
        except (urllib.error.URLError, http.client.RemoteDisconnected, ConnectionError):
            if attempt == 14:
                raise
            time.sleep(2)
    result = client.select("""
        WITH shapes AS (
          SELECT public.ST_MakeEnvelope(0, 0, 10, 10, 32647) AS a,
                 public.ST_MakeEnvelope(5, 0, 15, 10, 32647) AS b
        )
        SELECT ST_Area(ST_Intersection(a,b)) AS intersection,
               ST_Area(ST_Union(a,b)) AS union_area,
               ST_Area(ST_Difference(a,b)) AS difference,
               ST_Area(ST_SymDifference(a,b)) AS symmetric_difference,
               ST_Intersects(a,b) AS intersects,
               ST_Within(ST_Intersection(a,b),a) AS within,
               ST_Contains(a,ST_Intersection(a,b)) AS contains,
               ST_Covers(a,ST_Intersection(a,b)) AS covers,
               ST_CoveredBy(ST_Intersection(a,b),a) AS covered_by,
               ST_Disjoint(a,b) AS disjoint,
               ST_Touches(a,b) AS touches,
               ST_Overlaps(a,b) AS overlaps,
               ST_Equals(a,a) AS equals,
               ST_DWithin(a,b,1) AS dwithin,
               ST_Distance(a,b) AS distance,
               ST_Length(ST_GeomFromText('LINESTRING(0 0,3 4)',32647)) AS length,
               ST_Area(ST_Buffer(a,1)) > 100 AS buffer_expands,
               ST_Area(ST_UnaryUnion(ST_Collect(a,b))) AS dissolved,
               ST_IsValid(ST_MakeValid(a)) AS valid,
               ST_IsValidReason(a) AS validity_reason,
               ST_IsEmpty(ST_Difference(a,a)) AS empty_difference,
               ST_GeometryType(ST_Multi(ST_CollectionExtract(a,3))) AS geometry_type,
               ST_SRID(ST_Transform(ST_MakeEnvelope(700000,1500000,700010,1500010,32647),4326)) AS transformed_srid,
               ST_AsText(ST_Intersection(a,b)) AS wkt,
               ST_AsGeoJSON(ST_Intersection(a,b)) AS geojson
        FROM shapes
    """)[0]
    expected = {"intersection": 50, "union_area": 150, "difference": 50,
                "symmetric_difference": 100, "dissolved": 150,
                "distance": 0, "length": 5, "transformed_srid": 4326,
                "geometry_type": "ST_MultiPolygon", "validity_reason": "Valid Geometry"}
    for key, value in expected.items():
        assert result[key] == value, (key, result[key], value)
    for key in ("intersects", "within", "contains", "covers", "covered_by",
                "overlaps", "equals", "dwithin", "buffer_expands", "valid", "empty_difference"):
        assert result[key] is True, (key, result[key])
    for key in ("disjoint", "touches"):
        assert result[key] is False, (key, result[key])
    assert result["wkt"].startswith("POLYGON")
    assert json.loads(result["geojson"])["type"] == "Polygon"
    print("PASS: overlay, predicates, validation, transformation and serialization")

    row = client.select("SELECT current_database() AS db, current_user AS role, "
                        "current_setting('transaction_read_only') AS read_only")[0]
    assert row == {"db": "waterdb", "role": "mcpg_reader", "read_only": "on"}, row
    print("PASS: waterdb / mcpg_reader / read-only transaction")

    basin = client.select('''
        SELECT count(*) AS features, count(geom) AS nonnull_geometries,
               bool_and(ST_IsValid(geom)) AS valid,
               bool_or(ST_IsEmpty(geom)) AS any_empty,
               min(ST_SRID(geom)) AS min_srid, max(ST_SRID(geom)) AS max_srid,
               ST_Area(ST_Union(geom))/1600.0 AS rai
        FROM public."MainBasin_Hydro_BPK"
    ''')[0]
    assert basin["features"] > 0 and basin["nonnull_geometries"] == basin["features"], basin
    assert basin["valid"] and not basin["any_empty"], basin
    assert basin["min_srid"] == basin["max_srid"] == 32647, basin
    assert math.isfinite(basin["rai"]) and basin["rai"] > 0, basin
    print("PASS: live basin geometry", json.dumps(basin))
