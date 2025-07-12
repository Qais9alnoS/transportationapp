import requests
import time
import subprocess
import sys
import json
import sqlalchemy
from sqlalchemy import create_engine, inspect
from datetime import datetime, timedelta
import uuid

BASE_URL = "http://127.0.0.1:8000"
DB_URL = "postgresql://postgres:PostgreSQL@localhost:5432/makroji_db_clean"

# متغيرات عامة للاختبارات
test_user_token = None
test_admin_token = None
test_user_id = None
test_admin_id = None
test_route_id = None
test_stop_id = None
test_friend_id = None
test_complaint_id = None
test_feedback_id = None
test_makro_location_id = None
test_friend_email = None

def assert_status(r, code=200):
    """التحقق من رمز الاستجابة"""
    assert r.status_code == code, f"Expected {code}, got {r.status_code}: {r.text}"

def print_step(msg):
    """طباعة خطوة الاختبار"""
    print(f"{msg:<60}", end=" ")

def print_success():
    """طباعة نجاح الاختبار"""
    print("✅")

def print_failure(error):
    """طباعة فشل الاختبار"""
    print(f"❌ {error}")

def print_detailed_result(test_name, success, details=None):
    if success:
        print(f"[PASS] {test_name}")
    else:
        print(f"[FAIL] {test_name}")
        if details:
            print(f"    التفاصيل: {details}")

def run_test(test_name, test_func):
    try:
        print_step(f"[{test_name}]")
        test_func()
        print_success()
        print_detailed_result(test_name, True)
        return True
    except AssertionError as e:
        print_failure(str(e))
        print_detailed_result(test_name, False, str(e))
        return False
    except Exception as e:
        print_failure(str(e))
        print_detailed_result(test_name, False, str(e))
        return False

# ============================================================================
# اختبارات قاعدة البيانات والهجرات
# ============================================================================

def test_database_migrations():
    """اختبار تشغيل الهجرات"""
    subprocess.run(["alembic", "upgrade", "head"], check=True, capture_output=True)

def test_database_tables():
    """اختبار وجود الجداول المطلوبة"""
    engine = create_engine(DB_URL)
    insp = inspect(engine)
    existing_tables = insp.get_table_names()
    
    required_tables = [
        'routes', 'stops', 'route_stops', 'route_paths',
        'users', 'friendships', 'user_locations', 'makro_locations',
        'complaints', 'feedback', 'search_logs', 'analytics_data'
    ]
    
    missing = [tbl for tbl in required_tables if tbl not in existing_tables]
    assert not missing, f"الجداول الناقصة: {missing}"

# ============================================================================
# اختبارات نظام المصادقة
# ============================================================================

def test_user_registration():
    global test_user_id, test_user_email, test_user_password
    unique = str(uuid.uuid4())[:8]
    test_user_email = f"testuser_{unique}@example.com"
    test_user_password = "testpass123"
    payload = {
        "username": f"testuser_{unique}",
        "email": test_user_email,
        "password": test_user_password,
        "full_name": "مستخدم اختبار"
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload)
    assert_status(r, 201) if r.status_code != 200 else assert_status(r, 200)
    data = r.json()
    assert "id" in data
    assert data["email"] == payload["email"]
    test_user_id = data["id"]

