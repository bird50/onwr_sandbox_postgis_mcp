FROM ghcr.io/devopam/mcpg:0.8.2

# Extend the policy data only; retain the upstream SQL validator and
# force_readonly transaction handling. Re-review on every base version change.
USER root
COPY postgis_allowlist.py /opt/water-postgis/postgis_allowlist.py
COPY test_policy.py /opt/water-postgis/test_policy.py
RUN python -c 'from pathlib import Path; from importlib.metadata import version; assert version("mcpg") == "0.8.2"; p = Path("/app/src/mcpg/sql/allowlist.py"); extension = Path("/opt/water-postgis/postgis_allowlist.py").read_text(); p.write_text(p.read_text() + "\n" + extension)'
USER mcpg
