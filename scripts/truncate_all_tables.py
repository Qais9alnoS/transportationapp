import sqlalchemy
from sqlalchemy import create_engine, text

DB_URL = "postgresql://postgres:PostgreSQL@localhost:5432/makroji_db_clean"
engine = create_engine(DB_URL)

tables = [
    'route_stops',
    'route_paths',
    'friendships',
    'location_shares',
    'makro_locations',
    'search_logs',
    'complaints',
    'feedback',
    'stops',
    'routes',
    'users',
    'user_locations',
    'analytics_data'
]

with engine.begin() as conn:
    conn.execute(text('SET session_replication_role = replica;'))
    for table in tables:
        print(f"Truncating {table} ...")
        conn.execute(text(f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;'))
    conn.execute(text('SET session_replication_role = DEFAULT;'))
    print("تم حذف جميع البيانات التجريبية وإعادة تعيين العدادات بنجاح.")
    # تصحيح جميع قيم operating_hours لتكون بصيغة HH:MM-HH:MM
    print("تصحيح قيم operating_hours في جدول routes ...")
    conn.execute(text('''
        UPDATE routes
        SET operating_hours =
            LPAD(SPLIT_PART(operating_hours, '-', 1), 5, '0') || '-' || LPAD(SPLIT_PART(operating_hours, '-', 2), 5, '0')
        WHERE operating_hours IS NOT NULL AND operating_hours !~ '^[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}$';
    '''))
    print("تم تصحيح جميع القيم غير المطابقة في operating_hours.") 