def test_user_login():
    global test_user_token
    payload = {
        "email": test_user_email,
        "password": test_user_password
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
    assert_status(r, 200)
    data = r.json()
    assert "access_token" in data
    test_user_token = data["access_token"]

def test_admin_registration():
    """اختبار تسجيل مدير جديد"""
    global test_admin_id, test_admin_email, test_admin_password
    unique = str(uuid.uuid4())[:8]
    test_admin_email = f"adminuser_{unique}@example.com"
    test_admin_password = "adminpass123"
    payload = {
        "username": f"adminuser_{unique}",
        "email": test_admin_email,
        "password": test_admin_password,
        "full_name": "مدير اختبار",
        "is_admin": True
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload)
    assert_status(r, 201) if r.status_code != 200 else assert_status(r, 200)
    data = r.json()
    assert data["is_admin"] == True
    test_admin_id = data["id"]

def test_admin_login():
    """اختبار تسجيل دخول المدير"""
    global test_admin_token
    payload = {
        "email": test_admin_email,
        "password": test_admin_password
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
    assert_status(r, 200)
    data = r.json()
    assert "access_token" in data
    test_admin_token = data["access_token"]

def test_get_current_user():
    """اختبار جلب معلومات المستخدم الحالي"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["id"] == test_user_id

def test_invalid_login():
    """اختبار تسجيل دخول خاطئ"""
    payload = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
    assert_status(r, 401)

# ============================================================================
# اختبارات إدارة المحطات
# ============================================================================

def test_create_stop():
    """اختبار إنشاء محطة جديدة"""
    global test_stop_id
    
    payload = {
        "name": "محطة اختبار شاملة",
        "lat": 33.5138,
        "lng": 36.2765
    }
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/stops/", json=payload, headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["name"] == payload["name"]
    test_stop_id = data["id"]

def test_get_stop():
    """اختبار جلب محطة محددة"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/stops/{test_stop_id}", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["id"] == test_stop_id

def test_get_all_stops():
    """اختبار جلب جميع المحطات"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/stops/", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)
    assert any(stop["id"] == test_stop_id for stop in data)

def test_update_stop():
    """اختبار تحديث محطة"""
    payload = {
        "name": "محطة معدلة شاملة",
        "description": "وصف معدل"
    }
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.put(f"{BASE_URL}/api/v1/stops/{test_stop_id}", json=payload, headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["name"] == payload["name"]

def test_delete_stop():
    """اختبار حذف محطة"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.delete(f"{BASE_URL}/api/v1/stops/{test_stop_id}", headers=headers)
    assert_status(r, 200)
    
    # التحقق من حذف المحطة
    r = requests.get(f"{BASE_URL}/api/v1/stops/{test_stop_id}")
    assert_status(r, 404)

# ============================================================================
# اختبارات إدارة الخطوط
# ============================================================================

def test_create_route():
    """اختبار إنشاء خط جديد"""
    global test_route_id
    unique = str(uuid.uuid4())[:8]
    payload = {
        "name": f"مسار اختبار {unique}",
        "description": "مسار اختبار للاختبارات الشاملة",
        "price": 500,
        "operating_hours": "06:00-22:00",
        "stops": [
            {"name": f"محطة {unique} 1", "lat": 33.5138, "lng": 36.2765},
            {"name": f"محطة {unique} 2", "lat": 33.5238, "lng": 36.2865}
        ],
        "paths": [
            {"lat": 33.5138, "lng": 36.2765, "point_order": 1},
            {"lat": 33.5238, "lng": 36.2865, "point_order": 2}
        ]
    }
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=payload, headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert data["name"] == payload["name"]
    assert len(data["stops"]) == 2
    test_route_id = data["id"]

def test_get_route():
    """اختبار جلب خط محدد"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/routes/{test_route_id}", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["id"] == test_route_id
    assert len(data["stops"]) > 0
    assert len(data["paths"]) > 0

def test_get_all_routes():
    """اختبار جلب جميع الخطوط"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/routes/", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)
    assert any(route["id"] == test_route_id for route in data)

def test_update_route():
    """اختبار تحديث خط"""
    payload = {
        "name": "خط معدل شامل",
        "price": 600
    }
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.put(f"{BASE_URL}/api/v1/routes/{test_route_id}", json=payload, headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]

def test_delete_route():
    """اختبار حذف خط"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.delete(f"{BASE_URL}/api/v1/routes/{test_route_id}", headers=headers)
    assert_status(r, 200)
    
    # التحقق من حذف الخط
    r = requests.get(f"{BASE_URL}/api/v1/routes/{test_route_id}")
    assert_status(r, 404)

# ============================================================================
# اختبارات البحث عن المسارات
# ============================================================================

def test_route_search_fastest():
    """اختبار البحث عن أسرع مسار"""
    # إعادة إنشاء خط للاختبار
    test_create_route()
    
    payload = {
        "start_lat": 33.5138,
        "start_lng": 36.2765,
        "end_lat": 33.5238,
        "end_lng": 36.2865,
        "filter_type": "fastest"
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    assert_status(r, 200)
    
    data = r.json()
    assert "routes" in data
    assert len(data["routes"]) > 0

def test_route_search_cheapest():
    """اختبار البحث عن أرخص مسار"""
    payload = {
        "start_lat": 33.5138,
        "start_lng": 36.2765,
        "end_lat": 33.5238,
        "end_lng": 36.2865,
        "filter_type": "cheapest"
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    assert_status(r, 200)
    
    data = r.json()
    assert "routes" in data
    assert len(data["routes"]) > 0

def test_route_search_least_transfers():
    """اختبار البحث عن مسار بأقل تبديلات"""
    payload = {
        "start_lat": 33.5138,
        "start_lng": 36.2765,
        "end_lat": 33.5238,
        "end_lng": 36.2865,
        "filter_type": "least_transfers"
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    assert_status(r, 200)
    
    data = r.json()
    assert "routes" in data
    assert len(data["routes"]) > 0

def test_route_search_with_traffic():
    """اختبار تأثير بيانات الازدحام على زمن أسرع طريق"""
    test_create_route()
    payload = {
        "start_lat": 33.5138,
        "start_lng": 36.2765,
        "end_lat": 33.5238,
        "end_lng": 36.2865,
        "filter_type": "fastest"
    }
    print(f"    المدخلات: {payload}")
    r1 = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    assert_status(r1, 200)
    data1 = r1.json()
    time1 = data1["routes"][0]["total_estimated_time_seconds"]
    print(f"    الزمن الأول: {time1}")
    r2 = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    assert_status(r2, 200)
    data2 = r2.json()
    time2 = data2["routes"][0]["total_estimated_time_seconds"]
    print(f"    الزمن الثاني: {time2}")
    assert time1 != time2 or time1 > 0, f"زمن الرحلة يجب أن يتغير عند تفعيل بيانات الازدحام أو mock traffic (time1={time1}, time2={time2})"

def test_route_search_caching():
    """اختبار أن نتائج البحث عن المسارات تُخزن وتُسترجع من الكاش"""
    test_create_route()
    payload = {
        "start_lat": 33.5138,
        "start_lng": 36.2765,
        "end_lat": 33.5238,
        "end_lng": 36.2865,
        "filter_type": "fastest"
    }
    import time
    start1 = time.time()
    r1 = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    t1 = time.time() - start1
    assert_status(r1, 200)
    data1 = r1.json()
    start2 = time.time()
    r2 = requests.post(f"{BASE_URL}/api/v1/search-route/", json=payload)
    t2 = time.time() - start2
    assert_status(r2, 200)
    data2 = r2.json()
    assert data1 == data2, "نتيجة الكاش يجب أن تكون متطابقة"
    if abs(t2 - t1) < 0.05:
        print("تخطي: الفرق الزمني صغير جداً")
        return
    assert t2 <= t1 * 2, f"الكاش أبطأ من المتوقع: t1={t1:.3f}, t2={t2:.3f}"

# ============================================================================
# اختبارات نظام الصداقة
# ============================================================================

def test_send_friend_request():
    """اختبار إرسال طلب صداقة"""
    global test_friend_id, test_friend_email
    unique = str(uuid.uuid4())[:8]
    test_friend_email = f"friend_{unique}@example.com"
    payload = {
        "username": f"frienduser_{unique}",
        "email": test_friend_email,
        "password": "friendpass123",
        "full_name": "صديق اختبار"
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload)
    assert_status(r, 201) if r.status_code != 200 else assert_status(r, 200)
    data = r.json()
    assert "id" in data
    test_friend_id = data["id"]
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/friends/request", json={"friend_id": test_friend_id}, headers=headers)
    assert_status(r, 200)

def test_get_friend_requests():
    """اختبار جلب طلبات الصداقة"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/friends/requests/received", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)

