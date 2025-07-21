# تحليل مفصل وشامل لملفات Schemas (Pydantic) في المشروع

هذا الملف يشرح جميع نماذج البيانات (schemas) المستخدمة في النظام الخلفي (backend)، ويوضح كيفية استعمال كل نموذج في الـ API، مع أمثلة عملية وتوضيح العلاقات بين النماذج. الهدف هو أن يكون مرجعًا عمليًا لأي مطور يريد فهم أو استعمال الـ API أو تطويرها.

---

## 1. نماذج المستخدمين والمصادقة (auth.py)

### UserBase / UserCreate / UserLogin / UserResponse / UserWithToken

- **UserBase**: الأساس لكل مستخدم (username, email, full_name)
- **UserCreate**: لإنشاء مستخدم جديد (يضيف password, is_admin)
- **UserLogin**: بيانات تسجيل الدخول (email, password)
- **UserResponse**: بيانات المستخدم المسترجعة من النظام (id, is_active, is_verified, is_admin, profile_picture, created_at, updated_at)
- **UserWithToken**: يجمع بيانات المستخدم مع رموز التوكن (access_token, refresh_token, token_type, expires_in)

#### أمثلة استعمال في الـ API:
- **تسجيل مستخدم جديد:**
  - Endpoint: `POST /auth/register`
  - Body:
    ```json
    {
      "username": "user1",
      "email": "user1@email.com",
      "password": "12345678",
      "full_name": "User One"
    }
    ```
  - Response: UserWithToken

- **تسجيل الدخول:**
  - Endpoint: `POST /auth/login`
  - Body:
    ```json
    {
      "email": "user1@email.com",
      "password": "12345678"
    }
    ```
  - Response: Token

- **جلب بيانات المستخدم الحالي:**
  - Endpoint: `GET /auth/me`
  - Header: `Authorization: Bearer <access_token>`
  - Response: UserResponse

---

## 2. نماذج خطوط النقل (route.py)

### RouteBase / RouteCreate / RouteUpdate / RouteRead

- **RouteBase**: الأساس (name, description, price, operating_hours) مع تحقق من صحة السعر وصيغة ساعات العمل.
- **RouteCreate**: لإنشاء خط جديد (يضيف قائمة المحطات والمسارات)
- **RouteUpdate**: لتحديث خط (جميع الحقول اختيارية)
- **RouteRead**: لقراءة خط (يضيف id، وقوائم المحطات والمسارات المرتبطة)

