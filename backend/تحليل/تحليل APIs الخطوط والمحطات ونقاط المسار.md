# تحليل APIs الخطوط والمحطات ونقاط المسار

## تحليل ملف `src/routers/routes.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة خطوط النقل (routes) في النظام. يوفر عمليات CRUD كاملة (إنشاء، قراءة، تحديث، حذف)، بالإضافة إلى إدارة المحطات (stops) والمسارات (paths) وتحسين الخطوط (optimization). يعتمد على FastAPI وSQLAlchemy وGeoAlchemy2 وRedis للتخزين المؤقت.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /routes/ | إنشاء خط جديد | [create_route](#create_route) |
| GET     | /routes/{route_id}/stops | جلب محطات خط | [get_route_stops](#get_route_stops) |
| GET     | /routes/{route_id}/paths | جلب مسارات خط | [get_route_paths](#get_route_paths) |
| POST    | /routes/{route_id}/optimize | تحسين مسار خط | [optimize_route](#optimize_route) |
| GET     | /routes/ | جلب جميع الخطوط | [read_routes](#read_routes) |
| GET     | /routes/{route_id} | جلب خط محدد | [read_route](#read_route) |
| PUT     | /routes/{route_id} | تحديث خط | [update_route](#update_route) |
| DELETE  | /routes/{route_id} | حذف خط | [delete_route](#delete_route) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_route"></a>1. إنشاء خط جديد
- **المسار:** `/routes/`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `RouteCreate` (اسم الخط، الوصف، السعر، ساعات العمل، قائمة المحطات، قائمة المسارات)
- **المخرجات:**
  - كائن من نوع `RouteRead` (تفاصيل الخط مع المحطات والمسارات)
- **المنطق:**
  - يتحقق من عدم تكرار اسم الخط.
  - ينشئ كائن الخط.
  - ينشئ المحطات ويربطها بالخط.
  - ينشئ المسارات ويربطها بالخط.
  - يخزن النتيجة في الكاش (Redis).
- **أمثلة:**
```json
POST /routes/
{
  "name": "Route 1",
  "description": "Main route",
  "price": 1000,
  "operating_hours": "6:00-22:00",
  "stops": [
    {"name": "Stop 1", "lat": 33.5, "lng": 36.3},
    {"name": "Stop 2", "lat": 33.6, "lng": 36.4}
  ],
  "paths": [
    {"lat": 33.5, "lng": 36.3, "point_order": 1},
    {"lat": 33.6, "lng": 36.4, "point_order": 2}
  ]
}
```
- **ملاحظات أمنية:** يتطلب مصادقة (current_user).
- **ملاحظات تقنية:** يدعم الجيومكانيك (GeoAlchemy2)، ويستخدم الكاش بقوة.

---

#### <a name="get_route_stops"></a>2. جلب محطات خط محدد
- **المسار:** `/routes/{route_id}/stops`
- **الطريقة:** GET
- **المدخلات:**
  - Path: route_id (int)
- **المخرجات:**
  - قائمة من كائنات `StopRead`
- **المنطق:**
  - يتحقق من وجود الخط.
  - يجلب جميع المحطات المرتبطة بالخط.
- **أمثلة:**
```http
GET /routes/1/stops
```
- **ملاحظات:** لا يتطلب مصادقة.

---

#### <a name="get_route_paths"></a>3. جلب مسارات خط محدد
- **المسار:** `/routes/{route_id}/paths`
- **الطريقة:** GET
- **المدخلات:**
  - Path: route_id (int)
- **المخرجات:**
  - قائمة من كائنات `RoutePathRead`
- **المنطق:**
  - يتحقق من وجود الخط.
  - يجلب جميع المسارات المرتبطة بالخط مرتبة.
- **أمثلة:**
```http
GET /routes/1/paths
```

---

#### <a name="optimize_route"></a>4. تحسين مسار خط محدد
- **المسار:** `/routes/{route_id}/optimize`
- **الطريقة:** POST
- **المدخلات:**
  - Path: route_id (int)
- **المخرجات:**
  - رسالة نجاح وعدد المحطات
- **المنطق:**
  - يتحقق من وجود الخط.
  - يعيد ترتيب المحطات حسب الإحداثيات (بسيط).
  - يحدث ترتيب المحطات في قاعدة البيانات.
- **أمثلة:**
```http
POST /routes/1/optimize
```
- **ملاحظات:** يتطلب مصادقة. الخوارزمية بسيطة ويمكن تحسينها.

---

#### <a name="read_routes"></a>5. جلب جميع الخطوط
- **المسار:** `/routes/`
- **الطريقة:** GET
- **المدخلات:** لا شيء
- **المخرجات:**
  - قائمة من كائنات `RouteRead`
- **المنطق:**
  - يحاول جلب البيانات من الكاش أولًا.
  - إذا لم توجد، يجلبها من قاعدة البيانات مع المحطات والمسارات.
  - يخزنها في الكاش.
- **أمثلة:**
```http
GET /routes/
```

---

#### <a name="read_route"></a>6. جلب خط محدد
- **المسار:** `/routes/{route_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Path: route_id (int)
- **المخرجات:**
  - كائن `RouteRead`
- **المنطق:**
  - يحاول جلب البيانات من الكاش أولًا.
  - إذا لم توجد، يجلبها من قاعدة البيانات مع المحطات والمسارات.
  - يخزنها في الكاش.
- **أمثلة:**
```http
GET /routes/1
```

---

#### <a name="update_route"></a>7. تحديث خط
- **المسار:** `/routes/{route_id}`
- **الطريقة:** PUT
- **المدخلات:**
  - Path: route_id (int)
  - Body: كائن `RouteUpdate`
- **المخرجات:**
  - كائن `RouteRead` بعد التحديث
- **المنطق:**
  - يتحقق من وجود الخط.
  - يحدث الحقول المطلوبة فقط.
  - يحدث الكاش.
- **أمثلة:**
```json
PUT /routes/1
{
  "name": "Route 1 updated",
  "price": 1200
}
```
- **ملاحظات:** يتطلب مصادقة.

---

#### <a name="delete_route"></a>8. حذف خط
- **المسار:** `/routes/{route_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Path: route_id (int)
- **المخرجات:**
  - {"ok": true}
- **المنطق:**
  - يتحقق من وجود الخط.
  - يحذف جميع العلاقات (RouteStop, RoutePath) ثم الخط نفسه.
  - يحدث الكاش.
- **أمثلة:**
```http
DELETE /routes/1
```
- **ملاحظات:** يتطلب مصادقة. الحذف نهائي.

---

### استنتاجات تقنية وتحليل أمني
- الاعتماد على الكاش (Redis) قوي جدًا لتحسين الأداء، لكن يجب الانتباه لتزامن البيانات.
- حماية نقاط الإنشاء والتحديث والحذف عبر المصادقة (Depends(get_current_user)).
- دعم قوي للبيانات الجغرافية (GeoAlchemy2).
- الخوارزميات المستخدمة في التحسين بسيطة ويمكن تطويرها لاحقًا.
- كل نقطة نهاية موثقة جيدًا ويمكن اختبارها بسهولة عبر أدوات مثل Swagger UI أو Postman.

---

### توصيات
- تطوير خوارزمية تحسين المسار لتكون أكثر ذكاءً (مثلاً: TSP).
- إضافة صلاحيات أدق (مثلاً: فقط الأدمن يمكنه الحذف).
- مراقبة الكاش وتحديثه عند أي تغيير في البيانات.
- توثيق جميع الحقول في RouteCreate وRouteRead وStopRead وRoutePathRead في قسم النماذج.

---

## تحليل ملف `src/routers/stops.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة المحطات (stops) في النظام. يوفر عمليات CRUD كاملة (إضافة، قراءة، تحديث، حذف)، بالإضافة إلى البحث عن المحطات القريبة bulk/nearby. يعتمد على FastAPI وSQLAlchemy وRedis للتخزين المؤقت.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /stops/ | إنشاء محطة جديدة | [create_stop](#create_stop) |
| POST    | /stops/bulk | إنشاء عدة محطات دفعة واحدة | [create_stops_bulk](#create_stops_bulk) |
| GET     | /stops/nearby | البحث عن المحطات القريبة | [get_nearby_stops](#get_nearby_stops) |
| GET     | /stops/ | جلب جميع المحطات | [read_stops](#read_stops) |
| GET     | /stops/{stop_id} | جلب محطة محددة | [read_stop](#read_stop) |
| PUT     | /stops/{stop_id} | تحديث محطة | [update_stop](#update_stop) |
| DELETE  | /stops/{stop_id} | حذف محطة | [delete_stop](#delete_stop) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_stop"></a>1. إنشاء محطة جديدة
- **المسار:** `/stops/`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `StopCreate` (name, lat, lng)
- **المخرجات:**
  - كائن من نوع `StopRead`
- **المنطق:**
  - يتحقق من عدم تكرار اسم المحطة.
  - ينشئ كائن المحطة.
  - يخزنها في قاعدة البيانات.
  - يحدث الكاش.
- **أمثلة:**
```json
POST /stops/
{
  "name": "Stop 1",
  "lat": 33.5,
  "lng": 36.3
}
```
- **ملاحظات أمنية:** يتطلب مصادقة (current_user).

---

#### <a name="create_stops_bulk"></a>2. إنشاء عدة محطات دفعة واحدة
- **المسار:** `/stops/bulk`
- **الطريقة:** POST
- **المدخلات:**
  - Body: قائمة من كائنات `StopCreate`
- **المخرجات:**
  - قائمة من كائنات `StopRead`
- **المنطق:**
  - ينشئ عدة محطات دفعة واحدة، ويتجاهل المكررة.
  - يحدث الكاش.
- **أمثلة:**
```json
POST /stops/bulk
[
  {"name": "Stop 1", "lat": 33.5, "lng": 36.3},
  {"name": "Stop 2", "lat": 33.6, "lng": 36.4}
]
```
- **ملاحظات أمنية:** يتطلب مصادقة (current_user).

---

#### <a name="get_nearby_stops"></a>3. البحث عن المحطات القريبة
- **المسار:** `/stops/nearby`
- **الطريقة:** GET
- **المدخلات:**
  - Query: lat (float), lng (float), radius (float, default=1.0)
- **المخرجات:**
  - قائمة من كائنات `StopRead`
- **المنطق:**
  - يحسب المسافة بين كل محطة والنقطة المطلوبة باستخدام معادلة Haversine.
  - يعيد المحطات ضمن نصف القطر المحدد.
- **أمثلة:**
```http
GET /stops/nearby?lat=33.5&lng=36.3&radius=2
```
- **ملاحظات تقنية:** الحساب يتم في التطبيق وليس في قاعدة البيانات (يمكن تحسينه باستخدام PostGIS).

---

#### <a name="read_stops"></a>4. جلب جميع المحطات
- **المسار:** `/stops/`
- **الطريقة:** GET
- **المدخلات:** لا شيء
- **المخرجات:**
  - قائمة من كائنات `StopRead`
- **المنطق:**
  - يحاول جلب البيانات من الكاش أولًا.
  - إذا لم توجد، يجلبها من قاعدة البيانات.
  - يخزنها في الكاش.
- **أمثلة:**
```http
GET /stops/
```

---

#### <a name="read_stop"></a>5. جلب محطة محددة
- **المسار:** `/stops/{stop_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Path: stop_id (int)
- **المخرجات:**
  - كائن `StopRead`
- **المنطق:**
  - يحاول جلب البيانات من الكاش أولًا.
  - إذا لم توجد، يجلبها من قاعدة البيانات.
  - يخزنها في الكاش.
- **أمثلة:**
```http
GET /stops/1
```

---

#### <a name="update_stop"></a>6. تحديث محطة
- **المسار:** `/stops/{stop_id}`
- **الطريقة:** PUT
- **المدخلات:**
  - Path: stop_id (int)
  - Body: كائن `StopUpdate`
- **المخرجات:**
  - كائن `StopRead` بعد التحديث
- **المنطق:**
  - يتحقق من وجود المحطة.
  - يحدث الحقول المطلوبة فقط.
  - يحدث الكاش.
- **أمثلة:**
```json
PUT /stops/1
{
  "name": "Stop 1 updated"
}
```
- **ملاحظات:** يتطلب مصادقة.

---

#### <a name="delete_stop"></a>7. حذف محطة
- **المسار:** `/stops/{stop_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Path: stop_id (int)
- **المخرجات:**
  - {"ok": true}
- **المنطق:**
  - يتحقق من وجود المحطة.
  - يحذفها من قاعدة البيانات.
  - يحدث الكاش.
- **أمثلة:**
```http
DELETE /stops/1
```
- **ملاحظات:** يتطلب مصادقة. الحذف نهائي.

---

### استنتاجات تقنية وتحليل أمني
- الاعتماد على الكاش (Redis) لتحسين الأداء في عمليات القراءة.
- حماية نقاط الإنشاء والتحديث والحذف عبر المصادقة (Depends(get_current_user)).
- البحث عن المحطات القريبة يتم في التطبيق وليس في قاعدة البيانات (قد يؤثر على الأداء مع كثرة البيانات).
- لا يوجد تحقق من العلاقات (مثلاً: هل المحطة مرتبطة بخط قبل حذفها؟) — يفضل إضافة تحقق أو حماية من الحذف العرضي.

---

### توصيات
- تحسين البحث عن المحطات القريبة باستخدام PostGIS وST_DWithin.
- إضافة تحقق من العلاقات قبل الحذف (مثلاً: لا تحذف محطة مرتبطة بخط).
- مراقبة الكاش وتحديثه عند أي تغيير في البيانات.
- توثيق جميع الحقول في StopCreate وStopRead في قسم النماذج.

---

## تحليل ملف `src/routers/route_paths.py`

### نظرة عامة

هذا الملف مسؤول عن إدارة نقاط المسار (Route Paths) لكل خط نقل. يوفر عمليات CRUD كاملة (إضافة، قراءة، تحديث، حذف) لنقاط المسار المرتبطة بالخطوط. يعتمد على FastAPI وSQLAlchemy.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /route-paths/ | إنشاء نقطة مسار جديدة | [create_route_path](#create_route_path) |
| GET     | /route-paths/ | جلب جميع نقاط المسار | [read_route_paths](#read_route_paths) |
| GET     | /route-paths/{route_path_id} | جلب نقطة مسار محددة | [read_route_path](#read_route_path) |
| PUT     | /route-paths/{route_path_id} | تحديث نقطة مسار | [update_route_path](#update_route_path) |
| DELETE  | /route-paths/{route_path_id} | حذف نقطة مسار | [delete_route_path](#delete_route_path) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_route_path"></a>1. إنشاء نقطة مسار جديدة
- **المسار:** `/route-paths/`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `RoutePathCreate` (route_id, lat, lng, point_order)
- **المخرجات:**
  - كائن من نوع `RoutePathRead`
- **المنطق:**
  - ينشئ نقطة مسار جديدة ويربطها بخط معين.
  - يخزن الإحداثيات كنقطة جغرافية (geom).
- **أمثلة:**
```json
POST /route-paths/
{
  "route_id": 1,
  "lat": 33.5,
  "lng": 36.3,
  "point_order": 1
}
```
- **ملاحظات أمنية:** يتطلب مصادقة (current_user).

---

#### <a name="read_route_paths"></a>2. جلب جميع نقاط المسار
- **المسار:** `/route-paths/`
- **الطريقة:** GET
- **المدخلات:** لا شيء
- **المخرجات:**
  - قائمة من كائنات `RoutePathRead`
- **المنطق:**
  - يجلب جميع نقاط المسار من قاعدة البيانات.
- **أمثلة:**
```http
GET /route-paths/
```

---

#### <a name="read_route_path"></a>3. جلب نقطة مسار محددة
- **المسار:** `/route-paths/{route_path_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Path: route_path_id (int)
- **المخرجات:**
  - كائن `RoutePathRead`
- **المنطق:**
  - يجلب نقطة المسار حسب المعرف.
  - يعيد خطأ 404 إذا لم توجد.
- **أمثلة:**
```http
GET /route-paths/1
```

---

#### <a name="update_route_path"></a>4. تحديث نقطة مسار
- **المسار:** `/route-paths/{route_path_id}`
- **الطريقة:** PUT
- **المدخلات:**
  - Path: route_path_id (int)
  - Body: كائن `RoutePathUpdate`
- **المخرجات:**
  - كائن `RoutePathRead` بعد التحديث
- **المنطق:**
  - يتحقق من وجود نقطة المسار.
  - يحدث الحقول المطلوبة فقط.
- **أمثلة:**
```json
PUT /route-paths/1
{
  "lat": 33.6,
  "lng": 36.4
}
```
- **ملاحظات:** يتطلب مصادقة.

---

#### <a name="delete_route_path"></a>5. حذف نقطة مسار
- **المسار:** `/route-paths/{route_path_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Path: route_path_id (int)
- **المخرجات:**
  - {"ok": true}
- **المنطق:**
  - يتحقق من وجود نقطة المسار.
  - يحذفها من قاعدة البيانات.
- **أمثلة:**
```http
DELETE /route-paths/1
```
- **ملاحظات:** يتطلب مصادقة. الحذف نهائي.

---

### استنتاجات تقنية وتحليل أمني
- جميع العمليات التي تتطلب تعديل (إنشاء، تحديث، حذف) تتطلب مصادقة المستخدم (current_user).
- لا يوجد كاش هنا، كل العمليات مباشرة على قاعدة البيانات.
- لا يوجد تحقق من علاقات النقطة (مثلاً: هل النقطة مرتبطة بمسار مستخدم؟) — يفضل إضافة تحقق أو حماية من الحذف العرضي.
- دعم جيد للبيانات الجغرافية (geom).

---

### توصيات
- إضافة تحقق من العلاقات قبل الحذف (مثلاً: لا تحذف نقطة مرتبطة بمسار مستخدم).
- توثيق جميع الحقول في RoutePathCreate وRoutePathRead في قسم النماذج.
- إضافة دعم للكاش إذا زاد حجم البيانات.

