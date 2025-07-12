import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine, text
from config.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_makro_locations_geom ON makro_locations USING gist (geom);
    """))
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_stops_geom ON stops USING gist (geom);
    """))
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_route_paths_geom ON route_paths USING gist (geom);
    """))
    conn.commit()
    print("GiST indexes created (if not already present).") 