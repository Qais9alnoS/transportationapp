# تحليل APIs مشاركة الموقع والبحث

## تحليل ملف `src/routers/location_share.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بمشاركة الموقع بين المستخدمين في النظام. يوفر إنشاء مشاركات الموقع، تحديثها، إلغاؤها، وجلب المشاركات النشطة. يعتمد على FastAPI وSQLAlchemy مع دعم البيانات الجغرافية.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /location-share/ | إنشاء مشاركة موقع جديدة | [create_location_share](#create_location_share) |
| GET     | /location-share/ | جلب مشاركات الموقع للمستخدم | [get_location_shares](#get_location_shares) |
| GET     | /location-share/shared-with-me | جلب المشاركات الموجهة للمستخدم | [get_shared_with_me](#get_shared_with_me) |
| PUT     | /location-share/{share_id} | تحديث مشاركة موقع | [update_location_share](#update_location_share) |
| DELETE  | /location-share/{share_id} | إلغاء مشاركة موقع | [cancel_location_share](#cancel_location_share) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_location_share"></a>1. إنشاء مشاركة موقع جديدة
- **المسار:** `/location-share/`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن من نوع `LocationShareCreate` (current_lat, current_lng, destination_lat, destination_lng, destination_name, estimated_arrival, message, duration_hours, friend_ids)
- **المخرجات:**
  - قائمة من كائنات `LocationShareResponse`
- **المنطق:**
  - ينشئ مشاركة موقع منفصلة لكل صديق في القائمة.
  - يحسب وقت انتهاء المشاركة بناءً على duration_hours.
  - يحفظ الإحداثيات كنقاط جغرافية.
- **أمثلة:**
```json
POST /location-share/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "current_lat": 33.5,
  "current_lng": 36.3,
  "destination_lat": 33.6,
  "destination_lng": 36.4,
  "destination_name": "Home",
  "estimated_arrival": "2024-01-01T15:30:00",
  "message": "On my way home",
  "duration_hours": 2,
  "friend_ids": [2, 3]
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من وجود الأصدقاء.

---

#### <a name="get_location_shares"></a>2. جلب مشاركات الموقع للمستخدم
- **المسار:** `/location-share/`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب جميع مشاركات الموقع التي أنشأها المستخدم الحالي.
  - يشمل تفاصيل المستخدمين المشارك معهم.
- **أمثلة:**
```http
GET /location-share/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، يعرض فقط مشاركات المستخدم.

---

#### <a name="get_shared_with_me"></a>3. جلب المشاركات الموجهة للمستخدم
- **المسار:** `/location-share/shared-with-me`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب جميع مشاركات الموقع الموجهة للمستخدم الحالي.
  - يشمل تفاصيل المستخدمين الذين شاركوا معه.
- **أمثلة:**
```http
GET /location-share/shared-with-me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، يعرض فقط المشاركات الموجهة للمستخدم.

---

#### <a name="update_location_share"></a>4. تحديث مشاركة موقع
- **المسار:** `/location-share/{share_id}`
- **الطريقة:** PUT
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: share_id (int)
  - Body: كائن من نوع `LocationShareUpdate`
- **المخرجات:**
  - كائن من نوع `LocationShareResponse` بعد التحديث
- **المنطق:**
  - يتحقق من ملكية المستخدم للمشاركة.
  - يحدث الحقول المطلوبة فقط.
  - يحدث الإحداثيات كنقاط جغرافية إذا تم تغييرها.
- **أمثلة:**
```json
PUT /location-share/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "current_lat": 33.55,
  "current_lng": 36.35,
  "message": "Updated location"
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من الملكية.

---

#### <a name="cancel_location_share"></a>5. إلغاء مشاركة موقع
- **المسار:** `/location-share/{share_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: share_id (int)
- **المخرجات:**
  - {"message": "Location share cancelled successfully"}
- **المنطق:**
  - يتحقق من ملكية المستخدم للمشاركة.
  - يغير حالة المشاركة إلى "cancelled".
- **أمثلة:**
```http
DELETE /location-share/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من الملكية.

---

### استنتاجات تقنية وتحليل أمني
- نظام مشاركة موقع متكامل مع دعم البيانات الجغرافية.
- حماية جميع العمليات بالمصادقة.
- التحقق من ملكية المشاركات قبل التحديث أو الإلغاء.
- دعم مشاركة الموقع مع عدة أصدقاء في طلب واحد.
- نظام انتهاء صلاحية تلقائي للمشاركات.

---

### توصيات
- إضافة إشعارات فورية للأصدقاء عند المشاركة أو التحديث.
- إضافة نظام تتبع الموقع في الوقت الفعلي.
- إضافة حد أقصى لعدد المشاركات النشطة.
- تحسين الأداء بإضافة فهارس على الحقول الجغرافية.
- إضافة نظام خصوصية لتحديد من يمكنه مشاركة الموقع معه.

---

## تحليل ملف `src/routers/search.py`

### نظرة عامة

هذا الملف مسؤول عن نقطة النهاية الرئيسية للبحث عن خطوط النقل في النظام. يوفر خوارزمية بحث متقدمة تجد أفضل المسارات بين نقطتين جغرافيتين، مع دعم أنواع مختلفة من الفلترة (أسرع، أرخص، أقل تنقلات). يعتمد على FastAPI وSQLAlchemy مع حسابات جغرافية معقدة.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /search-route/ | البحث عن خطوط النقل | [search_route](#search_route) |

---

### تحليل وتوثيق API البحث بالتفصيل

#### <a name="search_route"></a>1. البحث عن خطوط النقل
- **المسار:** `/search-route/`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `SearchRouteRequest` (start_lat, start_lng, end_lat, end_lng, filter_type)
- **المخرجات:**
  - كائن من نوع `SearchRouteResponse` (routes)
- **المنطق:**
  - يجد المحطات القريبة من نقطة البداية والنهاية (ضمن نصف قطر 2 كم).
  - يبحث عن الخطوط التي تمر بهذه المحطات.
  - يحسب المسارات المقترحة مع تفاصيل كل مقطع (مشي، مكرو، مشي).
  - يرتب النتائج حسب نوع الفلترة المطلوبة.
  - يسجل عملية البحث في جدول search_logs.

---

### خوارزمية البحث المفصلة

#### الخطوة 1: العثور على المحطات القريبة
```python
# البحث عن محطات ضمن نصف قطر 2 كم من نقطة البداية
start_stops = find_nearby_stops(start_lat, start_lng, radius=2.0)
# البحث عن محطات ضمن نصف قطر 2 كم من نقطة النهاية  
end_stops = find_nearby_stops(end_lat, end_lng, radius=2.0)
```

#### الخطوة 2: العثور على الخطوط المشتركة
```python
# البحث عن الخطوط التي تمر بمحطات البداية والنهاية
common_routes = find_routes_with_stops(start_stops, end_stops)
```

#### الخطوة 3: بناء المسارات المقترحة
لكل خط مشترك، يتم بناء مسار مكون من 3 مقاطع:
1. **مقطع المشي الأول:** من نقطة البداية إلى أقرب محطة
2. **مقطع المكرو:** من محطة البداية إلى محطة النهاية عبر الخط
3. **مقطع المشي الأخير:** من محطة النهاية إلى نقطة الوصول

#### الخطوة 4: حساب التفاصيل لكل مقطع
```python
# مقطع المشي الأول
walking_segment_1 = {
    "type": "walking",
    "distance": haversine_distance(start_point, start_stop),
    "duration": walking_time_calculation,
    "instructions": f"Walk to {start_stop.name}",
    "estimated_cost": 0
}

# مقطع المكرو
makro_segment = {
    "type": "makro",
    "distance": route_distance_calculation,
    "duration": route_time_calculation,
    "instructions": f"Take {route.name} from {start_stop.name} to {end_stop.name}",
    "makro_id": route.id,
    "start_stop_id": start_stop.id,
    "end_stop_id": end_stop.id,
    "estimated_cost": route.price
}

# مقطع المشي الأخير
walking_segment_2 = {
    "type": "walking", 
    "distance": haversine_distance(end_stop, end_point),
    "duration": walking_time_calculation,
    "instructions": f"Walk from {end_stop.name} to destination",
    "estimated_cost": 0
}
```

#### الخطوة 5: ترتيب النتائج حسب نوع الفلترة
```python
if filter_type == "fastest":
    routes.sort(key=lambda x: x.total_estimated_time_seconds)
elif filter_type == "cheapest":
    routes.sort(key=lambda x: x.total_estimated_cost)
elif filter_type == "least_transfers":
    routes.sort(key=lambda x: len([s for s in x.segments if s.type == "makro"]))
```

---

### أمثلة عملية

#### مثال 1: البحث عن أسرع مسار
```json
POST /search-route/
{
  "start_lat": 33.5,
  "start_lng": 36.3,
  "end_lat": 33.6,
  "end_lng": 36.4,
  "filter_type": "fastest"
}
```

#### مثال على الاستجابة
```json
{
  "routes": [
    {
      "route_id": 1,
      "description": "Route via Line 1",
      "segments": [
        {
          "type": "walking",
          "distance": 0.5,
          "duration": 360,
          "instructions": "Walk to Stop A",
          "estimated_cost": 0
        },
        {
          "type": "makro",
          "distance": 5.2,
          "duration": 900,
          "instructions": "Take Line 1 from Stop A to Stop B",
          "makro_id": 1,
          "start_stop_id": 1,
          "end_stop_id": 2,
          "estimated_cost": 1000
        },
        {
          "type": "walking",
          "distance": 0.3,
          "duration": 216,
          "instructions": "Walk from Stop B to destination",
          "estimated_cost": 0
        }
      ],
      "total_estimated_time_seconds": 1476,
      "total_estimated_cost": 1000
    }
  ]
}
```

---

### الحسابات الجغرافية المستخدمة

#### معادلة Haversine للمسافة
```python
def haversine_distance(lat1, lng1, lat2, lng2):
    """
    حساب المسافة بين نقطتين جغرافيتين بالكيلومتر
    """
    R = 6371  # نصف قطر الأرض بالكيلومتر
    
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlng/2) * math.sin(dlng/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance
```

#### حساب وقت المشي
```python
def calculate_walking_time(distance_km):
    """
    حساب وقت المشي بناءً على سرعة 5 كم/ساعة
    """
    walking_speed_kmh = 5.0
    time_hours = distance_km / walking_speed_kmh
    return int(time_hours * 3600)  # تحويل إلى ثواني
```

#### حساب وقت المكرو
```python
def calculate_makro_time(distance_km):
    """
    حساب وقت المكرو بناءً على سرعة 30 كم/ساعة
    """
    makro_speed_kmh = 30.0
    time_hours = distance_km / makro_speed_kmh
    return int(time_hours * 3600)  # تحويل إلى ثواني
```

---

### تسجيل عمليات البحث

يتم تسجيل كل عملية بحث في جدول `search_logs` مع التفاصيل التالية:
- إحداثيات البداية والنهاية
- نوع الفلترة المستخدمة
- وقت تنفيذ البحث
- عدد النتائج المعادة

```python
search_log = SearchLog(
    start_lat=request.start_lat,
    start_lng=request.start_lng,
    end_lat=request.end_lat,
    end_lng=request.end_lng,
    filter_type=request.filter_type,
    execution_time_ms=execution_time,
    results_count=len(suggested_routes)
)
```

---

### استنتاجات تقنية وتحليل أمني
- خوارزمية بحث متقدمة تدعم أنواع مختلفة من الفلترة.
- حسابات جغرافية دقيقة باستخدام معادلة Haversine.
- تسجيل شامل لعمليات البحث لأغراض التحليل والتحسين.
- لا يتطلب مصادقة، مما يجعله متاحًا للجميع.
- دعم للمسارات المعقدة مع عدة مقاطع.

---

### توصيات
- تحسين الأداء باستخدام فهارس جغرافية (PostGIS).
- إضافة دعم للمسارات متعددة الخطوط (transfers).
- إضافة معلومات الازدحام والتأخير في الحسابات.
- إضافة كاش للبحثات المتكررة.
- تحسين خوارزمية البحث لتشمل عوامل أخرى مثل الراحة والأمان.
- إضافة rate limiting لمنع إساءة الاستخدام.

---

## تحليل ملف `src/routers/makro_locations.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة مواقع المكاري (Makro Locations) في النظام. يوفر تسجيل مواقع المكاري، جلب المواقع الحديثة، والبحث عن المكاري القريبة. يعتمد على FastAPI وSQLAlchemy مع دعم البيانات الجغرافية.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /makro-locations/ | تسجيل موقع مكرو جديد | [create_makro_location](#create_makro_location) |
| GET     | /makro-locations/ | جلب جميع مواقع المكاري | [get_makro_locations](#get_makro_locations) |
| GET     | /makro-locations/recent | جلب المواقع الحديثة | [get_recent_makro_locations](#get_recent_makro_locations) |
| GET     | /makro-locations/nearby | البحث عن المكاري القريبة | [get_nearby_makros](#get_nearby_makros) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_makro_location"></a>1. تسجيل موقع مكرو جديد
- **المسار:** `/makro-locations/`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `MakroLocationCreate` (makro_id, lat, lng, timestamp)
- **المخرجات:**
  - كائن من نوع `MakroLocationRead`
- **المنطق:**
  - يسجل موقع جديد للمكرو مع الوقت الحالي إذا لم يتم تحديد timestamp.
  - يحفظ الإحداثيات كنقطة جغرافية.
- **أمثلة:**
```json
POST /makro-locations/
{
  "makro_id": "makro_123",
  "lat": 33.5,
  "lng": 36.3,
  "timestamp": "2024-01-01T12:00:00"
}
```
- **ملاحظات أمنية:** لا يتطلب مصادقة (يمكن للمكاري تسجيل مواقعهم مباشرة).

---

#### <a name="get_makro_locations"></a>2. جلب جميع مواقع المكاري
- **المسار:** `/makro-locations/`
- **الطريقة:** GET
- **المدخلات:** لا شيء
- **المخرجات:**
  - قائمة من كائنات `MakroLocationRead`
- **المنطق:**
  - يجلب جميع مواقع المكاري من قاعدة البيانات.
- **أمثلة:**
```http
GET /makro-locations/
```
- **ملاحظات:** لا يتطلب مصادقة.

---

#### <a name="get_recent_makro_locations"></a>3. جلب المواقع الحديثة
- **المسار:** `/makro-locations/recent`
- **الطريقة:** GET
- **المدخلات:**
  - Query: minutes (int, default=30) - عدد الدقائق للبحث في المواقع الحديثة
- **المخرجات:**
  - قائمة من كائنات `MakroLocationRead`
- **المنطق:**
  - يجلب مواقع المكاري التي تم تسجيلها خلال الدقائق المحددة.
  - يستخدم للحصول على المواقع النشطة حديثًا.
- **أمثلة:**
```http
GET /makro-locations/recent?minutes=15
```
- **ملاحظات:** مفيد لتتبع المكاري النشطة.

---

#### <a name="get_nearby_makros"></a>4. البحث عن المكاري القريبة
- **المسار:** `/makro-locations/nearby`
- **الطريقة:** GET
- **المدخلات:**
  - Query: lat (float), lng (float), radius (float, default=2.0), minutes (int, default=30)
- **المخرجات:**
  - قائمة من كائنات `MakroLocationRead`
- **المنطق:**
  - يبحث عن المكاري ضمن نصف القطر المحدد.
  - يقتصر على المواقع المسجلة خلال الدقائق المحددة.
  - يحسب المسافة باستخدام معادلة Haversine.
- **أمثلة:**
```http
GET /makro-locations/nearby?lat=33.5&lng=36.3&radius=1.5&minutes=20
```
- **ملاحظات:** مفيد للمستخدمين للعثور على مكاري قريبة ونشطة.

---

### استنتاجات تقنية وتحليل أمني
- نظام تتبع مواقع بسيط وفعال للمكاري.
- لا يتطلب مصادقة، مما يسهل على المكاري تسجيل مواقعهم.
- دعم البحث الجغرافي والزمني.
- يمكن استخدامه لتحليل أنماط حركة المكاري.

---

### توصيات
- إضافة مصادقة للمكاري لمنع التلاعب بالمواقع.
- إضافة تشفير لمعرفات المكاري.
- تحسين الأداء باستخدام فهارس جغرافية.
- إضافة نظام تنظيف تلقائي للمواقع القديمة.
- إضافة إحصائيات عن نشاط المكاري.

---

## نقاط نهاية إضافية وتحليل مفصل

### أولاً: نقاط نهاية مشاركة الموقع (location_share) الإضافية

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| GET     | /location-share/active | جلب جميع المشاركات النشطة للمستخدم الحالي | [get_active_location_shares](#get_active_location_shares) |
| GET     | /location-share/received | جلب المشاركات التي استلمها المستخدم الحالي | [get_received_location_shares](#get_received_location_shares) |
| GET     | /location-share/sent | جلب المشاركات التي أرسلها المستخدم الحالي | [get_sent_location_shares](#get_sent_location_shares) |
| GET     | /location-share/history | جلب سجل المشاركات السابقة | [get_location_share_history](#get_location_share_history) |
| GET     | /location-share/friends/locations | جلب مواقع الأصدقاء الذين يشاركون الموقع حاليًا مع المستخدم | [get_friend_locations](#get_friend_locations) |
| POST    | /location-share/cleanup | تنظيف المشاركات المنتهية | [cleanup_expired_shares](#cleanup_expired_shares) |

---

#### <a name="get_active_location_shares"></a>1. جلب جميع المشاركات النشطة للمستخدم الحالي
- **المسار:** `/location-share/active`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب جميع المشاركات النشطة التي أنشأها المستخدم الحالي ولم تنتهِ بعد.
  - يشمل تفاصيل المستخدمين المشارك معهم.
- **أمثلة:**
```http
GET /location-share/active
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_received_location_shares"></a>2. جلب المشاركات التي استلمها المستخدم الحالي
- **المسار:** `/location-share/received`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب جميع المشاركات النشطة التي تم مشاركتها مع المستخدم الحالي من أصدقائه.
- **أمثلة:**
```http
GET /location-share/received
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_sent_location_shares"></a>3. جلب المشاركات التي أرسلها المستخدم الحالي
- **المسار:** `/location-share/sent`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب جميع المشاركات التي أرسلها المستخدم الحالي لأصدقائه (سواء نشطة أو منتهية).
- **أمثلة:**
```http
GET /location-share/sent
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_location_share_history"></a>4. جلب سجل المشاركات السابقة
- **المسار:** `/location-share/history`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Query: limit (int, افتراضي 50)
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب سجل المشاركات السابقة (المنتهية أو الملغاة) للمستخدم الحالي.
  - يمكن تحديد الحد الأقصى للنتائج عبر limit.
- **أمثلة:**
```http
GET /location-share/history?limit=20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_friend_locations"></a>5. جلب مواقع الأصدقاء الذين يشاركون الموقع حاليًا مع المستخدم
- **المسار:** `/location-share/friends/locations`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `LocationShareWithUserResponse`
- **المنطق:**
  - يجلب مواقع الأصدقاء الذين لديهم مشاركة موقع نشطة مع المستخدم الحالي.
- **أمثلة:**
```http
GET /location-share/friends/locations
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="cleanup_expired_shares"></a>6. تنظيف المشاركات المنتهية
- **المسار:** `/location-share/cleanup`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - {"message": "Expired shares cleaned up"}
- **المنطق:**
  - يحذف أو يحدّث حالة جميع المشاركات المنتهية (expired) في النظام.
  - عادة تستخدم كخدمة إدارية أو مجدولة.
- **أمثلة:**
```http
POST /location-share/cleanup
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، ويفضل تقييدها للمشرفين فقط.

---

### استنتاجات تقنية وتحليل أمني (إضافي)
- النظام يدعم إدارة شاملة لمشاركات الموقع (نشطة، مستلمة، مرسلة، سجل).
- تنظيف المشاركات المنتهية يحافظ على الأداء.
- جميع العمليات محمية بالمصادقة.

### توصيات (إضافية)
- إضافة صلاحيات خاصة لتنظيف المشاركات (للمشرفين فقط).
- دعم التصفية حسب التاريخ أو الحالة في سجل المشاركات.

---

### نقاط نهاية البحث (search) الإضافية

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| GET     | /search/logs | جلب سجل عمليات البحث | [get_search_logs](#get_search_logs) |

---

#### <a name="get_search_logs"></a>1. جلب سجل عمليات البحث
- **المسار:** `/search/logs`
- **الطريقة:** GET
- **المدخلات:** لا شيء (أو يمكن إضافة فلاتر مستقبلًا)
- **المخرجات:**
  - قائمة من كائنات (dict) تمثل عمليات البحث السابقة (start_lat, start_lng, end_lat, end_lng, filter_type, execution_time_ms, results_count, ...).
- **المنطق:**
  - يجلب جميع عمليات البحث المسجلة في النظام (لأغراض التحليل أو الإدارة).
- **أمثلة:**
```http
GET /search/logs
```
- **ملاحظات أمنية:** يفضل تقييد الوصول للمشرفين أو لأغراض التحليل فقط.

---

### استنتاجات تقنية وتحليل أمني (إضافي)
- سجل عمليات البحث مفيد لتحليل الاستخدام وتحسين الخوارزميات.
- يفضل تقييد الوصول لهذه البيانات.

### توصيات (إضافية)
- دعم التصفية حسب المستخدم أو التاريخ.
- حماية endpoint للمشرفين فقط.

---

### نقاط نهاية مواقع المكاري (makro_locations) الإضافية

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| PUT     | /makro-locations/{makro_location_id} | تحديث موقع مكرو | [update_makro_location](#update_makro_location) |

---

#### <a name="update_makro_location"></a>1. تحديث موقع مكرو
- **المسار:** `/makro-locations/{makro_location_id}`
- **الطريقة:** PUT
- **المدخلات:**
  - Path: makro_location_id (int)
  - Body: كائن من نوع `MakroLocationCreate` (makro_id, lat, lng, timestamp)
- **المخرجات:**
  - كائن من نوع `MakroLocationRead` بعد التحديث
- **المنطق:**
  - يحدث بيانات موقع مكرو محدد (الإحداثيات، الوقت، ...).
- **أمثلة:**
```json
PUT /makro-locations/10
{
  "makro_id": "makro_123",
  "lat": 33.6,
  "lng": 36.4,
  "timestamp": "2024-06-01T13:00:00"
}
```
- **ملاحظات أمنية:** يفضل تقييد التحديث للمكاري أو المشرفين فقط.

---

### استنتاجات تقنية وتحليل أمني (إضافي)
- دعم تحديث بيانات المواقع يعزز دقة النظام.
- يفضل تقييد التحديث للمستخدمين المصرح لهم فقط.

### توصيات (إضافية)
- إضافة تحقق من هوية المكرو قبل السماح بالتحديث.
- تسجيل جميع عمليات التحديث لأغراض التدقيق.

