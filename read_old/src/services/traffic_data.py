"""
خدمة بيانات الازدحام المروري (Google Directions/Distance Matrix)

- ضع مفتاح Google API الخاص بك في المتغير GOOGLE_API_KEY أدناه.
- استخدم الدوال get_directions_with_traffic وget_distance_matrix_with_traffic لجلب بيانات المسارات والزمن مع الازدحام.
- ما زالت دالة get_mock_traffic_data موجودة للاختبار.
"""
from typing import List, Dict
import requests
import os
import random

class BaseTrafficProvider:
    def get_directions(self, origin_lat, origin_lng, dest_lat, dest_lng, departure_time="now"):
        raise NotImplementedError
    def get_distance_matrix(self, origins: List[Dict], destinations: List[Dict], departure_time="now"):
        raise NotImplementedError
    def get_traffic_data(self, path: List[Dict]) -> List[Dict]:
        raise NotImplementedError

class GoogleTrafficProvider(BaseTrafficProvider):
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY", "ضع_مفتاحك_هنا")
    def get_directions(self, origin_lat, origin_lng, dest_lat, dest_lng, departure_time="now"):
        url = (
            f"https://maps.googleapis.com/maps/api/directions/json?"
            f"origin={origin_lat},{origin_lng}&destination={dest_lat},{dest_lng}"
            f"&departure_time={departure_time}&key={self.api_key}"
        )
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    def get_distance_matrix(self, origins: List[Dict], destinations: List[Dict], departure_time="now"):
        origins_str = "|".join([f"{o['lat']},{o['lng']}" for o in origins])
        destinations_str = "|".join([f"{d['lat']},{d['lng']}" for d in destinations])
        url = (
            f"https://maps.googleapis.com/maps/api/distancematrix/json?"
            f"origins={origins_str}&destinations={destinations_str}"
            f"&departure_time={departure_time}&key={self.api_key}"
        )
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    def get_traffic_data(self, path: List[Dict]) -> List[Dict]:
        # Google API لا تدعم هذا مباشرة، يمكن التخصيص لاحقًا
        return []

class MockTrafficProvider(BaseTrafficProvider):
    def get_directions(self, origin_lat, origin_lng, dest_lat, dest_lng, departure_time="now"):
        # تعيد بيانات وهمية
        return {
            "routes": [
                {
                    "legs": [
                        {
                            "duration": {"value": 600},
                            "duration_in_traffic": {"value": 900}
                        }
                    ]
                }
            ],
            "status": "OK"
        }
    def get_distance_matrix(self, origins: List[Dict], destinations: List[Dict], departure_time="now"):
        # بيانات وهمية
        return {"rows": []}
    def get_traffic_data(self, path: List[Dict]) -> List[Dict]:
        traffic_data = []
        for point in path:
            traffic_data.append({
                "lat": point["lat"],
                "lng": point["lng"],
                "traffic_level": random.randint(1, 5)
            })
        return traffic_data

def get_traffic_provider():
    provider = os.getenv("TRAFFIC_PROVIDER", "google").lower()
    if provider == "google":
        return GoogleTrafficProvider()
    elif provider == "mock":
        return MockTrafficProvider()
    # يمكن إضافة مزودات أخرى هنا
    else:
        return MockTrafficProvider()  # fallback

# واجهة موحدة للاستخدام في باقي الكود:
traffic_provider = get_traffic_provider()

def get_directions_with_traffic(origin_lat, origin_lng, dest_lat, dest_lng, departure_time="now"):
    return traffic_provider.get_directions(origin_lat, origin_lng, dest_lat, dest_lng, departure_time)

def get_distance_matrix_with_traffic(origins: List[Dict], destinations: List[Dict], departure_time="now"):
    return traffic_provider.get_distance_matrix(origins, destinations, departure_time)

def get_mock_traffic_data(path: List[Dict]) -> List[Dict]:
    return traffic_provider.get_traffic_data(path)