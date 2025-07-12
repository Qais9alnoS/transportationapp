# تحليل شامل لملف `src/routers/auth.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/auth` بسبب:
  ```python
  router = APIRouter(prefix="/auth", tags=["Authentication"])
  ```

## 2. المسارات المعرفة
- **POST `/auth/register`**: تسجيل مستخدم جديد (يُرجع توكن)
- **POST `/auth/login`**: تسجيل دخول (يُرجع توكن)
- **POST `/auth/google`**: تسجيل دخول عبر Google OAuth
- **POST `/auth/refresh`**: تجديد التوكن
- **GET `/auth/me`**: جلب معلومات المستخدم الحالي
- **POST `/auth/forgot-password`**: طلب إعادة تعيين كلمة المرور
- **POST `/auth/reset-password`**: إعادة تعيين كلمة المرور
- **POST `/auth/change-password`**: تغيير كلمة المرور
- **GET `/auth/google/url`**: جلب رابط Google OAuth

## 3. الصلاحيات
- بعض المسارات تتطلب مصادقة (مثل `/me`, `/change-password`)
- يتم التحقق من صلاحيات المدير عبر دالة `get_current_admin`

## 4. التوافق مع الاختبارات
- في ملف `main.py`، الراوتر يُضاف مع بادئة `/api/v1`:
  ```python
  app.include_router(auth.router, prefix="/api/v1")
  ```
- إذًا المسارات النهائية هي مثل:
  - `/api/v1/auth/register`
  - `/api/v1/auth/login`
  - ...إلخ
- يجب أن تكون جميع طلبات الاختبار للمصادقة تبدأ بـ `/api/v1/auth/`

## 5. الحقول المطلوبة
- جميع الحقول المطلوبة في التسجيل وتسجيل الدخول معرفة في `UserCreate` و`UserLogin` في `src/schemas/auth.py`

## 6. الاعتمادية
- يعتمد على `AuthService` في `src/services/auth_service.py` لتنفيذ منطق المصادقة.

---

# تحليل شامل لملف `src/routers/routes.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/routes` بسبب:
  ```python
  router = APIRouter(prefix="/routes", tags=["Routes"])
  ```

## 2. المسارات المعرفة
- **POST `/routes/`**: إنشاء خط جديد (يتطلب مصادقة)
- **GET `/routes/`**: جلب جميع الخطوط
- **GET `/routes/{route_id}`**: جلب خط محدد
- **PUT `/routes/{route_id}`**: تحديث خط (يتطلب مصادقة)
- **DELETE `/routes/{route_id}`**: حذف خط (يتطلب مصادقة)

## 3. الصلاحيات
- إنشاء، تحديث، حذف الخطوط تتطلب مصادقة (`current_user=Depends(get_current_user)`).
- جلب الخطوط لا يتطلب مصادقة.

## 4. التوافق مع الاختبارات
- في ملف `main.py`، الراوتر يُضاف بدون بادئة إضافية:
  ```python
  app.include_router(routes.router)
  ```
- إذًا المسارات النهائية هي كما هي في الراوتر (`/routes/...`).
- يجب أن تكون جميع طلبات الاختبار لمسارات الخطوط تبدأ بـ `/routes/`.

## 5. الحقول المطلوبة
- يعتمد على نماذج `RouteCreate`, `RouteRead`, `RouteUpdate` من `src/schemas/route.py`.
- الحقل `operating_hours` يجب أن يكون بصيغة `HH:MM-HH:MM` (مثال: `06:00-23:00`).
- أي قيمة مثل `6:00-23:00` ستسبب خطأ تحقق (ValidationError).

## 6. الاعتمادية
- يعتمد على:
  - `models.Route`, `models.Stop`, `models.RouteStop`, `models.RoutePath` من `src/models/models.py`
  - خدمات الكاش: `cache_get`, `cache_set`, `redis_client` من `src/services/cache_service.py`
  - دوال التحقق من المستخدم من `src/routers/auth.py`

## 7. ملاحظات ومشاكل محتملة
- يجب التأكد من أن جميع الحقول في قاعدة البيانات متوافقة مع النماذج.
- يجب التأكد من أن جميع القيم المدخلة في الاختبارات (خاصة `operating_hours`) بصيغة صحيحة.
- إذا ظهرت أخطاء 403 في الاختبارات، تحقق من أن التوكنات صالحة.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/dashboard.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/dashboard` بسبب:
  ```python
  router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **GET `/dashboard/real-time-stats`**: إحصائيات فورية متقدمة للتطبيق
- **GET `/dashboard/route-analytics`**: تحليلات متقدمة للخطوط (مع دعم الفلترة بفترة زمنية أو خط محدد)
- **GET `/dashboard/user-behavior`**: تحليل سلوك المستخدمين
- **GET `/dashboard/predictive-insights`**: رؤى تنبؤية (توقعات)
- **GET `/dashboard/complaint-intelligence`**: تحليلات الشكاوى
- **GET `/dashboard/geographic-intelligence`**: تحليلات جغرافية
- **GET `/dashboard/system-health`**: صحة النظام
- **GET `/dashboard/top-routes`**: أفضل الخطوط أداءً
- **GET `/dashboard/usage-statistics`**: إحصائيات الاستخدام
- **GET `/dashboard/complaints`**: جلب الشكاوى مع دعم الفلترة
- **PUT `/dashboard/complaints/{complaint_id}`**: تحديث حالة الشكوى
- **GET `/dashboard/heatmap-data`**: بيانات خريطة الحرارة
- **GET `/dashboard/recommendations`**: توصيات ذكية

## 3. الصلاحيات
- جميع المسارات تتطلب مصادقة مدير (admin) عبر:
  ```python
  current_admin: UserResponse = Depends(get_current_admin)
  ```

## 4. الاعتمادية
- يعتمد على:
  - نماذج: `Route`, `User`, `Complaint`, `SearchLog`, `LocationShare`, `Friendship`, `MakroLocation` من `src/models/models.py`
  - خدمات الكاش: `cache_get`, `cache_set`, `redis_client` من `src/services/cache_service.py`
  - دوال التحقق من المدير من `src/routers/auth.py`
  - دوال مساعدة وتحليل داخلية (generate_route_recommendations, ...)

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات الداشبورد بـ `/dashboard/`.
- جميع المسارات تتطلب توكن مدير صالح.
- تحقق من أن بيانات الاختبار تغطي جميع السيناريوهات (إحصائيات، تحليلات، شكاوى، توصيات).