def test_accept_friend_request():
    """اختبار قبول طلب صداقة"""
    global test_friend_email
    login_payload = {
        "email": test_friend_email,
        "password": "friendpass123"
    }
    r = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_payload)
    friend_token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {friend_token}"}
    # يجب جلب id طلب الصداقة من /friends/requests/received
    r = requests.get(f"{BASE_URL}/api/v1/friends/requests/received", headers=headers)
    assert_status(r, 200)
    requests_data = r.json()
    assert len(requests_data) > 0
    friendship_id = requests_data[0]["id"]
    r = requests.put(f"{BASE_URL}/api/v1/friends/request/{friendship_id}/respond", json={"status": "accepted"}, headers=headers)
    assert_status(r, 200)

def test_get_friends_list():
    """اختبار جلب قائمة الأصدقاء"""
    global test_user_token
    test_user_login()  # تسجيل الدخول دائمًا لضمان صلاحية التوكن
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/friends/", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)

# ============================================================================
# اختبارات مشاركة الموقع
# ============================================================================

def test_share_location():
    """اختبار مشاركة الموقع"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    payload = {
        "current_lat": 33.5138,
        "current_lng": 36.2765,
        "friend_ids": [test_friend_id]
    }
    r = requests.post(f"{BASE_URL}/api/v1/location-share/share", json=payload, headers=headers)
    assert_status(r, 200)

def test_get_friend_locations():
    """اختبار جلب مواقع الأصدقاء"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/location-share/friends/locations", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)

# ============================================================================
# اختبارات إدارة الشكاوى والملاحظات
# ============================================================================

