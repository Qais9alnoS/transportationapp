import os
import requests

def get_traffic_data(start_lat, start_lng, end_lat, end_lng):
    """
    جلب بيانات الازدحام المروري بين نقطتين باستخدام Google Directions API (Traffic).
    حالياً: إذا لم يوجد مفتاح API، تعيد زمن إضافي وهمي (mock).
    لاحقاً: يمكن ربطها فعلياً مع Google Directions API.
    تعيد: زمن إضافي تقديري (بالثواني)
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_TRAFFIC_API_KEY")
    if not GOOGLE_API_KEY:
        # Mock: زمن إضافي عشوائي بين 0 و 10 دقائق
        import random
        return random.randint(0, 600)
    
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_lat},{start_lng}&destination={end_lat},{end_lng}"
        f"&departure_time=now&key={GOOGLE_API_KEY}"
    )
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("status") == "OK":
            # نأخذ أول مسار
            route = data["routes"][0]
            leg = route["legs"][0]
            duration = leg["duration"]["value"]  # زمن الرحلة بالثواني (بدون ازدحام)
            duration_in_traffic = leg.get("duration_in_traffic", {}).get("value", duration)
            extra = max(duration_in_traffic - duration, 0)
            return extra
        else:
            return 0  # إذا فشل الطلب، لا نضيف زمن إضافي
    except Exception:
        return 0 