## 6. ملاحظات ومشاكل محتملة
- جميع المسارات محمية بصلاحيات المدير فقط (403 إذا لم يكن التوكن صالحًا).
- بعض المسارات تعتمد على بيانات متراكمة (logs, complaints, ...)، يجب تهيئة بيانات كافية للاختبار.
- تحقق من صحة تواريخ الإدخال (start_time, end_time) في المسارات التحليلية.
- بعض الدوال التحليلية تعتمد على وجود بيانات في الجداول المرتبطة (routes, users, complaints, ...).
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/friendship.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/friends` بسبب:
  ```python
  router = APIRouter(prefix="/friends", tags=["Friendship"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/friends/request`**: إرسال طلب صداقة
- **PUT `/friends/request/{friendship_id}/respond`**: قبول أو رفض طلب صداقة
- **GET `/friends/`**: جلب جميع الأصدقاء للمستخدم الحالي
- **GET `/friends/requests/received`**: جلب طلبات الصداقة المستلمة
- **GET `/friends/requests/sent`**: جلب طلبات الصداقة المرسلة
- **DELETE `/friends/{friend_id}`**: حذف صديق
- **DELETE `/friends/request/{friendship_id}/cancel`**: إلغاء طلب صداقة مرسل
- **GET `/friends/search`**: البحث عن مستخدمين لإضافتهم كأصدقاء
- **GET `/friends/status/{user_id}`**: جلب حالة الصداقة مع مستخدم آخر

## 3. الصلاحيات
- جميع المسارات تتطلب مصادقة مستخدم (current_user=Depends(get_current_user)).

## 4. الاعتمادية
- يعتمد على:
  - خدمة الصداقة: `FriendshipService` من `src/services/friendship_service.py`
  - خدمة المصادقة: `AuthService` من `src/services/auth_service.py`
  - مخططات: `FriendshipCreate`, `FriendshipResponse`, `FriendshipUpdate`, `UserFriendResponse`, `FriendshipWithUserResponse`, `FriendRequestResponse` من `src/schemas/friendship.py`
  - دوال التحقق من المستخدم من `src/routers/auth.py`

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات الصداقة بـ `/friends/`.
- جميع المسارات تتطلب توكن مستخدم صالح.
- تحقق من أن بيانات الاختبار تغطي جميع السيناريوهات (إرسال، قبول، رفض، حذف، بحث، حالة).

## 6. ملاحظات ومشاكل محتملة
- جميع المسارات محمية بصلاحيات المستخدم فقط (403 إذا لم يكن التوكن صالحًا).
- بعض المسارات تعتمد على وجود مستخدمين آخرين في قاعدة البيانات.
- تحقق من صحة معرفات المستخدمين في الاختبارات.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/location_share.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/location-share` بسبب:
  ```python
  router = APIRouter(prefix="/location-share", tags=["Location Sharing"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/location-share/share`**: مشاركة الموقع الحالي مع الأصدقاء
- **PUT `/location-share/{share_id}/update`**: تحديث مشاركة موقع نشطة
- **DELETE `/location-share/{share_id}/cancel`**: إلغاء مشاركة موقع نشطة
- **GET `/location-share/active`**: جلب جميع المشاركات النشطة للمستخدم الحالي
- **GET `/location-share/received`**: جلب المشاركات المستلمة من الآخرين
- **GET `/location-share/sent`**: جلب المشاركات المرسلة للآخرين
- **GET `/location-share/history`**: جلب سجل المشاركات السابقة
- **GET `/location-share/friends/locations`**: جلب مواقع الأصدقاء الذين يشاركون الموقع مع المستخدم
- **POST `/location-share/cleanup`**: تنظيف المشاركات المنتهية (وظيفة إدارية)

## 3. الصلاحيات
- جميع المسارات تتطلب مصادقة مستخدم (current_user=Depends(get_current_user)).
- وظيفة التنظيف (cleanup) قد تتطلب صلاحيات إضافية (تحقق من منطق الخدمة).

## 4. الاعتمادية
- يعتمد على:
  - خدمة مشاركة الموقع: `LocationShareService` من `src/services/location_share_service.py`
  - مخططات: `LocationShareCreate`, `LocationShareResponse`, `LocationShareUpdate`, `LocationShareWithUserResponse`, `LocationShareCancel` من `src/schemas/location_share.py`
  - دوال التحقق من المستخدم من `src/routers/auth.py`

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات مشاركة الموقع بـ `/location-share/`.
- جميع المسارات تتطلب توكن مستخدم صالح.
- تحقق من أن بيانات الاختبار تغطي جميع السيناريوهات (مشاركة، تحديث، إلغاء، جلب مشاركات، سجل، تنظيف).

## 6. ملاحظات ومشاكل محتملة
- جميع المسارات محمية بصلاحيات المستخدم فقط (403 إذا لم يكن التوكن صالحًا).
- بعض المسارات تعتمد على وجود أصدقاء أو مشاركات سابقة في قاعدة البيانات.
- تحقق من صحة معرفات المشاركات والمستخدمين في الاختبارات.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/makro_locations.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/makro-locations` بسبب:
  ```python
  router = APIRouter(prefix="/makro-locations", tags=["MakroLocations"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/makro-locations/`**: استقبال بيانات موقع مكرو (GPS) وحفظها في قاعدة البيانات
- **GET `/makro-locations/`**: جلب جميع مواقع المكاري المخزنة

## 3. الصلاحيات
- لا يوجد تحقق من المستخدم أو صلاحيات (المسارات مفتوحة لأي جهاز أو برنامج)
- مناسب لتتبع الأجهزة الخارجية (مثل GPS)

## 4. الاعتمادية
- يعتمد على:
  - نموذج MakroLocation من `src/models/models.py`
  - مخططات: `MakroLocationCreate`, `MakroLocationRead` من `src/schemas/makro_location.py`
  - قاعدة البيانات عبر `SessionLocal` من `config/database.py`
  - مكتبات GIS: `geoalchemy2`, `shapely`

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات تتبع المكاري بـ `/makro-locations/`.
- تحقق من أن بيانات الاختبار تغطي سيناريوهات الإدخال (إرسال موقع جديد، جلب المواقع).

## 6. ملاحظات ومشاكل محتملة
- لا يوجد تحقق من هوية المرسل (أي جهاز يمكنه الإرسال)، يجب الانتباه أمنيًا إذا كان ذلك غير مقصود.
- تحقق من صحة البيانات المدخلة (lat/lng/format).
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/route_paths.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/route-paths` بسبب:
  ```python
  router = APIRouter(prefix="/route-paths", tags=["RoutePaths"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/route-paths/`**: إنشاء نقطة مسار جديدة (يتطلب مصادقة)
- **GET `/route-paths/`**: جلب جميع نقاط المسارات
- **GET `/route-paths/{route_path_id}`**: جلب نقطة مسار محددة
- **PUT `/route-paths/{route_path_id}`**: تحديث نقطة مسار (يتطلب مصادقة)
- **DELETE `/route-paths/{route_path_id}`**: حذف نقطة مسار (يتطلب مصادقة)

## 3. الصلاحيات
- إنشاء، تحديث، حذف نقاط المسار تتطلب مصادقة (`current_user=Depends(get_current_user)`).
- جلب نقاط المسار لا يتطلب مصادقة.

## 4. الاعتمادية
- يعتمد على:
  - نموذج RoutePath من `src/models/models.py`
  - مخططات: `RoutePathCreate`, `RoutePathRead`, `RoutePathUpdate` من `src/schemas/route_path.py`
  - قاعدة البيانات عبر `SessionLocal` من `config/database.py`
  - دوال التحقق من المستخدم من `src/routers/auth.py`

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات نقاط المسار بـ `/route-paths/`.
- تحقق من أن بيانات الاختبار تغطي جميع السيناريوهات (إضافة، جلب، تحديث، حذف).

## 6. ملاحظات ومشاكل محتملة
- تحقق من صحة معرفات نقاط المسار في الاختبارات.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/stops.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/stops` بسبب:
  ```python
  router = APIRouter(prefix="/stops", tags=["Stops"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/stops/`**: إنشاء محطة جديدة (يتطلب مصادقة)
- **GET `/stops/`**: جلب جميع المحطات (مع دعم الكاش)
- **GET `/stops/{stop_id}`**: جلب محطة محددة (مع دعم الكاش)
- **PUT `/stops/{stop_id}`**: تحديث محطة (يتطلب مصادقة)
- **DELETE `/stops/{stop_id}`**: حذف محطة (يتطلب مصادقة)

## 3. الصلاحيات
- إنشاء، تحديث، حذف المحطات تتطلب مصادقة (`current_user=Depends(get_current_user)`).
- جلب المحطات لا يتطلب مصادقة.

## 4. الاعتمادية
- يعتمد على:
  - نموذج Stop من `src/models/models.py`
  - مخططات: `StopCreate`, `StopRead`, `StopUpdate` من `src/schemas/stop.py`
  - قاعدة البيانات عبر `SessionLocal` من `config/database.py`
  - دوال التحقق من المستخدم من `src/routers/auth.py`
  - خدمات الكاش: `cache_get`, `cache_set`, `redis_client` من `src/services/cache_service.py`

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات المحطات بـ `/stops/`.
- تحقق من أن بيانات الاختبار تغطي جميع السيناريوهات (إضافة، جلب، تحديث، حذف).

## 6. ملاحظات ومشاكل محتملة
- تحقق من صحة معرفات المحطات في الاختبارات.
- تحقق من عدم تكرار اسم المحطة عند الإنشاء.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

---

# تحليل شامل لملف `src/routers/traffic.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/traffic-data` بسبب:
  ```python
  router = APIRouter(prefix="/traffic-data", tags=["Traffic"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/traffic-data/`**: جلب بيانات الازدحام لمسار معين (محاكاة)
- **POST `/traffic-data/google`**: جلب بيانات المسار والزمن الفعلي من Google Directions API

## 3. الصلاحيات
- لا يوجد تحقق من المستخدم أو صلاحيات (المسارات مفتوحة للجميع)

## 4. الاعتمادية
- يعتمد على:
  - خدمات: `get_mock_traffic_data`, `get_directions_with_traffic` من `src/services/traffic_data.py`
  - مخططات داخلية (PathPoint, TrafficRequest, DirectionsRequest)
  - مفتاح Google API يجب أن يكون مضبوطًا في `src/services/traffic_data.py` للمسار الثاني

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسارات بيانات الازدحام بـ `/traffic-data/`.
- تحقق من أن بيانات الاختبار تغطي سيناريوهات المسار الوهمي والحقيقي (Google).

## 6. ملاحظات ومشاكل محتملة
- لا يوجد تحقق من هوية المرسل (أي مستخدم يمكنه الإرسال)، يجب الانتباه أمنيًا عند استخدام Google API.
- تحقق من صحة بيانات النقاط (lat/lng) وصيغة الوقت في الطلبات.
- يجب ضبط مفتاح Google API بشكل صحيح في الخدمة.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق الخدمة أو إعدادات Google API.

---

# تحليل شامل لملف `src/routers/search.py`

## 1. البادئة (prefix) للمسارات
- جميع المسارات تبدأ فعليًا بـ `/search-route` بسبب:
  ```python
  router = APIRouter(prefix="/search-route", tags=["SearchRoute"])
  ```

## 2. المسارات المعرفة (Endpoints)
- **POST `/search-route/`**: البحث عن خط (Route) بناءً على الطلب

## 3. الصلاحيات
- لا يوجد تحقق من المستخدم أو صلاحيات (المسار مفتوح للجميع)

## 4. الاعتمادية
- يعتمد على:
  - خدمة البحث عن الخطوط: `search_routes` من `src/services/route_search.py`
  - مخططات: `SearchRouteRequest`, `SearchRouteResponse` من `src/schemas/search.py`

## 5. التوافق مع الاختبارات
- يجب أن تبدأ جميع طلبات الاختبار لمسار البحث بـ `/search-route/`.
- تحقق من أن بيانات الاختبار تغطي سيناريوهات البحث المختلفة.

## 6. ملاحظات ومشاكل محتملة
- لا يوجد تحقق من هوية المرسل (أي مستخدم يمكنه الإرسال)، يجب الانتباه أمنيًا إذا كان ذلك غير مقصود.
- تحقق من صحة بيانات البحث وصيغة الطلب.
- إذا ظهرت أخطاء 500، تحقق من صحة البيانات المدخلة أو منطق خدمة البحث.

---

# تحليل شامل لملفات الخدمات القصيرة والمتوسطة

## 1. src/services/cache_service.py
- **الوظيفة:** إدارة الكاش باستخدام Redis (get/set/delete).
- **الاعتمادية:** يعتمد على مكتبة redis وبيئة REDIS_URL.
- **التوافق:** مستخدم في عدة راوترات (stops, routes, ...).
- **ملاحظات:** يجب التأكد من تشغيل Redis وضبط المتغيرات البيئية.

## 2. src/services/traffic.py
- **الوظيفة:** جلب بيانات الازدحام بين نقطتين باستخدام Google Directions API أو محاكاة إذا لم يوجد مفتاح API.
- **الاعتمادية:** requests، متغير GOOGLE_TRAFFIC_API_KEY.
- **التوافق:** مستخدم في route_search.py والراوترات المرتبطة بالازدحام.
- **ملاحظات:** إذا لم يوجد مفتاح API، يتم إرجاع بيانات وهمية. يجب الانتباه أمنيًا عند استخدام Google API.

## 3. src/services/traffic_data.py
- **الوظيفة:** مزود بيانات ازدحام مروري مرن (Google/Mock). يدعم جلب المسارات والزمن مع الازدحام.
- **الاعتمادية:** requests، متغيرات GOOGLE_API_KEY وTRAFFIC_PROVIDER.
- **التوافق:** مستخدم في راوتر traffic-data وملفات أخرى.
- **ملاحظات:** يمكن التبديل بين مزودات متعددة. يجب ضبط المفاتيح البيئية بشكل صحيح.

## 4. src/services/route_search.py
- **الوظيفة:** منطق البحث عن أقرب خط مكرو بناءً على نقطة البداية والنهاية، مع تقدير الزمن والتكلفة.
- **الاعتمادية:** geopy, shapely, قاعدة البيانات، خدمات الكاش، traffic.py.
- **التوافق:** مستخدم في راوتر search-route.
- **ملاحظات:** يعتمد على وجود بيانات كافية في قاعدة البيانات (خطوط ومحطات). يدعم الكاش لتسريع البحث. يجب التأكد من صحة البيانات المدخلة.

## 5. src/services/location_share_service.py
- **الوظيفة:** إدارة منطق مشاركة الموقع بين الأصدقاء (إرسال، تحديث، إلغاء، جلب المشاركات النشطة/المستلمة/المرسلة/التاريخ/مواقع الأصدقاء، تنظيف المشاركات المنتهية).
- **الاعتمادية:**
  - النماذج: User, LocationShare, Friendship من models
  - المخططات: LocationShareCreate, LocationShareUpdate من schemas
  - يعتمد على صلاحيات الصداقة (FriendshipStatus)
  - قاعدة البيانات (Session)
- **التوافق:** مستخدم في راوتر location-share، ويجب أن تتوافق جميع استدعاءات الخدمة مع منطق الصداقة والمستخدمين.
- **ملاحظات:**
  - يتحقق من وجود المستخدم والأصدقاء وصلاحية الصداقة قبل المشاركة.
  - يعتمد على الوقت (expires_at) لتحديد صلاحية المشاركة.
  - يجب التأكد من صحة معرفات المستخدمين والأصدقاء في الاختبارات.
  - إذا ظهرت أخطاء 500 أو 400، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.

## 6. src/services/friendship_service.py
- **الوظيفة الأساسية:** إدارة منطق الصداقة بين المستخدمين (إرسال/استقبال/قبول/رفض/إلغاء طلبات الصداقة، حذف صديق، البحث عن مستخدمين، جلب حالة الصداقة).

### شرح تفصيلي لكل وظيفة:
- **send_friend_request(user_id, friend_id):**
  - يتحقق من وجود المستخدمين.
  - يمنع إرسال طلب صداقة لنفسك.
  - يتحقق من عدم وجود علاقة صداقة أو طلب سابق (مقبول أو معلق) بين الطرفين.
  - إذا كان هناك طلب معلق من الطرف الآخر، يعطي رسالة مناسبة.
  - ينشئ طلب صداقة جديد بحالة PENDING.
  - حالات حرجة: إرسال طلب لنفسك، إرسال طلب لمستخدم غير موجود، إرسال طلب لمستخدم سبق وأرسلت له أو أرسل لك.

- **respond_to_friend_request(user_id, friendship_id, status):**
  - يقبل أو يرفض طلب صداقة معلق موجه للمستخدم الحالي.
  - يتحقق من وجود الطلب وأنه معلق.
  - يغير الحالة إلى ACCEPTED أو REJECTED ويحدث وقت التحديث.
  - حالات حرجة: محاولة قبول/رفض طلب غير موجود أو غير موجه للمستخدم.

- **get_friends(user_id):**
  - يجلب جميع الأصدقاء (علاقات الصداقة المقبولة) للمستخدم.
  - يعتمد على كلا الطرفين (user_id أو friend_id).

- **get_friend_requests(user_id):**
  - يجلب جميع طلبات الصداقة المعلقة المستلمة.

- **get_sent_friend_requests(user_id):**
  - يجلب جميع طلبات الصداقة المعلقة المرسلة.

- **remove_friend(user_id, friend_id):**
  - يحذف علاقة الصداقة المقبولة بين المستخدمين.
  - يتحقق من وجود العلاقة.
  - حالات حرجة: محاولة حذف صديق غير موجود.

- **cancel_friend_request(user_id, friendship_id):**
  - يلغي طلب صداقة معلق أرسله المستخدم.
  - يتحقق من وجود الطلب وأنه معلق.

- **search_users(user_id, query, limit):**
  - يبحث عن مستخدمين بالاسم أو اسم المستخدم، مع استبعاد الأصدقاء الحاليين والطلبات المعلقة.
  - يعتمد على is_active.
  - حالات حرجة: البحث عن مستخدمين غير نشطين أو أصدقاء حاليين.

- **get_friendship_status(user_id, other_user_id):**
  - يجلب حالة الصداقة (مقبول، معلق، لا يوجد) بين مستخدمين.

### الاعتمادية:
- النماذج: User, Friendship من models
- المخططات: FriendshipCreate, FriendshipUpdate, FriendshipStatus من schemas
- قاعدة البيانات (Session)

### التوافق مع الراوترات والاختبارات:
- مستخدم في راوتر friends (جميع المسارات تعتمد عليه).
- يجب أن تتوافق جميع استدعاءات الخدمة مع منطق الصداقة (لا يمكن إرسال طلب لنفسك، لا يمكن قبول طلب غير موجه لك، ...).
- يجب اختبار جميع الحالات الحرجة (إرسال/إلغاء/قبول/رفض/حذف/بحث/حالة).

### ملاحظات وتوصيات:
- يجب التأكد من صحة معرفات المستخدمين في جميع العمليات.
- يجب التعامل مع الحالات المتكررة (duplicate requests) برسائل واضحة.
- يجب اختبار منطق البحث بدقة (استبعاد الأصدقاء والطلبات المعلقة).
- إذا ظهرت أخطاء 400 أو 404 أو 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.
- يفضل إضافة اختبارات وحدات (unit tests) لكل حالة حرجة.

---

## 7. src/services/auth_service.py
- **الوظيفة الأساسية:** إدارة منطق المصادقة وتسجيل المستخدمين (محلي/Google)، التحقق من الهوية، تحديث الملف الشخصي.

### شرح تفصيلي لكل وظيفة:
- **create_user(user_data):**
  - يتحقق من عدم وجود مستخدم بنفس البريد أو اسم المستخدم.
  - ينشئ مستخدم جديد مع تشفير كلمة المرور.
  - يعيد المستخدم الجديد بعد الحفظ.
  - حالات حرجة: محاولة تسجيل بريد/اسم مستخدم مستخدم مسبقًا، فشل الحفظ في قاعدة البيانات.

- **authenticate_user(email, password):**
  - يتحقق من وجود المستخدم بالبريد.
  - يتحقق من صحة كلمة المرور (باستخدام دالة verify_password).
  - يعيد المستخدم إذا نجحت المصادقة، أو None إذا فشلت.

- **get_user_by_email / get_user_by_username / get_user_by_id:**
  - جلب مستخدم حسب البريد أو اسم المستخدم أو المعرف.

- **authenticate_google_user(google_data):**
  - يتحقق من صحة توكن Google OAuth.
  - إذا كان المستخدم موجودًا مسبقًا بنفس google_id: يعيده.
  - إذا كان موجودًا بنفس البريد: يربط الحساب بـ Google.
  - إذا لم يكن موجودًا: ينشئ مستخدم جديد بمعلومات Google.
  - حالات حرجة: توكن Google غير صالح، فشل الحفظ، محاولة ربط حسابات بنفس البريد.

- **_generate_username_from_email(email):**
  - ينشئ اسم مستخدم فريد من البريد الإلكتروني (يضيف رقم إذا كان الاسم مستخدمًا).

- **update_user_profile(user_id, **kwargs):**
  - يحدث معلومات المستخدم (الاسم، الصورة، ...).
  - يتحقق من وجود المستخدم.
  - يحدث فقط الحقول المرسلة.

### الاعتمادية:
- النماذج: User من models
- المخططات: UserCreate, UserLogin, GoogleAuthRequest من schemas
- دوال التشفير والتحقق من كلمة المرور وتوليد التوكنات من config/auth.py
- Google OAuth (google-auth)
- قاعدة البيانات (Session)

### التوافق مع الراوترات والاختبارات:
- مستخدم في راوتر auth (جميع مسارات التسجيل/الدخول/Google تعتمد عليه).
- يجب اختبار جميع الحالات الحرجة (تسجيل مستخدم جديد، تسجيل دخول بكلمة مرور خاطئة، تسجيل دخول Google، تحديث الملف الشخصي).
- يجب اختبار منطق ربط الحسابات (Google + بريد موجود).

### ملاحظات وتوصيات:
- يجب التأكد من صحة البريد وكلمة المرور قبل الحفظ.
- يجب التعامل مع الحالات المتكررة (duplicate email/username) برسائل واضحة.
- يجب اختبار منطق Google OAuth بدقة (توكنات غير صالحة، ربط حسابات).
- إذا ظهرت أخطاء 400 أو 401 أو 404 أو 500، تحقق من صحة البيانات المدخلة أو منطق العلاقات بين الجداول.
- يفضل إضافة اختبارات وحدات (unit tests) لكل حالة حرجة.
- يجب الانتباه لأمان كلمة المرور والتخزين المشفر.

---
8. src/services/advanced_analytics_service.py (الجزء الأول: حتى سطر 250)
الوظيفة الأساسية:
خدمة التحليلات المتقدمة للوحة التحكم الحكومية، تشمل التنبؤ بالنمو، الطلب على الخطوط، اتجاهات الشكاوى، مؤشرات الأداء، وغيرها.
أهم الدوال المحللة:
predict_user_growth(days):
يجمع بيانات المستخدمين الجدد يوميًا لآخر 30 يومًا.
يحسب معدل النمو ويستخدم نموذج خطي بسيط للتنبؤ بعدد المستخدمين للأيام القادمة.
يعيد قائمة بتواريخ وتوقعات النمو، مع مستوى ثقة مبني على حجم البيانات.
حالات حرجة: إذا كانت البيانات أقل من 14 يومًا، يعطي تحذيرًا بعدم كفاية البيانات.
predict_route_demand(route_id, days):
يتحقق من صحة route_id ووجوده.
يجمع بيانات الاستخدام التاريخية (عدد الشكاوى المرتبطة بالخط كبديل للبحث).
يحلل الأنماط الأسبوعية ويستخدمها للتنبؤ بالطلب المستقبلي.
حالات حرجة: إذا لم يوجد بيانات كافية (أقل من 7 أيام)، يعطي تحذيرًا بعدم كفاية البيانات.
predict_complaint_trends(days):
يجمع بيانات الشكاوى اليومية.
يحسب الاتجاه (trend) ويستخدمه للتنبؤ بعدد الشكاوى للأيام القادمة.
حالات حرجة: إذا لم يوجد بيانات كافية (أقل من 7 أيام)، يعطي تحذيرًا بعدم كفاية البيانات.
calculate_performance_metrics():
يحسب مؤشرات الأداء الرئيسية (عدد المستخدمين، المستخدمين النشطين، الخطوط، الشكاوى، معدلات الحل، ...).
يستخدم دوال SQL متقدمة وتجميعية.
الاعتمادية:
يعتمد على نماذج: User, Route, Complaint, SearchLog, LocationShare, MakroLocation.
يعتمد على إعدادات التحليلات من config/dashboard_config.py.
يستخدم مكتبات إحصائية (statistics, math) وتجميع البيانات (collections).
ملاحظات وتوصيات:
يجب التأكد من وجود بيانات كافية في قاعدة البيانات (خاصة عند التنبؤ).
يجب اختبار جميع الدوال مع سيناريوهات نقص البيانات.
يجب الانتباه إلى أن بعض التحليلات تعتمد على وجود بيانات تاريخية كافية (وإلا ستظهر تحذيرات أو أخطاء).
يفضل إضافة اختبارات وحدات لكل دالة تحليلية، خاصة التنبؤات.
9. src/schemas/stop.py
الوظيفة:
تعريف مخططات محطة التوقف (Stop) مع تحقق دقيق من صحة البيانات.
تفاصيل الحقول والتحقق:
name: نص غير فارغ.
lat: بين -90 و90.
lng: بين -180 و180.
جميع الحقول تمر عبر field_validator للتحقق من القيم.
StopCreate: نفس StopBase.
StopUpdate: جميع الحقول اختيارية (للتحديث الجزئي).
StopRead: يضيف id ويستخدم from_attributes=True للربط مع ORM.
ملاحظات:
أي قيمة غير صحيحة سترفع ValueError برسالة واضحة.
يضمن التوافق بين البيانات المدخلة وقاعدة البيانات.
10. src/schemas/route_path.py
الوظيفة:
تعريف مخططات نقاط المسار (RoutePath) مع تحقق دقيق من صحة البيانات.
تفاصيل الحقول والتحقق:
route_id: اختياري (للتحديث/القراءة).
lat: بين -90 و90.
lng: بين -180 و180.
point_order: اختياري (ترتيب النقطة على المسار).
جميع الحقول تمر عبر field_validator للتحقق من القيم.
RoutePathCreate وRoutePathUpdate: نفس القاعدة.
RoutePathRead: يضيف id ويستخدم from_attributes=True للربط مع ORM.
ملاحظات:
أي قيمة غير صحيحة سترفع ValueError برسالة واضحة.
يضمن التوافق بين البيانات المدخلة وقاعدة البيانات.

8.1. advanced_analytics_service.py (الجزء الثاني: حتى سطر 500)
تحليل شرائح المستخدمين (analyze_user_segments):
يصنف المستخدمين إلى نشطين، جدد، غير نشطين بناءً على آخر تحديث/تسجيل.
يجمع إحصائيات الشكاوى والمشاركات لكل مستخدم نشط (أول 20).
يحسب "activity_score" لكل مستخدم (وزن الشكاوى ×2 والمشاركات ×3).
يعيد شرائح المستخدمين، سلوكهم، ورؤى تحليلية (insights).
ملاحظات: يعتمد على وجود بيانات كافية في الجداول المرتبطة.
تحليل أداء الخطوط (analyze_route_performance):
يجمع إحصائيات الشكاوى والبحث لكل خط خلال الأسبوع الماضي.
يحسب مؤشر أداء لكل خط بناءً على الشكاوى والبحث والشكاوى المحلولة.
يعيد قائمة الخطوط مرتبة حسب الأداء مع توصيات.
ملاحظات: يدعم وجود أو عدم وجود route_id في SearchLog.
تحليل النقاط الساخنة الجغرافية (analyze_geographic_hotspots):
يجمع عمليات البحث حسب المناطق (تقريب الإحداثيات).
يصنف النقاط الساخنة حسب شدة الاستخدام (high/medium/low).
ملاحظات: يعتمد على وجود بيانات start_lat/start_lng في SearchLog.
تحليل أنماط الحركة (analyze_mobility_patterns):
يجمع المسارات الشائعة (من-إلى) ويصنفها حسب الشعبية.
ملاحظات: يعتمد على وجود بيانات start/end في SearchLog.
11. src/schemas/route.py
الوظيفة:
تعريف مخططات خط السير (Route) مع تحقق دقيق من صحة البيانات.
تفاصيل الحقول والتحقق:
name: نص.
description: نص اختياري.
price: رقم اختياري ≥ 0 (تحقق عبر field_validator).
operating_hours: نص اختياري بصيغة HH:MM-HH:MM (تحقق Regex).
stops وpaths: قائمة محطات ونقاط مسار (لإنشاء/قراءة).
جميع الحقول تمر عبر field_validator للتحقق من القيم.
RouteCreate: يدعم إضافة محطات ونقاط مسار.
RouteUpdate: جميع الحقول اختيارية (للتحديث الجزئي).
RouteRead: يضيف id وقوائم stops/paths ويستخدم from_attributes=True للربط مع ORM.
ملاحظات:
أي قيمة غير صحيحة سترفع ValueError برسالة واضحة.
يضمن التوافق بين البيانات المدخلة وقاعدة البيانات.
صيغة operating_hours الصارمة تمنع الأخطاء في التوقيت.
12. src/schemas/makro_location.py
الوظيفة:
تعريف مخططات موقع المكرو (MakroLocation) مع دعم التواريخ.
تفاصيل الحقول:
makro_id: معرف المكرو (نص).
lat, lng: إحداثيات الموقع (أرقام).
timestamp: وقت الإرسال (اختياري عند الإنشاء، إجباري عند القراءة).
id: معرف السجل (للقراءة فقط).
ملاحظات:
لا يوجد تحقق مخصص (يفترض صحة الإحداثيات والمعرف).
يدعم التكامل مع أجهزة تتبع خارجية بسهولة.



8.2. advanced_analytics_service.py (الجزء الثالث: حتى سطر 750)
أهم الدوال التحليلية والـ Endpoints المرتبطة بها:
analyze_coverage_gaps
يحلل فجوات التغطية الجغرافية (مناطق عليها طلب بحث مرتفع ولا توجد خطوط قريبة).
يعيد قائمة بالمناطق ذات الأولوية (high/medium).
Endpoint: /dashboard/geographic-intelligence (عادةً عبر نوع area_type=coverage)
analyze_complaint_trends
يحلل اتجاهات الشكاوى يوميًا، حسب الخط، ويصنفها حسب النوع (delays, crowding, ...).
يعيد daily_trends, route_analysis, categories, overview.
Endpoint: /dashboard/complaint-intelligence
generate_complaint_insights
يولد رؤى ذكية حول الشكاوى (معدل الحل، الخطوط الحرجة، وقت الاستجابة).
Endpoint: /dashboard/complaint-intelligence (عادةً ضمن insights)
monitor_system_health
يراقب صحة النظام (قاعدة البيانات، الأداء، الأخطاء، التوصيات).
Endpoint: /dashboard/system-health
ملاحظات عامة:
كل دالة تحليلية مرتبطة مباشرة بـ endpoint في راوتر dashboard.
تعتمد النتائج على وجود بيانات كافية في الجداول (SearchLog, Complaint, Route, User).
التصنيفات (high/medium/low) مبنية على إحصائيات حقيقية من قاعدة البيانات.
يجب اختبار كل endpoint مع سيناريوهات نقص البيانات أو وجود بيانات متطرفة.
13. src/schemas/auth.py
أهم المخططات والـ Endpoints المرتبطة بها:
UserCreate, UserLogin, UserResponse
مستخدمة في:
/api/v1/auth/register (UserCreate)
/api/v1/auth/login (UserLogin)
/api/v1/auth/me (UserResponse)
Token, TokenRefresh
مستخدمة في:
/api/v1/auth/login (Token)
/api/v1/auth/refresh (TokenRefresh)
GoogleAuthRequest
مستخدمة في:
/api/v1/auth/google
PasswordResetRequest, PasswordReset, ChangePassword
مستخدمة في:
/api/v1/auth/forgot-password
/api/v1/auth/reset-password
/api/v1/auth/change-password
تفاصيل التحقق:
تحقق من طول اسم المستخدم وكلمة المرور.
البريد الإلكتروني يجب أن يكون صحيح الصيغة (EmailStr).
جميع الحقول الأساسية مطلوبة عند الإنشاء.
UserResponse يضيف حقول الحالة (is_active, is_verified, is_admin) وتواريخ الإنشاء والتحديث.
14. src/schemas/friendship.py
أهم المخططات والـ Endpoints المرتبطة بها:
FriendshipCreate, FriendshipResponse, FriendshipUpdate
مستخدمة في:
/friends/request (FriendshipCreate, FriendshipResponse)
/friends/request/{friendship_id}/respond (FriendshipUpdate, FriendshipResponse)
UserFriendResponse, FriendshipWithUserResponse, FriendRequestResponse
مستخدمة في:
/friends/ (UserFriendResponse)
/friends/requests/received (FriendRequestResponse)
/friends/requests/sent (FriendRequestResponse)
/friends/status/{user_id} (status فقط)
/friends/search (UserFriendResponse)
تفاصيل التحقق:
FriendshipStatus (pending, accepted, rejected) يضبط منطق الحالة.
جميع الحقول الأساسية مطلوبة عند الإنشاء أو التحديث.
UserFriendResponse يضيف is_online (محسوب من النشاط).
جميع المخططات تدعم from_attributes=True للربط مع ORM.
15. src/schemas/location_share.py
أهم المخططات والـ Endpoints المرتبطة بها:
LocationShareCreate, LocationShareResponse, LocationShareUpdate
مستخدمة في:
/location-share/share (LocationShareCreate, LocationShareResponse)
/location-share/{share_id}/update (LocationShareUpdate, LocationShareResponse)
/location-share/{share_id}/cancel (LocationShareCancel)
LocationShareWithUserResponse
مستخدمة في:
/location-share/active
/location-share/received
/location-share/sent
/location-share/history
/location-share/friends/locations
تفاصيل التحقق:
current_lat/lng وdestination_lat/lng: تحقق من النطاق الجغرافي.
friend_ids: قائمة معرفات الأصدقاء (1-10).
duration_hours: بين 1 و24 ساعة.
جميع المخططات تدعم from_attributes=True للربط مع ORM.

8.3. advanced_analytics_service.py (الجزء الرابع: حتى سطر 1000)
أهم الدوال التحليلية والـ Endpoints المرتبطة بها:
_calculate_confidence, get_confidence_level, _analyze_weekly_patterns, _calculate_trend
دوال مساعدة لحساب الثقة في التنبؤات، تحليل الأنماط الأسبوعية، حساب الميل (trend) في البيانات.
تستخدم في: جميع دوال التنبؤ والتحليل في الـ endpoints التالية:
/dashboard/predictive-insights
/dashboard/route-analytics
/dashboard/complaint-intelligence
_classify_user_type, generate_user_insights
تصنيف المستخدمين حسب النشاط، وتوليد رؤى سلوكية.
تستخدم في: /dashboard/user-behavior
_calculate_route_performance_score, generate_route_recommendations
حساب مؤشر أداء الخط وتوليد توصيات ذكية.
تستخدم في: /dashboard/route-analytics, /dashboard/top-routes
_find_nearby_routes
البحث عن خطوط قريبة من نقطة جغرافية (يستخدم في تحليل فجوات التغطية).
تستخدم في: /dashboard/geographic-intelligence
_generate_system_recommendations
توليد توصيات لتحسين النظام بناءً على حالة قاعدة البيانات ومعدل الأخطاء.
تستخدم في: /dashboard/system-health
get_performance_metrics_summary, get_user_segments_summary, ...
دوال تلخيصية تستدعي التحليلات الأساسية وتعيدها بشكل مبسط للـ endpoints.
Endpoints:
/dashboard/real-time-stats
/dashboard/user-behavior
/dashboard/route-analytics
/dashboard/geographic-intelligence
/dashboard/complaint-intelligence
/dashboard/system-health
/dashboard/predictive-insights
/dashboard/recommendations
get_analytics_summary, export_analytics_report
تلخيص شامل أو تصدير تقرير تحليلي (comprehensive/performance/predictive).
Endpoints: غالبًا /dashboard/analytics أو /dashboard/export
ملاحظات عامة:
كل دالة تحليلية مرتبطة مباشرة أو غير مباشرة بـ endpoint في راوتر dashboard.
الدوال المساعدة تضمن دقة التنبؤات والتوصيات.
يجب اختبار كل endpoint مع بيانات متنوعة (كثيرة/قليلة/متطرفة).
16. src/schemas/route_path.py
أهم المخططات والـ Endpoints المرتبطة بها:
RoutePathCreate, RoutePathUpdate, RoutePathRead
مستخدمة في:
/route-paths/ (POST, PUT, GET, DELETE)
/routes/ (عند إنشاء/قراءة خط مع نقاط المسار)
/routes/{route_id} (قراءة نقاط المسار المرتبطة بخط معين)
تفاصيل التحقق:
lat/lng: تحقق من النطاق الجغرافي.
point_order: ترتيب النقطة على المسار (اختياري).
جميع المخططات تدعم from_attributes=True للربط مع ORM.
ملاحظات:
أي قيمة غير صحيحة سترفع ValueError برسالة واضحة.
يضمن التوافق بين البيانات المدخلة وقاعدة البيانات.
يجب اختبار جميع الـ endpoints المرتبطة مع بيانات صحيحة وخاطئة.

8.4. advanced_analytics_service.py (الجزء الأخير: حتى نهاية الملف)
أهم الدوال التحليلية والـ Endpoints المرتبطة بها:
_analyze_seasonal_patterns
يحلل الأنماط الموسمية (ساعات الذروة، الأيام الأكثر نشاطًا).
Endpoints: /dashboard/analytics, /dashboard/predictive-insights
_generate_overall_recommendations
يولد توصيات شاملة بناءً على مؤشرات الأداء (مشاركة المستخدمين، استخدام الخطوط، معدل حل الشكاوى).
Endpoints: /dashboard/recommendations, /dashboard/analytics
get_real_time_insights, generate_real_time_alerts
رؤى وتنبيهات فورية حول نشاط اليوم (بحث، شكاوى، مستخدمين نشطين) مقارنة بالأمس.
Endpoints: /dashboard/real-time-stats
validate_data_quality, identify_quality_issues
يتحقق من جودة البيانات (إحداثيات مفقودة/خاطئة، عمليات بحث مكررة).
Endpoints: غالبًا /dashboard/system-health أو /dashboard/analytics
get_service_usage_statistics
إحصائيات استخدام الخدمة (بحث، شكاوى، مشاركة موقع، مستخدمين جدد) يوميًا وأسبوعيًا.
Endpoints: /dashboard/usage-statistics
_get_peak_usage_hours, get_most_popular_routes
ساعات الذروة، الخطوط الأكثر شعبية.
Endpoints: /dashboard/top-routes, /dashboard/analytics
ملاحظات عامة:
كل دالة تحليلية مرتبطة مباشرة أو غير مباشرة بـ endpoint في راوتر dashboard.
الدوال المساعدة تضمن دقة التوصيات والتنبيهات.
يجب اختبار كل endpoint مع بيانات متنوعة (كثيرة/قليلة/متطرفة).
17. src/schemas/search.py
أهم المخططات والـ Endpoints المرتبطة بها:
SearchRouteRequest, SearchRouteResponse, SuggestedRoute, RouteSegment
مستخدمة في:
/search-route/ (POST)
SearchRouteRequest: طلب البحث (نقطة بداية/نهاية، نوع الفلترة)
SearchRouteResponse: الاستجابة (قائمة المسارات المقترحة)
SuggestedRoute: تفاصيل كل مسار مقترح (id، وصف، مقاطع)
RouteSegment: تفاصيل كل مقطع (مشاة/مكرو، زمن، تكلفة، تعليمات)
تفاصيل التحقق:
start_lat/lng, end_lat/lng: إحداثيات البداية والنهاية.
filter_type: نوع الفلترة (fastest, cheapest, least_transfers).
جميع الحقول مطلوبة في الطلب.
ملاحظات:
أي قيمة غير صحيحة سترفع خطأ تحقق من Pydantic.
يجب اختبار endpoint /search-route/ مع بيانات صحيحة وخاطئة.
18. src/schemas/stop.py
أهم المخططات والـ Endpoints المرتبطة بها:
StopCreate, StopUpdate, StopRead
مستخدمة في:
/stops/ (POST, PUT, GET, DELETE)
/routes/ (عند إنشاء/قراءة خط مع محطات)
/routes/{route_id} (قراءة محطات الخط)
تفاصيل التحقق:
name: نص غير فارغ.
lat: بين -90 و90.
lng: بين -180 و180.
جميع الحقول تمر عبر field_validator للتحقق من القيم.
StopUpdate: جميع الحقول اختيارية (للتحديث الجزئي).
StopRead: يضيف id ويستخدم from_attributes=True للربط مع ORM.
ملاحظات:
أي قيمة غير صحيحة سترفع ValueError برسالة واضحة.
يجب اختبار جميع الـ endpoints المرتبطة مع بيانات صحيحة وخاطئة.

1. friendship.py (مخططات الصداقة)
FriendshipStatus (Enum): يحدد حالات الصداقة (pending, accepted, rejected).
FriendshipBase: يحتوي فقط على friend_id.
FriendshipCreate: يرث من FriendshipBase (لإنشاء طلب صداقة).
FriendshipResponse: يمثل استجابة الصداقة مع جميع الحقول (id, user_id, friend_id, status, created_at, updated_at). يستخدم from_attributes للربط مع ORM.
FriendshipUpdate: لتحديث حالة الصداقة فقط.
UserFriendResponse: معلومات مختصرة عن المستخدم (id, username, full_name, profile_picture, is_online).
FriendshipWithUserResponse: استجابة شاملة للصداقة مع معلومات المستخدم المرتبط.
FriendRequestResponse: استجابة لطلب الصداقة مع معلومات المستخدم.
الربط مع الراوترات:
جميع هذه المخططات تُستخدم في endpoints راوتر friendship (src/routers/friendship.py) مثل:
إرسال طلب صداقة (POST)
قبول/رفض طلب (PATCH)
جلب قائمة الأصدقاء/الطلبات (GET)
التحقق: يعتمد على Enum للحالة، ووجود friend_id، وتحقق من الحقول المطلوبة.
التوافق: المخططات متوافقة مع النماذج وقاعدة البيانات، وتدعم from_attributes للربط مع ORM.
2. location_share.py (مخططات مشاركة الموقع)
LocationSharingStatus (Enum): يحدد حالة المشاركة (active, expired, cancelled).
LocationShareBase: يحتوي على current_lat/lng (إجباري، مع تحقق من النطاق)، destination_lat/lng (اختياري)، اسم الوجهة، وقت الوصول المتوقع، رسالة، مدة المشاركة (1-24 ساعة).
LocationShareCreate: يرث من LocationShareBase ويضيف friend_ids (قائمة أرقام، 1-10 عناصر).
LocationShareResponse: استجابة شاملة لمشاركة الموقع (id, user_id, shared_with_id, current_lat/lng, الوجهة، الحالة، وقت الانتهاء، وقت الإنشاء). يستخدم from_attributes.
LocationShareWithUserResponse: يرث من LocationShareResponse ويضيف user وshared_with (معلومات المستخدمين بشكل dict).
LocationShareUpdate: لتحديث الموقع أو الوجهة أو الرسالة.
LocationShareCancel: لإلغاء المشاركة (يحتوي فقط على share_id).
الربط مع الراوترات:
تُستخدم في endpoints راوتر location_share (src/routers/location_share.py) مثل:
مشاركة الموقع مع أصدقاء (POST)
تحديث الموقع أو الوجهة (PATCH)
إلغاء المشاركة (POST)
جلب المشاركات النشطة (GET)
التحقق: تحقق دقيق من إحداثيات الموقع، وعدد الأصدقاء، والمدة.
التوافق: المخططات متوافقة مع النماذج وقاعدة البيانات، وتدعم from_attributes للربط مع ORM.
ملاحظات عامة:
جميع المخططات تستخدم from_attributes (بديل orm_mode) لضمان التوافق مع Pydantic v2 وما بعده.
التحقق من الحقول يتم عبر Field وEnum، مع تحديد القيم الدنيا/العليا حيث يلزم.
المخططات متوافقة مع الراوترات والنماذج، وتدعم جميع حالات الاستخدام في الـ endpoints الفعلية.

1. makro_location.py (مخططات مواقع الميكرو)
MakroLocationCreate: لإنشاء موقع ميكرو جديد. الحقول:
makro_id (معرّف الميكرو، نصي)
lat/lng (إحداثيات الموقع، أرقام عشرية)
timestamp (تاريخ ووقت اختياري)
MakroLocationRead: لقراءة بيانات موقع ميكرو. الحقول:
id (رقم تسلسلي)
makro_id
lat/lng
timestamp (إجباري هنا)
الربط مع الراوترات:
تُستخدم هذه المخططات في راوتر makro_locations (src/routers/makro_locations.py) في endpoints مثل:
إضافة موقع ميكرو جديد (POST)
جلب مواقع الميكرو (GET)
التحقق: لا يوجد تحقق دقيق على القيم (يفترض أن التحقق يتم في الراوتر أو الخدمة).
التوافق: المخططات بسيطة ومباشرة، متوافقة مع النماذج وقاعدة البيانات.
2. auth.py (مخططات المصادقة والمستخدمين)
UserBase: أساس بيانات المستخدم (username مع تحقق الطول، email، full_name اختياري).
UserCreate: لإنشاء مستخدم جديد (يرث من UserBase ويضيف كلمة مرور مع تحقق الطول).
UserLogin: لتسجيل الدخول (email، password).
UserResponse: استجابة بيانات المستخدم (id، is_active، is_verified، is_admin، profile_picture، created_at، updated_at). يستخدم from_attributes للربط مع ORM.
Token: استجابة التوكن (access_token، refresh_token، النوع، مدة الانتهاء).
TokenRefresh: لتحديث التوكن (refresh_token فقط).
GoogleAuthRequest: للمصادقة عبر Google (code فقط).
PasswordResetRequest: طلب إعادة تعيين كلمة المرور (email).
PasswordReset: إعادة تعيين كلمة المرور (token، new_password مع تحقق الطول).
ChangePassword: تغيير كلمة المرور (current_password، new_password مع تحقق الطول).
الربط مع الراوترات:
تُستخدم هذه المخططات في راوتر auth (src/routers/auth.py) في endpoints مثل:
تسجيل مستخدم جديد (POST /register)
تسجيل الدخول (POST /login)
تحديث التوكن (POST /refresh)
المصادقة عبر Google (POST /google-auth)
إعادة تعيين كلمة المرور (POST /password-reset-request, /password-reset)
تغيير كلمة المرور (POST /change-password)
جلب بيانات المستخدم (GET /me)
التحقق: تحقق دقيق من الحقول (الطول، النوع، البريد الإلكتروني).
التوافق: المخططات متوافقة مع النماذج وقاعدة البيانات، وتدعم from_attributes للربط مع ORM.
ملاحظات عامة:
جميع المخططات تدعم التحقق المناسب للحقول الحساسة (كلمة المرور، البريد الإلكتروني).
التوافق مع الراوترات ممتاز، حيث أن كل مخطط مرتبط مباشرة بعمليات الـ endpoints.
استخدام from_attributes في UserResponse يضمن التوافق مع ORM وPydantic v2+.

search.py (مخططات البحث عن المسارات)
SearchRouteRequest: طلب بحث عن مسار. الحقول:
start_lat, start_lng (إحداثيات البداية)
end_lat, end_lng (إحداثيات النهاية)
filter_type (نوع الفلترة: "fastest", "cheapest", "least_transfers"، افتراضي "fastest")
RouteSegment: جزء من المسار المقترح. الحقول:
type (نوع الجزء: "walk" أو "makro")
distance_meters (المسافة بالمتر، اختياري)
duration_seconds (المدة بالثواني، اختياري)
instructions (تعليمات، اختياري)
makro_id (معرّف الميكرو، اختياري)
start_stop_id, end_stop_id (معرّفات المحطات، اختياري)
estimated_cost (التكلفة التقديرية، اختياري)
SuggestedRoute: مسار مقترح. الحقول:
route_id (معرّف المسار)
description (وصف المسار)
segments (قائمة RouteSegment)
total_estimated_time_seconds (الوقت الكلي التقديري)
total_estimated_cost (التكلفة الكلية التقديرية)
SearchRouteResponse: استجابة البحث عن المسارات. الحقول:
routes (قائمة SuggestedRoute)
الربط مع الراوترات:
تُستخدم هذه المخططات في راوتر search (src/routers/search.py) في endpoints مثل:
البحث عن مسار بين نقطتين (POST /search/route)
التحقق: لا يوجد تحقق دقيق على القيم (يفترض أن التحقق يتم في الراوتر أو الخدمة)، لكن الحقول الأساسية موجودة.
التوافق: المخططات متوافقة مع النماذج وقاعدة البيانات، وتدعم جميع حالات الاستخدام في الـ endpoints الفعلية.
ملاحظات عامة:
المخططات تدعم تعدد أنواع المسارات (مشاة/ميكرو) وتفاصيل كل جزء من الرحلة.
filter_type في الطلب يدعم تخصيص نتائج البحث حسب رغبة المستخدم.
الاستجابة تدعم تعدد المسارات المقترحة، مع تفاصيل دقيقة لكل مسار.

1. src/config/auth.py (إعدادات المصادقة والتشفير)
إعدادات JWT:
SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
تستخدم في إنشاء وتحقق التوكنات (JWT) للمصادقة.
إعدادات Google OAuth:
GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
تدعم تسجيل الدخول عبر Google.
تشفير كلمات المرور:
يستخدم passlib (bcrypt) للتحقق والتشفير.
دوال رئيسية:
verify_password, get_password_hash: للتحقق وتوليد هاش كلمة المرور.
create_access_token, create_refresh_token: لإنشاء توكنات JWT.
verify_token: للتحقق من صحة التوكن ونوعه (access/refresh).
create_tokens: لإنشاء توكنات الدخول والتحديث معًا.
الربط:
تُستخدم هذه الدوال في راوتر auth (src/routers/auth.py) وجميع الخدمات التي تتطلب مصادقة JWT أو تحقق كلمة مرور.
ملاحظات:
جميع المفاتيح الحساسة تُقرأ من متغيرات البيئة (os.getenv).
التحقق من نوع التوكن (access/refresh) يضيف أمانًا إضافيًا.
2. src/config/dashboard_config.py (إعدادات لوحة التحكم والتحليلات)
DASHBOARD_CONFIG:
إعدادات عامة للوحة التحكم (الاسم، الإصدار، الوصف، الصلاحيات، التوقيت، إلخ).
ANALYTICS_CONFIG:
إعدادات التحليلات (الزمن الحقيقي، التنبؤي، الجغرافي، سلوك المستخدم).
PERFORMANCE_CONFIG:
إعدادات الأداء (الكاش، قاعدة البيانات، API).
VISUALIZATION_CONFIG:
إعدادات الرسوم البيانية والخرائط.
ALERT_CONFIG:
إعدادات التنبيهات (القنوات، العتبات، المستلمين).
EXPORT_CONFIG:
إعدادات التصدير (الصيغ، الحجم، القوالب).
SECURITY_CONFIG:
إعدادات الأمان (JWT، المحاولات، القفل، الأدوار، حماية البيانات).
FEATURE_FLAGS:
أعلام الميزات لتفعيل/تعطيل ميزات محددة.
CUSTOMIZATION_CONFIG:
إعدادات التخصيص (الشعار، الألوان، إلخ).
دوال مساعدة:
get_dashboard_config, get_analytics_config, ...: دوال لإرجاع كل قسم من الإعدادات.
is_feature_enabled: للتحقق من تفعيل ميزة.
validate_config: للتحقق من صحة الإعدادات.
get_config_summary: ملخص الإعدادات.
الربط:
تُستخدم هذه الإعدادات في خدمات التحليلات (src/services/advanced_analytics_service.py) وراوتر dashboard (src/routers/dashboard.py) لتخصيص سلوك اللوحة والتحليلات والتنبيهات.
ملاحظات:
الإعدادات شاملة وقابلة للتخصيص عبر متغيرات البيئة.
تدعم تعدد البيئات (development, production) عبر دوال خاصة.
ملاحظات عامة:
ملفات الإعدادات تعتمد بشكل كبير على متغيرات البيئة (os.getenv) لضمان الأمان والمرونة.
جميع الإعدادات مقسمة بشكل منطقي (تحليلات، أداء، أمان، تخصيص...) مع دوال مساعدة للوصول السهل.
الربط مع الخدمات والراوترات واضح، خاصة في المصادقة والتحليلات.

. Route, Stop, RouteStop, RoutePath
Route: يمثل خط سير ميكرو (id, name, description, price, operating_hours). علاقات مع RouteStop, RoutePath, Feedback, Complaint.
Stop: محطة (id, name, lat, lng, geom). علاقة مع RouteStop.
RouteStop: ربط بين Route وStop مع ترتيب المحطة.
RoutePath: نقاط المسار الجغرافية (lat, lng, geom, point_order).
الربط: تُستخدم في راوترات makro_locations, stops, route_paths, routes. متوافقة مع مخططات route.py, stop.py, route_path.py.
2. Feedback, Complaint
Feedback: تقييم أو ملاحظة على Route (type, rating, comment, route_id, timestamp).
Complaint: شكوى على Route أو User أو makro_id (complaint_text, status, timestamp).
الربط: تُستخدم في راوتر dashboard (تحليلات الشكاوى والتقييمات)، متوافقة مع مخططات dashboard/analytics.
3. User (المستخدم)
User: جميع بيانات المستخدم (username, email, hashed_password, full_name, profile_picture, is_active, is_verified, is_admin, google_id, google_email, created_at, updated_at).
علاقات:
complaints (الشكاوى)
sent_friendships, received_friendships (طلبات الصداقة)
location_shares, received_location_shares (مشاركات الموقع)
الربط: تُستخدم في راوتر auth (تسجيل، دخول، بيانات المستخدم)، friendship (الصداقة)، location_share (مشاركة الموقع). متوافقة مع مخططات auth.py, friendship.py, location_share.py.
4. Friendship (الصداقة)
Friendship: ربط بين مستخدمين (user_id, friend_id, status, created_at, updated_at).
الربط: تُستخدم في راوتر friendship، متوافقة مع مخططات friendship.py.
5. LocationShare (مشاركة الموقع)
LocationShare: مشاركة موقع بين مستخدمين (user_id, shared_with_id, current_lat/lng, destination_lat/lng, destination_name, estimated_arrival, message, status, expires_at, created_at).
الربط: تُستخدم في راوتر location_share، متوافقة مع مخططات location_share.py.
6. MakroLocation (مواقع الميكرو)
MakroLocation: موقع ميكرو (makro_id, lat, lng, geom, timestamp).
الربط: تُستخدم في راوتر makro_locations، متوافقة مع مخططات makro_location.py.
7. SearchLog (سجل البحث)
SearchLog: يسجل عمليات البحث عن المسارات (start_lat/lng, end_lat/lng, filter_type, timestamp).
الربط: تُستخدم في راوتر search (تتبع وتحليل عمليات البحث)، متوافقة مع مخططات search.py.
8. Enums (FriendshipStatus, LocationSharingStatus)
FriendshipStatus: (pending, accepted, rejected)
LocationSharingStatus: (active, expired, cancelled)
الربط: تُستخدم في النماذج والمخططات (schemas) لضمان التوافق في التحقق والمنطق.
الملاحظات:
جميع النماذج تعتمد على SQLAlchemy وGeoAlchemy2 (للحقول الجغرافية).
العلاقات بين النماذج واضحة وتدعم جميع العمليات المطلوبة في الراوترات.
الحقول متوافقة مع المخططات (schemas) والهجرات (alembic).
النماذج تدعم جميع السيناريوهات الحرجة (مصادقة، صداقة، مشاركة موقع، شكاوى، تقييمات، بحث).


الجداول التي تم إنشاؤها/تعديلها:
1. friendships
الحقول:
id (مفتاح أساسي)
user_id (مفتاح خارجي إلى users)
friend_id (مفتاح خارجي إلى users)
status (Enum: PENDING, ACCEPTED, REJECTED)
created_at, updated_at (تواريخ)
الربط:
متوافق تمامًا مع نموذج Friendship في models.py ومخططات friendship.py.
العلاقات مع User واضحة (user_id, friend_id).
2. location_shares
الحقول:
id (مفتاح أساسي)
user_id, shared_with_id (مفاتيح خارجية إلى users)
current_lat/lng, destination_lat/lng, destination_name, estimated_arrival, message
status (Enum: ACTIVE, EXPIRED, CANCELLED)
expires_at, created_at (تواريخ)
الربط:
متوافق مع نموذج LocationShare في models.py ومخططات location_share.py.
العلاقات مع User واضحة (user_id, shared_with_id).
3. users (تعديلات وإضافات)
إضافة أعمدة:
hashed_password, full_name, profile_picture, is_active, is_verified, created_at, updated_at, google_id, google_email
تعديلات:
جعل email غير قابل لأن يكون فارغًا (nullable=False)
إضافة قيد فريد على google_id
الربط:
متوافق مع نموذج User في models.py ومخططات auth.py.
يدعم المصادقة التقليدية وOAuth (Google).
ملاحظات حول التوافق:
جميع الحقول الأساسية في النماذج (Friendship, LocationShare, User) ممثلة بدقة في الهجرة.
أنواع البيانات (Enum, String, DateTime, Boolean) متوافقة مع النماذج والمخططات.
العلاقات (ForeignKey) بين الجداول تدعم جميع العمليات المنطقية في الراوترات والخدمات.
لا توجد فروقات أو تعارضات واضحة بين الهجرة والنماذج/المخططات.
ملاحظات إضافية:
الهجرة تدعم التراجع الكامل (downgrade) بإزالة الجداول والتعديلات.
Enum في قاعدة البيانات يحمل نفس القيم المستخدمة في النماذج والمخططات.
إضافة google_id وgoogle_email تدعم المصادقة عبر Google بشكل متكامل.

تحليل ملف الهجرة alembic/versions/35d20bc8818b_init_tables.py يؤكد أن جميع الجداول الأساسية في المشروع متوافقة مع النماذج (models.py) والمخططات (schemas):
الجداول التي تم إنشاؤها:
1. makro_locations
الحقول: id, makro_id, lat, lng, geom (نقطة جغرافية), timestamp
الربط: متوافق مع نموذج MakroLocation في models.py ومخطط makro_location.py
2. routes
الحقول: id, name, description, price, operating_hours
الربط: متوافق مع نموذج Route في models.py ومخطط route.py
3. search_logs
الحقول: id, start_lat/lng, end_lat/lng, filter_type, timestamp
الربط: متوافق مع نموذج SearchLog في models.py ومخطط search.py
4. stops
الحقول: id, name, lat, lng, geom (نقطة جغرافية)
الربط: متوافق مع نموذج Stop في models.py ومخطط stop.py
5. users
الحقول: id, username, email (فريد)
الربط: متوافق مع نموذج User في models.py ومخطط auth.py (مع ملاحظة أن الحقول الإضافية تضاف في هجرات لاحقة)
6. complaints
الحقول: id, user_id, route_id, makro_id, complaint_text, status, timestamp
الربط: متوافق مع نموذج Complaint في models.py
7. feedback
الحقول: id, type, rating, comment, route_id, timestamp
الربط: متوافق مع نموذج Feedback في models.py
8. route_paths
الحقول: id, route_id, lat, lng, geom, point_order
الربط: متوافق مع نموذج RoutePath في models.py ومخطط route_path.py
9. route_stops
الحقول: id, route_id, stop_id, stop_order
الربط: متوافق مع نموذج RouteStop في models.py
الملاحظات:
جميع العلاقات (ForeignKey) بين الجداول تدعم العمليات المنطقية في الراوترات والخدمات.
الحقول الجغرافية (geom) تستخدم geoalchemy2، ما يدعم العمليات الجغرافية في البحث والتحليلات.
الحقول الفريدة (Unique) على email وusername في users تدعم التحقق من التكرار في التسجيل.
الحقول الإضافية للمستخدم (is_active, hashed_password, ...) تضاف في هجرات لاحقة (كما في 9d55d630af12_add_authentication_and_friendship_tables.py).
التوافق مع النماذج والمخططات:
لا توجد فروقات أو تعارضات واضحة بين الهجرة والنماذج/المخططات.
جميع الجداول الأساسية التي تعتمد عليها الخدمات والراوترات موجودة ومهيكلة بشكل صحيح.

1. هجرة إضافة حقل is_admin للمستخدمين
الملف: alembic/versions/6390f52d2174_add_admin_field_to_users.py
المحتوى: إضافة عمود is_admin (Boolean) إلى جدول users.
التوافق: متوافق مع نموذج User في models.py ومخطط UserResponse في schemas/auth.py. يدعم صلاحيات المدير في النظام.
2. التوثيق الرئيسي للمشروع
الملف: README.md
المحتوى:
شرح شامل لإعداد البيئة وقاعدة البيانات.
توثيق جميع الـ APIs الأساسية (routes, stops, search, makro_locations).
تعليمات تشغيل الخادم والاختبارات.
شرح بنية الكود (models, routers, schemas, services, config, alembic).
دعم بيانات الازدحام المروري (Google Traffic API) والكاش المتقدم (Redis).
تعليمات النشر عبر Docker وDocker Compose.
ملاحظات حول الأمان (HTTPS) والتطوير.
التوافق: التوثيق دقيق ومحدث ويغطي جميع الجوانب الفعلية للكود.
3. توثيق لوحة التحكم والتحليلات
الملف: DASHBOARD_README.md
المحتوى:
شرح جميع ميزات لوحة التحكم (إحصائيات فورية، تحليلات تنبؤية، ذكاء جغرافي، تحليل الشكاوى، مراقبة صحة النظام).
أمثلة على استجابات الـ API لكل نوع تحليلي.
توثيق تقنيات الباكند والفرونتند المستخدمة.
أمثلة على واجهات المستخدم (overview, analytics, complaints, system health).
التوافق: التوثيق مفصل ويعكس فعليًا ما هو موجود في الكود وراوتر dashboard.
4. نقطة البداية للتطبيق
الملف: src/main.py
المحتوى:
تهيئة FastAPI مع جميع الراوترات (routes, stops, route_paths, search, makro_locations, traffic, auth, friendship, location_share, dashboard).
إضافة middleware لتسجيل الطلبات.
نقطة جذرية ("/") ترجع رسالة ترحيبية.
التوافق: نقطة البداية شاملة وتربط جميع أجزاء النظام بشكل صحيح.
5. ملف توليد البيانات الأولية
الملف: src/seed.py
المحتوى:
توليد بيانات تجريبية لخطين (routes) مع محطاتهم ومساراتهم.
استخدام SQLAlchemy وGeoAlchemy2 لإضافة بيانات مكانية.
التوافق: يوفر بيانات كافية للاختبار والتجربة، ويغطي السيناريوهات الأساسية.
6. ملفات المهام المساعدة (GiST Indexes)
الملف: src/create_gist_indexes.py
ينشئ فهارس GiST على الحقول الجغرافية (geom) في makro_locations, stops, route_paths.
الملف: src/delete_index.py
يعرض الجداول والفهارس، ويحذف جدول makro_locations (مع الفهارس المرتبطة).
التوافق: تدعم الأداء العالي في الاستعلامات الجغرافية، وتساعد في إدارة البيانات التجريبية.
7. قاعدة النماذج (Base)
الملف: src/models/base.py
المحتوى:
تعريف Base باستخدام SQLAlchemy (declarative_base).
التوافق: أساسي لجميع النماذج، متوافق مع جميع ملفات models.

_تم التحليل بدقة ملفًا ملفًا وسطرًا سطرًا. إذا رغبت في تحليل ملف آخر أو جزء معين من المشروع، يرجى تحديده._ 