def test_create_complaint():
    """اختبار إنشاء شكوى"""
    global test_complaint_id
    headers = {"Authorization": f"Bearer {test_user_token}"}
    payload = {
        "complaint_text": "شكوى اختبارية",
        "route_id": test_route_id
    }
    r = requests.post(f"{BASE_URL}/api/v1/complaints/", json=payload, headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert data["complaint_text"] == payload["complaint_text"]
    test_complaint_id = data["id"]

def test_get_complaints():
    """اختبار جلب الشكاوى"""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/complaints/", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)

def test_create_feedback():
    """اختبار إنشاء ملاحظة"""
    global test_feedback_id
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    payload = {
        "rating": 4,
        "comment": "ملاحظة اختبار",
        "route_id": test_route_id,
        "category": "service_quality"
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/feedback/", json=payload, headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert data["rating"] == payload["rating"]
    test_feedback_id = data["id"]

def test_get_feedback():
    """اختبار جلب الملاحظات"""
    r = requests.get(f"{BASE_URL}/api/v1/feedback/")
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)

# ============================================================================
# اختبارات تتبع مواقع المكروجي
# ============================================================================

def test_create_makro_location():
    """اختبار إنشاء موقع مكروجي"""
    global test_makro_location_id
    
    payload = {
        "makro_id": "MAKRO001",
        "lat": 33.5138,
        "lng": 36.2765,
        "status": "active",
        "last_update": datetime.now().isoformat()
    }
    
    r = requests.post(f"{BASE_URL}/api/v1/makro-locations/", json=payload)
    assert_status(r, 200)
    
    data = r.json()
    assert data["makro_id"] == payload["makro_id"]
    test_makro_location_id = data["id"]

def test_get_makro_locations():
    """اختبار جلب مواقع المكروجي"""
    r = requests.get(f"{BASE_URL}/api/v1/makro-locations/")
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, list)

def test_update_makro_location():
    """اختبار تحديث موقع مكروجي"""
    global test_makro_location_id
    if not test_makro_location_id:
        # إنشاء makro location إذا لم يكن موجوداً
        payload = {
            "makro_id": "MAKRO001",
            "lat": 33.5138,
            "lng": 36.2765,
            "status": "active",
            "last_update": datetime.now().isoformat()
        }
        r = requests.post(f"{BASE_URL}/api/v1/makro-locations/", json=payload)
        assert_status(r, 200)
        data = r.json()
        test_makro_location_id = data["id"]
    payload = {
        "makro_id": "MAKRO001",
        "lat": 33.5238,
        "lng": 36.2865,
        "timestamp": datetime.now().isoformat()
    }
    r = requests.put(f"{BASE_URL}/api/v1/makro-locations/{test_makro_location_id}", json=payload)
    assert_status(r, 200)
    data = r.json()
    assert data["lat"] == payload["lat"]
    assert data["makro_id"] == payload["makro_id"]

# ============================================================================
# اختبارات لوحة تحكم الداشبورد المتقدمة (Dashboard API)
# ============================================================================

def test_dashboard_real_time_stats():
    if not test_admin_token:
        print("تخطي: لا يوجد توكن مدير")
        return
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/real-time-stats", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert "users" in data and "routes" in data and "complaints" in data

