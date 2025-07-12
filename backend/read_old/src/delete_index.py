import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine, text
from config.database import DATABASE_URL

print(f"DATABASE_URL in use: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("\nTables in current database:")
    tables = conn.execute(text("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog');
    """)).fetchall()
    for t in tables:
        print(t)

    print("\nIndexes named idx_makro_locations_geom:")
    result = conn.execute(text("""
        SELECT schemaname, tablename, indexname
        FROM pg_indexes
        WHERE indexname = 'idx_makro_locations_geom';
    """)).fetchall()
    for row in result:
        print(row)

    conn.execute(text("DROP TABLE IF EXISTS makro_locations CASCADE;"))
    conn.commit()
    print("Table makro_locations dropped (with all related indexes, if existed).") 