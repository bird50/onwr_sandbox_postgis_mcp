"""Regression checks for the local policy extension; run inside the image."""
import asyncio
import unittest

from mcpg.sql.allowlist import ALLOWED_FUNCTIONS, WATER_POSTGIS_FUNCTIONS
from mcpg.sql.safety import SafeSqlDriver


class RecordingDriver:
    def __init__(self):
        self.calls = []

    async def execute_query(self, query, **kwargs):
        self.calls.append((query, kwargs))
        return []


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.backend = RecordingDriver()
        self.driver = SafeSqlDriver(self.backend)

    def test_overlay_and_cte(self):
        self.driver._validate('''
            WITH bounds AS (
              SELECT public.ST_MakeEnvelope(0, 0, 10, 10, 32647) AS geom
            )
            SELECT ST_Area(ST_Intersection(a.geom, b.geom))
            FROM bounds a JOIN bounds b ON ST_Intersects(a.geom, b.geom)
        ''')

    def test_public_and_unqualified_functions(self):
        for name in WATER_POSTGIS_FUNCTIONS:
            for prefix in ("", "public."):
                with self.subTest(name=prefix + name):
                    # Validator-only: arity/type correctness is tested live.
                    self.driver._validate(f"SELECT {prefix}{name}(NULL)")

    def test_write_and_unapproved_functions_rejected(self):
        queries = [
            'DELETE FROM public."MainBasin_Hydro_BPK"',
            'UPDATE public."MainBasin_Hydro_BPK" SET geom = NULL',
            'INSERT INTO x VALUES (1)',
            'DROP TABLE x',
            'CREATE TABLE x (id integer)',
            'SELECT * FROM x FOR UPDATE',
            'WITH x AS (DELETE FROM y RETURNING *) SELECT * FROM x',
            'SELECT pg_sleep(1)',
            "SELECT pg_read_file('/etc/passwd')",
            'SELECT ST_Intersection(geom, pg_sleep(1)) FROM x',
            'SELECT other_schema.ST_Area(NULL)',
            "SELECT UpdateGeometrySRID('x', 'geom', 4326)",
        ]
        for query in queries:
            with self.subTest(query=query), self.assertRaises(ValueError):
                asyncio.run(self.driver.execute_query(query))
        self.assertEqual(self.backend.calls, [])
        self.assertNotIn("st_*", ALLOWED_FUNCTIONS)

    def test_execution_still_forces_readonly(self):
        asyncio.run(self.driver.execute_query(
            "SELECT ST_Area(NULL::geometry)", force_readonly=False, row_limit=2
        ))
        self.assertEqual(len(self.backend.calls), 1)
        self.assertTrue(self.backend.calls[0][1]["force_readonly"])
        self.assertEqual(self.backend.calls[0][1]["row_limit"], 2)


if __name__ == "__main__":
    unittest.main()
