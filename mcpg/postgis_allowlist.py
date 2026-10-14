# Appended to mcpg.sql.allowlist during the image build.
# Explicit, read-only PostGIS operations. No wildcard st_* permissions.
# PostGIS is installed in public in this deployment. Other schemas are
# deliberately not admitted by this extension.
WATER_POSTGIS_FUNCTIONS = frozenset({
    # Overlay and aggregation
    "st_intersection", "st_union", "st_unaryunion", "st_collect",
    "st_difference", "st_symdifference",
    # Spatial predicates
    "st_intersects", "st_within", "st_contains", "st_covers",
    "st_coveredby", "st_disjoint", "st_touches", "st_overlaps",
    "st_equals", "st_dwithin",
    # Measurements and buffer
    "st_area", "st_length", "st_distance", "st_buffer",
    # Geometry validation / normalization (returns values; does not update rows)
    "st_isvalid", "st_isvalidreason", "st_isempty", "st_makevalid",
    "st_geometrytype", "st_srid", "st_transform",
    "st_collectionextract", "st_multi",
    # Construction and result serialization
    "st_geomfromtext", "st_makeenvelope", "st_astext", "st_asgeojson",
})
ALLOWED_FUNCTIONS.update(WATER_POSTGIS_FUNCTIONS)
ALLOWED_FUNCTIONS.update("public." + name for name in WATER_POSTGIS_FUNCTIONS)