#### أمثلة استعمال في الـ API:
- **إنشاء خط جديد:**
  - Endpoint: `POST /routes/`
  - Body:
    ```json
    {
      "name": "Route 1",
      "description": "Main route",
      "price": 1000,
      "operating_hours": "06:00-22:00",
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
  - Response: RouteRead

- **جلب جميع الخطوط:**
  - Endpoint: `GET /routes/`
  - Response: List[RouteRead]

---

## 3. نماذج المحطات (stop.py)

### StopBase / StopCreate / StopUpdate / StopRead

- **StopBase**: الأساس (name, lat, lng) مع تحقق من صحة الإحداثيات والاسم.
- **StopCreate**: لإنشاء محطة جديدة.
- **StopUpdate**: لتحديث محطة (جميع الحقول اختيارية).
- **StopRead**: لقراءة محطة (يضيف id).

#### أمثلة استعمال في الـ API:
- **إنشاء محطة جديدة:**
  - Endpoint: `POST /stops/`
  - Body:
    ```json
    {
      "name": "Stop 1",
      "lat": 33.5,
      "lng": 36.3
    }
    ```
  - Response: StopRead

- **جلب جميع المحطات:**
  - Endpoint: `GET /stops/`
  - Response: List[StopRead]

---

## 4. نماذج نقاط المسار (route_path.py)

### RoutePathBase / RoutePathCreate / RoutePathUpdate / RoutePathRead

- **RoutePathBase**: الأساس (route_id, lat, lng, point_order) مع تحقق من صحة الإحداثيات.
- **RoutePathCreate**: لإنشاء نقطة مسار جديدة.
- **RoutePathUpdate**: لتحديث نقطة مسار.
- **RoutePathRead**: لقراءة نقطة مسار (يضيف id).

#### أمثلة استعمال في الـ API:
- **إضافة نقطة مسار:**
  - Endpoint: `POST /route-paths/`
  - Body:
    ```json
    {
      "route_id": 1,
      "lat": 33.5,
      "lng": 36.3,
      "point_order": 1
    }
    ```
  - Response: RoutePathRead

---

## 5. نماذج علاقات الصداقة (friendship.py)

### FriendshipStatus / FriendshipBase / FriendshipCreate / FriendshipResponse / FriendshipUpdate / UserFriendResponse / FriendshipWithUserResponse / FriendRequestResponse

- **FriendshipStatus**: Enum لحالة الصداقة (pending, accepted, rejected)
- **FriendshipBase/FriendshipCreate**: الأساس لإنشاء علاقة صداقة (friend_id)
- **FriendshipResponse**: تفاصيل علاقة الصداقة (id, user_id, friend_id, status, created_at, updated_at)
- **FriendshipUpdate**: لتحديث حالة الصداقة
- **UserFriendResponse**: معلومات مختصرة عن المستخدم (id, username, full_name, profile_picture, is_online)
- **FriendshipWithUserResponse**: علاقة صداقة مع تفاصيل المستخدم المرتبط
- **FriendRequestResponse**: تفاصيل طلب الصداقة مع معلومات المستخدم

#### أمثلة استعمال في الـ API:
- **إرسال طلب صداقة:**
  - Endpoint: `POST /friends/request`
  - Body:
    ```json
    { "friend_id": 2 }
    ```
  - Response: FriendshipResponse

- **جلب جميع الأصدقاء:**
  - Endpoint: `GET /friends/`
  - Response: List[FriendshipWithUserResponse]

---

## 6. نماذج مشاركة الموقع (location_share.py)

### LocationSharingStatus / LocationShareBase / LocationShareCreate / LocationShareResponse / LocationShareWithUserResponse / LocationShareUpdate / LocationShareCancel

- **LocationSharingStatus**: Enum لحالة المشاركة (active, expired, cancelled)
- **LocationShareBase**: الأساس (current_lat, current_lng, destination_lat/lng/name, estimated_arrival, message, duration_hours)
- **LocationShareCreate**: لإنشاء مشاركة موقع (يضيف friend_ids)
- **LocationShareResponse**: تفاصيل المشاركة (id, user_id, shared_with_id, current_lat/lng, destination_lat/lng/name, estimated_arrival, message, status, expires_at, created_at)
- **LocationShareWithUserResponse**: مشاركة موقع مع تفاصيل المستخدمين
- **LocationShareUpdate/LocationShareCancel**: لتحديث أو إلغاء المشاركة

#### أمثلة استعمال في الـ API:
- **مشاركة الموقع مع صديق:**
  - Endpoint: `POST /location-share/`
  - Body:
    ```json
    {
      "current_lat": 33.5,
      "current_lng": 36.3,
      "destination_lat": 33.6,
      "destination_lng": 36.4,
      "destination_name": "Home",
      "friend_ids": [2],
      "duration_hours": 2
    }
    ```
  - Response: LocationShareResponse

---

## 7. نماذج التقييمات (feedback.py)

### FeedbackCreate / FeedbackRead

- **FeedbackCreate**: لإرسال تقييم (type, rating, comment, route_id)
- **FeedbackRead**: لقراءة تقييم (id, type, rating, comment, route_id, timestamp)

#### أمثلة استعمال في الـ API:
- **إرسال تقييم:**
  - Endpoint: `POST /feedback/`
  - Body:
    ```json
    {
      "type": "service",
      "rating": 5,
      "comment": "Excellent!",
      "route_id": 1
    }
    ```
  - Response: FeedbackRead

---

## 8. نماذج الشكاوى (complaint.py)

### ComplaintCreate / ComplaintRead / ComplaintUpdate

- **ComplaintCreate**: لإرسال شكوى (user_id, route_id, makro_id, complaint_text)
- **ComplaintRead**: لقراءة شكوى (id, user_id, route_id, makro_id, complaint_text, status, timestamp)
- **ComplaintUpdate**: لتحديث الشكوى (status, complaint_text)

#### أمثلة استعمال في الـ API:
- **إرسال شكوى:**
  - Endpoint: `POST /complaints/`
  - Body:
    ```json
    {
      "user_id": 1,
      "route_id": 2,
      "complaint_text": "There was a delay."
    }
    ```
  - Response: ComplaintRead

---

## 9. نماذج مواقع المكاري (makro_location.py)

### MakroLocationCreate / MakroLocationRead

- **MakroLocationCreate**: لإرسال موقع مكرو (makro_id, lat, lng, timestamp)
- **MakroLocationRead**: لقراءة موقع مكرو (id, makro_id, lat, lng, timestamp)

#### أمثلة استعمال في الـ API:
- **إرسال موقع مكرو:**
  - Endpoint: `POST /makro-locations/`
  - Body:
    ```json
    {
      "makro_id": "makro_123",
      "lat": 33.5,
      "lng": 36.3
    }
    ```
  - Response: MakroLocationRead

---

## 10. نماذج البحث عن خطوط النقل (search.py)

### SearchRouteRequest / RouteSegment / SuggestedRoute / SearchRouteResponse

- **SearchRouteRequest**: طلب البحث (start_lat/lng, end_lat/lng, filter_type)
- **RouteSegment**: مقطع من المسار المقترح (type, distance, duration, instructions, makro_id, start_stop_id, end_stop_id, estimated_cost)
- **SuggestedRoute**: خط مقترح (route_id, description, segments, total_estimated_time_seconds, total_estimated_cost)
- **SearchRouteResponse**: استجابة البحث (routes)

#### أمثلة استعمال في الـ API:
- **البحث عن خط نقل:**
  - Endpoint: `POST /search-route/`
  - Body:
    ```json
    {
      "start_lat": 33.5,
      "start_lng": 36.3,
      "end_lat": 33.6,
      "end_lng": 36.4,
      "filter_type": "fastest"
    }
    ```
  - Response: SearchRouteResponse

---

## تحليل Alembic وملفات الترحيل (Migrations)

### 1. ملفات Alembic الأساسية

#### alembic/env.py
- **الغرض:** ضبط بيئة Alembic لتوليد وتطبيق ترحيلات قاعدة البيانات (migrations) بشكل ديناميكي.
- **آلية العمل:**
  - يستورد إعدادات الاتصال بقاعدة البيانات من config/database.py.
  - يحمّل جميع النماذج (ORM models) من src/models/base وsrc/models/models، ويجمع الـ metadata الخاص بها في target_metadata، ما يتيح دعم التوليد التلقائي للهجرات.
  - يدعم نمطين للتشغيل:
    - **offline:** توليد سكريبتات SQL فقط دون اتصال فعلي بقاعدة البيانات (مناسب لمراجعة التغييرات يدويًا).
    - **online:** تطبيق التغييرات مباشرة على قاعدة البيانات عبر SQLAlchemy Engine.
  - يسجل جميع العمليات في ملف اللوغ إذا كان ذلك مفعّلًا.
- **أهمية الملف:** أي تغيير في النماذج (models) سينعكس تلقائيًا في الهجرات الجديدة بفضل target_metadata.

#### alembic/script.py.mako
- **الغرض:** قالب لإنشاء ملفات الترحيل الجديدة تلقائيًا.
- **محتواه:**
  - رأس الملف يحتوي على معلومات الترحيل (revision, down_revision, تاريخ الإنشاء).
  - دوال upgrade وdowngrade:
    - **upgrade:** تكتب فيها أوامر إنشاء/تعديل الجداول أو الأعمدة.
    - **downgrade:** تكتب فيها أوامر التراجع عن التغييرات (حذف الجداول أو الأعمدة).
- **أهمية الملف:** يضمن توحيد شكل جميع ملفات الترحيل وسهولة تتبع التغييرات.

#### alembic/README
- **محتواه:**
  - ملاحظة مختصرة: "Generic single-database configuration."
  - لا يحتوي على تفاصيل تقنية إضافية، فقط يوضح أن الإعدادات تدعم قاعدة بيانات واحدة.

---

### 2. ملفات الترحيل (migrations) في alembic/versions

#### 35d20bc8818b_init_tables.py
- **الغرض:** إنشاء الجداول الأساسية للنظام في أول ترحيل.
- **الجداول التي تم إنشاؤها:**
  - **makro_locations:** لتخزين مواقع المكاري (يدعم بيانات جغرافية عبر geoalchemy2).
  - **routes:** خطوط النقل (اسم، وصف، سعر، ساعات عمل).
  - **search_logs:** سجلات عمليات البحث (إحداثيات البداية والنهاية، نوع الفلترة، وقت التنفيذ).
  - **stops:** المحطات (اسم، إحداثيات، نقطة جغرافية).
  - **users:** المستخدمون (اسم مستخدم، بريد إلكتروني، مع قيود فريدة).
  - **complaints:** الشكاوى (مرتبطة بالمستخدم أو الخط أو المكرو).
  - **feedback:** التقييمات (نوع، تقييم عددي، تعليق، مرتبط بخط).
  - **route_paths:** نقاط مسار الخط (إحداثيات، ترتيب، نقطة جغرافية، مرتبطة بخط).
  - **route_stops:** ربط الخطوط بالمحطات (ترتيب المحطة ضمن الخط).
- **ملاحظات تقنية:**
  - كل جدول يحتوي على فهارس (indexes) لتحسين الأداء.
  - العلاقات بين الجداول معرفة عبر Foreign Keys (مثلاً: complaints.user_id → users.id).
  - يدعم البيانات الجغرافية (geoalchemy2) في الجداول التي تتطلب ذلك.
- **دالة downgrade:** تحذف جميع الجداول والفهارس التي تم إنشاؤها، ما يسمح بالتراجع الكامل عن الترحيل.

#### 9d55d630af12_add_authentication_and_friendship_tables.py
- **الغرض:** إضافة جداول المصادقة والصداقة وتوسيع جدول المستخدمين.
- **الجداول التي تم إنشاؤها:**
  - **friendships:** علاقات الصداقة بين المستخدمين (user_id, friend_id, status [PENDING, ACCEPTED, REJECTED]، تواريخ الإنشاء والتحديث).
  - **location_shares:** مشاركة الموقع بين المستخدمين (user_id, shared_with_id، إحداثيات الموقع الحالي والوجهة، حالة المشاركة [ACTIVE, EXPIRED, CANCELLED]، تواريخ الانتهاء والإنشاء).
- **تعديلات على جدول users:**
  - إضافة أعمدة: hashed_password, full_name, profile_picture, is_active, is_verified, created_at, updated_at, google_id, google_email.
  - جعل email غير قابل للإهمال (nullable=False).
  - إضافة قيد فريد على google_id.
- **ملاحظات تقنية:**
  - يدعم حالات منطقية عبر ENUMs (status).
  - جميع العلاقات معرفة عبر Foreign Keys.
- **دالة downgrade:** تحذف الجداول والتعديلات المضافة، وتعيد جدول users إلى حالته السابقة.

---

### 3. أمثلة عملية على استعمال Alembic

- **توليد ترحيل جديد تلقائيًا بعد تعديل النماذج:**
  ```bash
  alembic revision --autogenerate -m "Add new field to users"
  ```
- **تطبيق جميع الترحيلات على قاعدة البيانات:**
  ```bash
  alembic upgrade head
  ```
- **التراجع عن آخر ترحيل:**
  ```bash
  alembic downgrade -1
  ```
- **مراجعة تاريخ الترحيلات:**
  ```bash
  alembic history
  ```

---

### 4. الخلاصة حول Alembic في المشروع

- نظام الترحيلات منظم جدًا ويغطي تطور قاعدة البيانات خطوة بخطوة.
- كل ترحيل موثق بدوال upgrade/downgrade واضحة، مع دعم العلاقات والفهارس والبيانات الجغرافية.
- env.py يضمن أن أي تغيير في النماذج ينعكس تلقائيًا في الترحيلات الجديدة.
- يمكن لأي مطور تتبع تطور قاعدة البيانات أو التراجع عن أي تغيير بسهولة.
- أمثلة الأوامر أعلاه تسهل إدارة الترحيلات في بيئة التطوير والإنتاج.

---

## تحليل ملف الاختبارات الشاملة (test_comprehensive.py)

### نظرة عامة

- ملف test_comprehensive.py يحتوي على اختبارات شاملة تغطي جميع جوانب الـ API والوظائف الأساسية للنظام.
- يستخدم مكتبة requests لاختبار نقاط النهاية الحقيقية (integration tests).
- يغطي:
  - اختبارات البيئة وقاعدة البيانات والهجرات
  - اختبارات المصادقة (تسجيل مستخدم/مدير، تسجيل الدخول، جلب المستخدم الحالي، تسجيل دخول خاطئ)
  - اختبارات CRUD للمحطات، الخطوط، نقاط المسار
  - اختبارات البحث عن الخطوط
  - اختبارات علاقات الصداقة ومشاركة الموقع
  - اختبارات الشكاوى والتقييمات
  - اختبارات مواقع المكاري
  - اختبارات لوحة التحكم (dashboard)
  - اختبارات الأداء (rate limiting, response time, concurrent requests)
  - اختبارات الاتصال بقاعدة البيانات والتعامل مع الأخطاء

### أمثلة عملية على بعض الاختبارات:

- **تسجيل مستخدم جديد:**
  - يقوم بإرسال POST إلى `/api/v1/auth/register` مع بيانات المستخدم، ويتحقق من الاستجابة ووجود id.
- **تسجيل الدخول:**
  - يرسل POST إلى `/api/v1/auth/login` ويتحقق من وجود access_token.
- **إنشاء محطة جديدة:**
  - يرسل POST إلى `/api/v1/stops/` مع بيانات المحطة، ويتحقق من الاستجابة.
- **البحث عن خط نقل:**
  - يرسل POST إلى `/api/v1/search-route/` مع إحداثيات البداية والنهاية، ويتحقق من وجود نتائج.
- **إرسال شكوى:**
  - يرسل POST إلى `/api/v1/complaints/` مع بيانات الشكوى، ويتحقق من الاستجابة.
- **مشاركة الموقع مع صديق:**
  - يرسل POST إلى `/api/v1/location-share/` مع بيانات الموقع وقائمة الأصدقاء.

### ملاحظات تقنية:
- جميع الاختبارات تستخدم assert_status للتحقق من رمز الاستجابة.
- يتم طباعة نتيجة كل اختبار بشكل واضح (PASS/FAIL) مع تفاصيل الخطأ إن وجدت.
- يمكن تشغيل جميع الاختبارات دفعة واحدة عبر دالة run_all_tests().
- يتم اختبار الأداء والضغط على النظام (concurrent requests, response time).
- يتم اختبار صحة الهجرات وقاعدة البيانات قبل بدء اختبارات الـ API.

### كيفية تشغيل الاختبارات:
- تأكد من تشغيل السيرفر على العنوان الصحيح (BASE_URL)
- شغّل الملف:
  ```bash
  python src/test_comprehensive.py
  ```
- راقب النتائج في الطرفية، حيث ستظهر PASS/FAIL لكل اختبار مع التفاصيل.

---

# ملاحظات ختامية

- هذا التحليل يغطي جميع ملفات schemas، نقطة الدخول الرئيسية، وملف الاختبارات الشاملة، مع أمثلة عملية وتوضيح العلاقات والاستخدامات البرمجية.
- يمكن لأي مطور الاعتماد على هذا الملف لفهم كيفية استعمال الـ API، اختبارها، أو تطويرها.
- جميع الأمثلة المذكورة مأخوذة من الكود الفعلي ويمكن تجربتها مباشرة عبر Postman أو Swagger UI أو عبر سكريبتات بايثون. 


