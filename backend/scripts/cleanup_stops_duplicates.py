import sqlalchemy
from sqlalchemy import create_engine, text

DB_URL = "postgresql://postgres:PostgreSQL@localhost:5432/makroji_db_clean"
engine = create_engine(DB_URL)

def get_duplicate_stops(conn):
    result = conn.execute(text('''
        SELECT name, array_agg(id ORDER BY id) as ids
        FROM stops
        GROUP BY name
        HAVING COUNT(*) > 1;
    '''))
    return result.fetchall()

def update_foreign_keys(conn, name, ids):
    main_id = ids[0]
    other_ids = ids[1:]
    if not other_ids:
        return
    # تحديث stop_id فقط في route_stops
    conn.execute(text('''
        UPDATE route_stops
        SET stop_id = :main_id
        WHERE stop_id = ANY(:other_ids)
    '''), {"main_id": main_id, "other_ids": other_ids})

def delete_duplicate_stops(conn, name, ids):
    main_id = ids[0]
    other_ids = ids[1:]
    if not other_ids:
        return
    conn.execute(text('''
        DELETE FROM stops WHERE id = ANY(:other_ids)
    '''), {"other_ids": other_ids})

with engine.begin() as conn:
    duplicates = get_duplicate_stops(conn)
    if not duplicates:
        print("لا يوجد تكرار في الأسماء.")
    else:
        for row in duplicates:
            name = row[0]
            ids = row[1]
            print(f"- {name} (معرفات: {ids})")
            update_foreign_keys(conn, name, ids)
            delete_duplicate_stops(conn, name, ids)
        print("تم تحديث العلاقات وحذف التكرارات بنجاح.") 