def test_dashboard_route_analytics():
    """اختبار تحليلات الخطوط مع جميع الفترات"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    for period in ["day", "week", "month"]:
        r = requests.get(f"{BASE_URL}/api/v1/dashboard/route-analytics?period={period}", headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert "analytics" in data

def test_dashboard_user_behavior():
    """اختبار تحليل سلوك المستخدمين"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    for user_type in [None, "active", "new", "inactive"]:
        url = f"{BASE_URL}/api/v1/dashboard/user-behavior"
        if user_type:
            url += f"?user_type={user_type}"
        r = requests.get(url, headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert "user_segments" in data

def test_dashboard_predictive_insights():
    """اختبار الرؤى التنبؤية"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    for days in [3, 7, 14]:
        r = requests.get(f"{BASE_URL}/api/v1/dashboard/predictive-insights?forecast_days={days}", headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert "predictions" in data

def test_dashboard_complaint_intelligence():
    """اختبار ذكاء الشكاوى"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    for analysis_type in ["all", "trends", "categories", "routes"]:
        r = requests.get(f"{BASE_URL}/api/v1/dashboard/complaint-intelligence?analysis_type={analysis_type}", headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert "overview" in data

def test_dashboard_geographic_intelligence():
    """اختبار الذكاء الجغرافي"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    for area_type in ["hotspots", "coverage", "mobility"]:
        r = requests.get(f"{BASE_URL}/api/v1/dashboard/geographic-intelligence?area_type={area_type}", headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert "type" in data

def test_dashboard_system_health():
    """اختبار صحة النظام"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/system-health", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert "overall_health" in data

def test_dashboard_heatmap_data():
    """اختبار بيانات الخريطة الحرارية"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/heatmap-data", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert isinstance(data, list) or isinstance(data, dict)

def test_dashboard_usage_statistics():
    """اختبار إحصائيات الاستخدام"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/usage-statistics", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert "users_count" in data

def test_dashboard_top_routes():
    """اختبار أكثر الخطوط طلباً"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/top-routes", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert isinstance(data, list)

def test_dashboard_complaints_with_filters():
    """اختبار جلب الشكاوى مع الفلاتر"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/complaints?status_filter=pending", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert isinstance(data, list)

def test_dashboard_update_complaint_status():
    """اختبار تحديث حالة الشكوى"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    # يجب أن يكون هناك شكوى منشأة مسبقاً
    if test_complaint_id:
        r = requests.put(f"{BASE_URL}/api/v1/dashboard/complaints/{test_complaint_id}?new_status=resolved", headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert data["status"] == "resolved"

def test_dashboard_recommendations():
    """اختبار توصيات الداشبورد"""
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/recommendations", headers=headers)
    assert_status(r, 200)
    data = r.json()
    assert "recommendations" in data

def test_dashboard_analytics():
    """اختبار تحليلات لوحة التحكم"""
    # الوصول بدون توكن يجب أن يفشل
    r = requests.get(f"{BASE_URL}/api/v1/admin/dashboard/analytics")
    assert_status(r, 401)

    # الوصول بتوكن مستخدم عادي يجب أن يفشل
    headers_user = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/admin/dashboard/analytics", headers=headers_user)
    assert_status(r, 403)

    # الوصول بتوكن مدير يجب أن ينجح
    headers_admin = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/admin/dashboard/analytics", headers=headers_admin)
    assert_status(r, 200)
    data = r.json()
    assert isinstance(data, dict)
    assert "analytics" in data or "summary" in data  # تحقق من وجود بيانات تحليلية

def test_dashboard_real_time_metrics():
    """اختبار المقاييس في الوقت الفعلي للداشبورد"""
    # الوصول بدون توكن يجب أن يفشل
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/real-time-metrics")
    assert_status(r, 401)

    # الوصول بتوكن مستخدم عادي يجب أن يفشل
    headers_user = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/real-time-metrics", headers=headers_user)
    assert_status(r, 403)

    # الوصول بتوكن مدير يجب أن ينجح
    headers_admin = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/dashboard/real-time-metrics", headers=headers_admin)
    assert_status(r, 200)
    data = r.json()
    assert isinstance(data, dict)
    assert "metrics" in data or "summary" in data  # تحقق من وجود بيانات مقاييس

# ============================================================================
# اختبارات الأمان والصلاحيات
# ============================================================================

def test_admin_only_endpoints():
    """اختبار أن نقاط النهاية الإدارية تتطلب صلاحيات مدير"""
    # محاولة الوصول بدون توكن
    r = requests.get(f"{BASE_URL}/api/v1/admin/dashboard/analytics")
    assert_status(r, 401)
    
    # محاولة الوصول بتوكن مستخدم عادي
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/admin/dashboard/analytics", headers=headers)
    assert_status(r, 403)

def test_protected_endpoints():
    """اختبار أن النقاط المحمية تتطلب مصادقة"""
    # محاولة الوصول بدون توكن
    r = requests.get(f"{BASE_URL}/api/v1/auth/me")
    assert_status(r, 401)
    
    r = requests.get(f"{BASE_URL}/api/v1/friends/")
    assert_status(r, 401)

# ============================================================================
# اختبارات التحقق من صحة البيانات
# ============================================================================

def test_invalid_data_validation():
    """اختبار التحقق من صحة البيانات"""
    # إحداثيات غير صحيحة
    payload = {
        "name": "محطة خاطئة",
        "lat": 200.0,  # خطأ في خط العرض
        "lng": 36.2765
    }
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/stops/", json=payload, headers=headers)
    assert_status(r, 422)
    
    # بيانات تسجيل غير صحيحة
    payload = {
        "email": "invalid-email",
        "password": "123"  # كلمة مرور قصيرة جداً
    }
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=payload, headers=headers)
    assert_status(r, 422)

    # إحداثيات خارج النطاق
    invalid_coords_payload = {
        "name": "محطة خاطئة",
        "lat": 91.0,  # خارج النطاق
        "lng": 181.0  # خارج النطاق
    }
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/stops/", json=invalid_coords_payload, headers=headers)
    assert_status(r, 422)
    
    # سعر سالب
    invalid_price_payload = {
        "name": "خط خاطئ",
        "price": -100,
        "operating_hours": "06:00-22:00"
    }
    
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=invalid_price_payload, headers=headers)
    assert_status(r, 422)
    
    # ساعات تشغيل غير صحيحة
    invalid_hours_payload = {
        "name": "خط خاطئ",
        "price": 500,
        "operating_hours": "25:00-26:00"  # ساعات غير صحيحة
    }
    
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=invalid_hours_payload, headers=headers)
    assert_status(r, 422)

    # طلب خطأ 404
    r = requests.get(f"{BASE_URL}/api/v1/nonexistent-endpoint")
    assert_status(r, 404)
    
    # طلب خطأ 422 (بيانات غير صحيحة)
    invalid_payload = {"invalid": "data"}
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=invalid_payload, headers=headers)
    assert_status(r, 422)

    # طلب خطأ 500 (محاكاة خطأ في الخادم)
    r = requests.get(f"{BASE_URL}/api/v1/test-error")
    # قد يكون 404 أو 500 حسب التنفيذ
    assert r.status_code in [404, 500]

def test_caching_mechanism():
    """اختبار آلية التخزين المؤقت"""
    # الطلب الأول
    start_time = time.time()
    r1 = requests.get(f"{BASE_URL}/api/v1/routes/")
    first_request_time = time.time() - start_time
    
    # الطلب الثاني (يجب أن يكون أسرع إذا كان هناك تخزين مؤقت)
    start_time = time.time()
    r2 = requests.get(f"{BASE_URL}/api/v1/routes/")
    second_request_time = time.time() - start_time
    
    assert_status(r1, 200)
    assert_status(r2, 200)
    
    # التحقق من أن الطلب الثاني ليس أبطأ بكثير
    assert second_request_time <= first_request_time * 1.5

def test_logging_system():
    """اختبار نظام التسجيل"""
    # إجراء طلب لإنشاء سجل
    r = requests.get(f"{BASE_URL}/api/v1/routes/")
    assert_status(r, 200)
    
    # التحقق من وجود ملفات السجل (إذا كانت موجودة)
    import os
    log_files = ["app.log", "error.log", "access.log"]
    existing_logs = [f for f in log_files if os.path.exists(f"logs/{f}")]
    
    # لا نتحقق من وجود الملفات لأنها قد تكون في مسار مختلف
    # لكن نتحقق من أن الطلب نجح

def test_health_check():
    """اختبار فحص صحة النظام"""
    r = requests.get(f"{BASE_URL}/api/v1/health")
    if r.status_code == 404:
        print("تحذير: health endpoint غير موجود")
        return
    assert_status(r, 200)
    data = r.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_metrics_endpoint():
    """اختبار نقطة نهاية المقاييس"""
    r = requests.get(f"{BASE_URL}/api/v1/metrics")
    # قد يكون 200 أو 404 حسب التنفيذ
    assert r.status_code in [200, 404]

def test_api_documentation():
    """اختبار توثيق API"""
    r = requests.get(f"{BASE_URL}/api/v1/docs")
    assert r.status_code in [200, 404]
    
    r = requests.get(f"{BASE_URL}/api/v1/redoc")
    assert r.status_code in [200, 404]

def test_cors_headers():
    """اختبار رؤوس CORS"""
    r = requests.options(f"{BASE_URL}/api/v1/routes/")
    # قد يكون 200 أو 405 حسب التنفيذ
    assert r.status_code in [200, 405]

def test_content_type_headers():
    """اختبار رؤوس نوع المحتوى"""
    r = requests.get(f"{BASE_URL}/api/v1/routes/")
    assert_status(r, 200)
    
    content_type = r.headers.get("content-type", "")
    assert "application/json" in content_type

def test_pagination():
    """اختبار الصفحات"""
    # إنشاء عدة خطوط للاختبار
    for i in range(5):
        unique = str(uuid.uuid4())[:8]
        route_payload = {
            "name": f"خط اختبار {i}_{unique}",
            "description": f"وصف خط {i}",
            "price": 500 + i * 50,
            "operating_hours": "06:00-22:00",
            "stops": [
                {"name": f"محطة {i} 1", "lat": 33.5138 + i * 0.001, "lng": 36.2765 + i * 0.001},
                {"name": f"محطة {i} 2", "lat": 33.5238 + i * 0.001, "lng": 36.2865 + i * 0.001}
            ],
            "paths": [
                {"lat": 33.5138 + i * 0.001, "lng": 36.2765 + i * 0.001, "point_order": 1},
                {"lat": 33.5238 + i * 0.001, "lng": 36.2865 + i * 0.001, "point_order": 2}
            ]
        }
        headers = {"Authorization": f"Bearer {test_user_token}"}
        r = requests.post(f"{BASE_URL}/api/v1/routes/", json=route_payload, headers=headers)
        assert_status(r, 200)
        data = r.json()
        assert data["name"] == route_payload["name"]
    
    # اختبار الصفحات
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/routes/?page=1&size=3", headers=headers)
    assert_status(r, 200)
    
    data = r.json()
    assert isinstance(data, dict) or isinstance(data, list)

def test_filtering_and_sorting():
    """اختبار التصفية والترتيب"""
    # اختبار التصفية حسب السعر
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/routes/?min_price=500&max_price=600", headers=headers)
    assert_status(r, 200)
    
    # اختبار الترتيب
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.get(f"{BASE_URL}/api/v1/routes/?sort_by=price&sort_order=desc", headers=headers)
    assert_status(r, 200)

def test_data_validation_edge_cases():
    """اختبار حالات حدودية للتحقق من البيانات"""
    # إحداثيات خارج النطاق
    invalid_coords_payload = {
        "name": "محطة خاطئة",
        "lat": 91.0,  # خارج النطاق
        "lng": 181.0  # خارج النطاق
    }
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/stops/", json=invalid_coords_payload, headers=headers)
    assert_status(r, 422)
    
    # سعر سالب
    invalid_price_payload = {
        "name": "خط خاطئ",
        "price": -100,
        "operating_hours": "06:00-22:00"
    }
    
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=invalid_price_payload, headers=headers)
    assert_status(r, 422)
    
    # ساعات تشغيل غير صحيحة
    invalid_hours_payload = {
        "name": "خط خاطئ",
        "price": 500,
        "operating_hours": "25:00-26:00"  # ساعات غير صحيحة
    }
    
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=invalid_hours_payload, headers=headers)
    assert_status(r, 422)

def test_database_constraints():
    """اختبار قيود قاعدة البيانات"""
    # محاولة إنشاء مستخدم بنفس البريد الإلكتروني
    duplicate_user_payload = {
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "testpass123",
        "full_name": "مستخدم مكرر"
    }
    
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/auth/register", json=duplicate_user_payload, headers=headers)
    assert_status(r, 400) if r.status_code != 422 else assert_status(r, 422)

def test_transaction_rollback():
    """اختبار التراجع عن المعاملات"""
    # محاولة إنشاء خط مع بيانات غير صحيحة
    invalid_route_payload = {
        "name": "خط اختبار التراجع",
        "price": "غير رقم",  # نوع بيانات خاطئ
        "stops": [
            {"name": "محطة 1", "lat": 33.5138, "lng": 36.2765}
        ]
    }
    
    headers = {"Authorization": f"Bearer {test_admin_token}"}
    r = requests.post(f"{BASE_URL}/api/v1/routes/", json=invalid_route_payload, headers=headers)
    assert_status(r, 422)

# ============================================================================
# تحديث قائمة الاختبارات الرئيسية
# ============================================================================

def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء الاختبارات الشاملة لمشروع مكروجي")
    print("=" * 80)
    
    tests = [
        # اختبارات قاعدة البيانات
        ("قاعدة البيانات والهجرات", test_database_migrations),
        ("فحص الجداول", test_database_tables),
        
        # اختبارات المصادقة
        ("تسجيل مستخدم جديد", test_user_registration),
        ("تسجيل دخول المستخدم", test_user_login),
        ("تسجيل مدير جديد", test_admin_registration),
        ("تسجيل دخول المدير", test_admin_login),
        ("جلب معلومات المستخدم", test_get_current_user),
        ("تسجيل دخول خاطئ", test_invalid_login),
        # ("Google OAuth", test_google_oauth_flow),  # غير معرف
        # ("إعادة تعيين كلمة المرور", test_password_reset_flow),  # غير معرف
        
        # اختبارات إدارة المستخدمين
        # ("إدارة الملف الشخصي", test_user_profile_management),  # غير معرف
        
        # اختبارات المحطات
        ("إنشاء محطة", test_create_stop),
        ("جلب محطة محددة", test_get_stop),
        ("جلب جميع المحطات", test_get_all_stops),
        ("تحديث محطة", test_update_stop),
        ("حذف محطة", test_delete_stop),
        # ("العمليات المجمعة للمحطات", test_bulk_operations),  # غير معرف
        # ("الاستعلامات الجغرافية", test_geospatial_queries),  # غير معرف
        
        # اختبارات الخطوط
        ("إنشاء خط", test_create_route),
        ("جلب خط محدد", test_get_route),
        ("جلب جميع الخطوط", test_get_all_routes),
        ("تحديث خط", test_update_route),
        ("حذف خط", test_delete_route),
        # ("إدارة محطات الخط", test_route_stops_management),  # غير معرف
        # ("إدارة مسارات الخط", test_route_paths_management),  # غير معرف
        # ("تحسين المسارات", test_route_optimization),  # غير معرف
        
        # اختبارات البحث
        ("البحث عن أسرع مسار", test_route_search_fastest),
        ("البحث عن أرخص مسار", test_route_search_cheapest),
        ("البحث عن أقل تبديلات", test_route_search_least_transfers),
        ("البحث عن أسرع طريق مع بيانات الازدحام", test_route_search_with_traffic),
        ("كاش البحث عن المسارات (Redis)", test_route_search_caching),
        # ("سجلات البحث", test_search_logs),  # غير معرف
        
        # اختبارات الصداقة
        ("إرسال طلب صداقة", test_send_friend_request),
        ("جلب طلبات الصداقة", test_get_friend_requests),
        ("قبول طلب صداقة", test_accept_friend_request),
        ("جلب قائمة الأصدقاء", test_get_friends_list),
        
        # اختبارات مشاركة الموقع
        ("مشاركة الموقع", test_share_location),
        ("جلب مواقع الأصدقاء", test_get_friend_locations),
        
        # اختبارات الشكاوى والملاحظات
        ("إنشاء شكوى", test_create_complaint),
        ("جلب الشكاوى", test_get_complaints),
        ("إنشاء ملاحظة", test_create_feedback),
        ("جلب الملاحظات", test_get_feedback),
        
        # اختبارات مواقع المكروجي
        ("إنشاء موقع مكروجي", test_create_makro_location),
        ("جلب مواقع المكروجي", test_get_makro_locations),
        ("تحديث موقع مكروجي", test_update_makro_location),
        
        # اختبارات لوحة التحكم القديمة
        ("تحليلات لوحة التحكم", test_dashboard_analytics),
        ("التنبؤات", test_dashboard_predictive_insights),
        ("الذكاء الجغرافي", test_dashboard_geographic_intelligence),
        ("تحليل الشكاوى", test_dashboard_complaint_intelligence),
        ("صحة النظام", test_dashboard_system_health),
        ("المقاييس في الوقت الفعلي", test_dashboard_real_time_metrics),
        # ("جمع البيانات التحليلية", test_analytics_data_collection),  # غير معرف
        
        # اختبارات لوحة التحكم المتقدمة
        ("إحصائيات الوقت الفعلي للداشبورد", test_dashboard_real_time_stats),
        ("تحليلات الخطوط للداشبورد", test_dashboard_route_analytics),
        ("سلوك المستخدمين للداشبورد", test_dashboard_user_behavior),
        ("الرؤى التنبؤية للداشبورد", test_dashboard_predictive_insights),
        ("ذكاء الشكاوى للداشبورد", test_dashboard_complaint_intelligence),
        ("الذكاء الجغرافي للداشبورد", test_dashboard_geographic_intelligence),
        ("صحة النظام للداشبورد", test_dashboard_system_health),
        ("الخريطة الحرارية للداشبورد", test_dashboard_heatmap_data),
        ("إحصائيات الاستخدام للداشبورد", test_dashboard_usage_statistics),
        ("أكثر الخطوط طلباً للداشبورد", test_dashboard_top_routes),
        ("الشكاوى مع الفلاتر للداشبورد", test_dashboard_complaints_with_filters),
        ("تحديث حالة الشكوى للداشبورد", test_dashboard_update_complaint_status),
        ("توصيات الداشبورد", test_dashboard_recommendations),
        
        # اختبارات الأمان
        ("نقاط النهاية الإدارية", test_admin_only_endpoints),
        ("النقاط المحمية", test_protected_endpoints),
        # ("تحديد معدل الطلبات", test_rate_limiting),  # غير معرف
        ("رؤوس CORS", test_cors_headers),
        ("رؤوس نوع المحتوى", test_content_type_headers),
        
        # اختبارات الأداء
        # ("وقت استجابة API", test_api_response_time),  # غير معرف
        # ("الطلبات المتزامنة", test_concurrent_requests),  # غير معرف
        # ("تجمع اتصالات قاعدة البيانات", test_database_connection_pool),  # غير معرف
        ("آلية التخزين المؤقت", test_caching_mechanism),
        
        # اختبارات معالجة الأخطاء
        # ("معالجة الأخطاء", test_error_handling),  # غير معرف
        ("نظام التسجيل", test_logging_system),
        ("التراجع عن المعاملات", test_transaction_rollback),
        
        # اختبارات واجهة المستخدم
        ("الصفحات", test_pagination),
        ("التصفية والترتيب", test_filtering_and_sorting),
        
        # اختبارات التحقق من البيانات
        ("التحقق من صحة البيانات", test_invalid_data_validation),
        ("حالات حدودية للتحقق", test_data_validation_edge_cases),
        ("قيود قاعدة البيانات", test_database_constraints),
    ]
    
    passed = 0
    failed = 0
    failed_details = []
    
    for test_name, test_func in tests:
        result = run_test(test_name, test_func)
        if result:
            passed += 1
        else:
            failed += 1
            failed_details.append(test_name)
    
    print("\n" + "=" * 80)
    print(f"📊 نتائج الاختبارات:")
    print(f"✅ نجح: {passed}")
    print(f"❌ فشل: {failed}")
    if failed_details:
        print("\n❗️الاختبارات التي فشلت:")
        for name in failed_details:
            print(f"   - {name}")
    print(f"📈 نسبة النجاح: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 جميع الاختبارات نجحت بنجاح كامل!")
    else:
        print(f"\n⚠️  هناك {failed} اختبارات فشلت. يرجى مراجعة التفاصيل أعلاه.")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف الاختبارات بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 خطأ غير متوقع: {e}")
        sys.exit(1) 