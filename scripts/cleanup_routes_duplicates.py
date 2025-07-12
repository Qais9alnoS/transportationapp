import sqlalchemy
from sqlalchemy import create_engine, text

# عدل بيانات الاتصال إذا لزم
DB_URL = "postgresql://postgres:PostgreSQL@localhost:5432/makroji_db_clean"
engine = create_engine(DB_URL)

def get_duplicate_routes(conn):
    result = conn.execute(text('''
        SELECT name, array_agg(id ORDER BY id) as ids
        FROM routes
        GROUP BY name
        HAVING COUNT(*) > 1;
    '''))
    return result.fetchall()

def update_foreign_keys(conn, name, ids):
    main_id = ids[0]
    other_ids = ids[1:]
    if not other_ids:
        return
    # تحديث جميع الجداول المرتبطة
    for table, col in [
        ("route_paths", "route_id"),
        ("route_stops", "route_id"),
        ("complaints", "route_id"),
        ("feedback", "route_id")
    ]:
        conn.execute(text(f'''
            UPDATE {table}
            SET {col} = :main_id
            WHERE {col} = ANY(:other_ids)
        '''), {"main_id": main_id, "other_ids": other_ids})

def delete_duplicate_routes(conn, name, ids):
    main_id = ids[0]
    other_ids = ids[1:]
    if not other_ids:
        return
    conn.execute(text('''
        DELETE FROM routes WHERE id = ANY(:other_ids)
    '''), {"other_ids": other_ids})

with engine.begin() as conn:
    duplicates = get_duplicate_routes(conn)
    if not duplicates:
        print("لا يوجد تكرار في الأسماء.")
    else:
        for row in duplicates:
            name = row[0]
            ids = row[1]
            print(f"- {name} (معرفات: {ids})")
            update_foreign_keys(conn, name, ids)
            delete_duplicate_routes(conn, name, ids)
        print("تم تحديث العلاقات وحذف التكرارات بنجاح.") 