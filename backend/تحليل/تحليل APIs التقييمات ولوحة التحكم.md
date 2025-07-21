# تحليل APIs التقييمات ولوحة التحكم

## تحليل ملف `src/routers/feedback.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة التقييمات (Feedback) في النظام. يوفر إرسال التقييمات، جلبها، وحذفها. يعتمد على FastAPI وSQLAlchemy.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /feedback/ | إرسال تقييم جديد | [create_feedback](#create_feedback) |
| GET     | /feedback/ | جلب جميع التقييمات | [get_feedback](#get_feedback) |
| GET     | /feedback/{feedback_id} | جلب تقييم محدد | [get_feedback_by_id](#get_feedback_by_id) |
| DELETE  | /feedback/{feedback_id} | حذف تقييم | [delete_feedback](#delete_feedback) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_feedback"></a>1. إرسال تقييم جديد
- **المسار:** `/feedback/`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن من نوع `FeedbackCreate` (type, rating, comment, route_id)
- **المخرجات:**
  - كائن من نوع `FeedbackRead`
- **المنطق:**
  - ينشئ تقييم جديد مرتبط بالمستخدم الحالي.
  - يحفظ نوع التقييم، التقييم العددي، التعليق، ومعرف الخط.
  - يضيف timestamp تلقائيًا.
- **أمثلة:**
```json
POST /feedback/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "type": "service",
  "rating": 5,
  "comment": "Excellent service!",
  "route_id": 1
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، يربط التقييم بالمستخدم الحالي.

---

#### <a name="get_feedback"></a>2. جلب جميع التقييمات
- **المسار:** `/feedback/`
- **الطريقة:** GET
- **المدخلات:**
  - Query: route_id (int, optional) - لفلترة التقييمات حسب الخط
- **المخرجات:**
  - قائمة من كائنات `FeedbackRead`
- **المنطق:**
  - يجلب جميع التقييمات أو يفلترها حسب route_id إذا تم تحديده.
  - يرتب النتائج حسب التاريخ (الأحدث أولاً).
- **أمثلة:**
```http
GET /feedback/
GET /feedback/?route_id=1
```
- **ملاحظات:** لا يتطلب مصادقة، متاح للجميع.

---

#### <a name="get_feedback_by_id"></a>3. جلب تقييم محدد
- **المسار:** `/feedback/{feedback_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Path: feedback_id (int)
- **المخرجات:**
  - كائن `FeedbackRead`
- **المنطق:**
  - يجلب تقييم محدد حسب المعرف.
  - يعيد خطأ 404 إذا لم يوجد.
- **أمثلة:**
```http
GET /feedback/1
```
- **ملاحظات:** لا يتطلب مصادقة.

---

#### <a name="delete_feedback"></a>4. حذف تقييم
- **المسار:** `/feedback/{feedback_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: feedback_id (int)
- **المخرجات:**
  - {"message": "Feedback deleted successfully"}
- **المنطق:**
  - يتحقق من ملكية المستخدم للتقييم أو كونه مدير.
  - يحذف التقييم من قاعدة البيانات.
- **أمثلة:**
```http
DELETE /feedback/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من الملكية أو صلاحية المدير.

---

### استنتاجات تقنية وتحليل أمني
- نظام تقييمات بسيط وفعال.
- حماية عمليات الإنشاء والحذف بالمصادقة.
- التحقق من الملكية قبل الحذف.
- دعم فلترة التقييمات حسب الخط.

---

### توصيات
- إضافة نظام تقييم متوسط للخطوط.
- إضافة حد أقصى لعدد التقييمات لكل مستخدم لكل خط.
- إضافة نظام الإبلاغ عن التقييمات غير المناسبة.
- تحسين الأداء بإضافة فهارس على route_id وuser_id.

---

## تحليل ملف `src/routers/complaints.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة الشكاوى (Complaints) في النظام. يوفر إرسال الشكاوى، جلبها، تحديثها، وحذفها. يعتمد على FastAPI وSQLAlchemy.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /complaints/ | إرسال شكوى جديدة | [create_complaint](#create_complaint) |
| GET     | /complaints/ | جلب جميع الشكاوى | [get_complaints](#get_complaints) |
| GET     | /complaints/{complaint_id} | جلب شكوى محددة | [get_complaint](#get_complaint) |
| PUT     | /complaints/{complaint_id} | تحديث شكوى | [update_complaint](#update_complaint) |
| DELETE  | /complaints/{complaint_id} | حذف شكوى | [delete_complaint](#delete_complaint) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_complaint"></a>1. إرسال شكوى جديدة
- **المسار:** `/complaints/`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن من نوع `ComplaintCreate` (user_id, route_id, makro_id, complaint_text)
- **المخرجات:**
  - كائن من نوع `ComplaintRead`
- **المنطق:**
  - ينشئ شكوى جديدة مع حالة "pending" افتراضيًا.
  - يضيف timestamp تلقائيًا.
  - يمكن أن تكون الشكوى مرتبطة بمستخدم، خط، أو مكرو.
- **أمثلة:**
```json
POST /complaints/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "user_id": 1,
  "route_id": 2,
  "complaint_text": "There was a significant delay on this route."
}
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_complaints"></a>2. جلب جميع الشكاوى
- **المسار:** `/complaints/`
- **الطريقة:** GET
- **المدخلات:**
  - Query: status (str, optional) - لفلترة الشكاوى حسب الحالة
- **المخرجات:**
  - قائمة من كائنات `ComplaintRead`
- **المنطق:**
  - يجلب جميع الشكاوى أو يفلترها حسب الحالة إذا تم تحديدها.
  - يرتب النتائج حسب التاريخ (الأحدث أولاً).
- **أمثلة:**
```http
GET /complaints/
GET /complaints/?status=pending
```
- **ملاحظات:** يتطلب مصادقة، عادة للمديرين.

---

#### <a name="get_complaint"></a>3. جلب شكوى محددة
- **المسار:** `/complaints/{complaint_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: complaint_id (int)
- **المخرجات:**
  - كائن `ComplaintRead`
- **المنطق:**
  - يجلب شكوى محددة حسب المعرف.
  - يعيد خطأ 404 إذا لم توجد.
- **أمثلة:**
```http
GET /complaints/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="update_complaint"></a>4. تحديث شكوى
- **المسار:** `/complaints/{complaint_id}`
- **الطريقة:** PUT
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: complaint_id (int)
  - Body: كائن من نوع `ComplaintUpdate` (status, complaint_text)
- **المخرجات:**
  - كائن `ComplaintRead` بعد التحديث
- **المنطق:**
  - يتحقق من وجود الشكوى.
  - يحدث الحقول المطلوبة فقط.
  - عادة يستخدم لتغيير حالة الشكوى (resolved, rejected, etc.).
- **أمثلة:**
```json
PUT /complaints/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "status": "resolved"
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، عادة للمديرين.

---

#### <a name="delete_complaint"></a>5. حذف شكوى
- **المسار:** `/complaints/{complaint_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: complaint_id (int)
- **المخرجات:**
  - {"message": "Complaint deleted successfully"}
- **المنطق:**
  - يتحقق من وجود الشكوى.
  - يحذفها من قاعدة البيانات.
- **أمثلة:**
```http
DELETE /complaints/1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhبGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، عادة للمديرين.

---

### استنتاجات تقنية وتحليل أمني
- نظام شكاوى شامل مع دعم حالات مختلفة.
- حماية جميع العمليات بالمصادقة.
- دعم فلترة الشكاوى حسب الحالة.
- مرونة في ربط الشكاوى بمستخدمين، خطوط، أو مكاري.

---

### توصيات
- إضافة نظام إشعارات للشكاوى الجديدة.
- إضافة نظام تصنيف الشكاوى حسب الأولوية.
- إضافة تتبع تاريخ تحديث الشكاوى.
- تحسين الأداء بإضافة فهارس على الحقول المهمة.

---

## تحليل ملف `src/routers/dashboard.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بلوحة التحكم الحكومية (Government Dashboard) في النظام. يوفر إحصائيات شاملة، تقارير، وبيانات تحليلية للمسؤولين الحكوميين. يعتمد على FastAPI وSQLAlchemy مع حسابات إحصائية معقدة.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| GET     | /dashboard/stats | إحصائيات عامة للنظام | [get_system_stats](#get_system_stats) |
| GET     | /dashboard/routes-usage | إحصائيات استخدام الخطوط | [get_routes_usage](#get_routes_usage) |
| GET     | /dashboard/user-activity | نشاط المستخدمين | [get_user_activity](#get_user_activity) |
| GET     | /dashboard/complaints-summary | ملخص الشكاوى | [get_complaints_summary](#get_complaints_summary) |
| GET     | /dashboard/feedback-analysis | تحليل التقييمات | [get_feedback_analysis](#get_feedback_analysis) |
| GET     | /dashboard/search-patterns | أنماط البحث | [get_search_patterns](#get_search_patterns) |
| GET     | /dashboard/makro-activity | نشاط المكاري | [get_makro_activity](#get_makro_activity) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="get_system_stats"></a>1. إحصائيات عامة للنظام
- **المسار:** `/dashboard/stats`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
- **المخرجات:**
  - كائن يحتوي على إحصائيات شاملة
- **المنطق:**
  - يحسب إجمالي عدد المستخدمين، الخطوط، المحطات، الشكاوى، التقييمات.
  - يحسب عدد المستخدمين النشطين (آخر 30 يوم).
  - يحسب متوسط التقييمات.
  - يحسب عدد عمليات البحث اليومية.
- **أمثلة:**
```http
GET /dashboard/stats
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### مثال على الاستجابة:
```json
{
  "total_users": 1250,
  "total_routes": 45,
  "total_stops": 320,
  "total_complaints": 89,
  "total_feedback": 456,
  "active_users_last_30_days": 890,
  "average_rating": 4.2,
  "daily_searches": 1200,
  "pending_complaints": 12,
  "resolved_complaints": 77
}
```
- **ملاحظات أمنية:** يتطلب صلاحية مدير.

---

#### <a name="get_routes_usage"></a>2. إحصائيات استخدام الخطوط
- **المسار:** `/dashboard/routes-usage`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
  - Query: days (int, default=30) - عدد الأيام للتحليل
- **المخرجات:**
  - قائمة من إحصائيات الخطوط
- **المنطق:**
  - يحسب عدد عمليات البحث لكل خط خلال الفترة المحددة.
  - يحسب متوسط التقييمات لكل خط.
  - يحسب عدد الشكاوى لكل خط.
  - يرتب النتائج حسب الاستخدام.
- **أمثلة:**
```http
GET /dashboard/routes-usage?days=7
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### مثال على الاستجابة:
```json
[
  {
    "route_id": 1,
    "route_name": "Line 1",
    "search_count": 450,
    "average_rating": 4.5,
    "complaints_count": 3,
    "feedback_count": 67
  },
  {
    "route_id": 2,
    "route_name": "Line 2", 
    "search_count": 320,
    "average_rating": 3.8,
    "complaints_count": 8,
    "feedback_count": 45
  }
]
```

---

#### <a name="get_user_activity"></a>3. نشاط المستخدمين
- **المسار:** `/dashboard/user-activity`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
  - Query: days (int, default=30) - عدد الأيام للتحليل
- **المخرجات:**
  - كائن يحتوي على إحصائيات نشاط المستخدمين
- **المنطق:**
  - يحسب عدد المستخدمين الجدد يوميًا.
  - يحسب عدد عمليات البحث يوميًا.
  - يحسب عدد التقييمات والشكاوى يوميًا.
  - يحسب أوقات الذروة للاستخدام.
- **أمثلة:**
```http
GET /dashboard/user-activity?days=14
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

#### <a name="get_complaints_summary"></a>4. ملخص الشكاوى
- **المسار:** `/dashboard/complaints-summary`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
- **المخرجات:**
  - كائن يحتوي على ملخص الشكاوى
- **المنطق:**
  - يصنف الشكاوى حسب الحالة (pending, resolved, rejected).
  - يحسب متوسط وقت حل الشكاوى.
  - يحدد الخطوط الأكثر شكاوى.
  - يحسب اتجاهات الشكاوى (زيادة/نقصان).
- **أمثلة:**
```http
GET /dashboard/complaints-summary
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### مثال على الاستجابة:
```json
{
  "total_complaints": 89,
  "pending": 12,
  "resolved": 65,
  "rejected": 12,
  "average_resolution_time_hours": 48,
  "most_complained_routes": [
    {"route_id": 3, "route_name": "Line 3", "complaints": 15},
    {"route_id": 7, "route_name": "Line 7", "complaints": 12}
  ],
  "trend": "decreasing"
}
```

---

#### <a name="get_feedback_analysis"></a>5. تحليل التقييمات
- **المسار:** `/dashboard/feedback-analysis`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
- **المخرجات:**
  - كائن يحتوي على تحليل التقييمات
- **المنطق:**
  - يحسب توزيع التقييمات (1-5 نجوم).
  - يحسب متوسط التقييمات لكل خط.
  - يحدد الخطوط الأعلى والأقل تقييمًا.
  - يحلل اتجاهات التقييمات عبر الوقت.
- **أمثلة:**
```http
GET /dashboard/feedback-analysis
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

#### <a name="get_search_patterns"></a>6. أنماط البحث
- **المسار:** `/dashboard/search-patterns`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
  - Query: days (int, default=30) - عدد الأيام للتحليل
- **المخرجات:**
  - كائن يحتوي على أنماط البحث
- **المنطق:**
  - يحلل أكثر نقاط البداية والنهاية بحثًا.
  - يحسب أوقات الذروة للبحث.
  - يحلل أنواع الفلترة المستخدمة (fastest, cheapest, least_transfers).
  - يحسب متوسط وقت تنفيذ البحث.
- **أمثلة:**
```http
GET /dashboard/search-patterns?days=7
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

#### <a name="get_makro_activity"></a>7. نشاط المكاري
- **المسار:** `/dashboard/makro-activity`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token> (مدير)
  - Query: hours (int, default=24) - عدد الساعات للتحليل
- **المخرجات:**
  - كائن يحتوي على إحصائيات نشاط المكاري
- **المنطق:**
  - يحسب عدد المكاري النشطة.
  - يحلل توزيع المكاري جغرافيًا.
  - يحسب متوسط المسافة المقطوعة.
  - يحدد أوقات الذروة لنشاط المكاري.
- **أمثلة:**
```http
GET /dashboard/makro-activity?hours=12
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

### استنتاجات تقنية وتحليل أمني
- لوحة تحكم شاملة توفر رؤى عميقة عن النظام.
- حماية جميع العمليات بصلاحية المدير.
- تحليلات متقدمة تساعد في اتخاذ القرارات.
- دعم فترات زمنية مختلفة للتحليل.

---

### توصيات
- إضافة تصدير التقارير بصيغ مختلفة (PDF, Excel).
- إضافة رسوم بيانية تفاعلية.
- إضافة تنبيهات تلقائية للمشاكل الحرجة.
- تحسين الأداء بإضافة كاش للإحصائيات.
- إضافة مقارنات تاريخية للبيانات.

---

## تحليل ملف `src/routers/traffic.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة بيانات الازدحام (Traffic) في النظام. يوفر تسجيل بيانات الازدحام، جلبها، وتحليلها. يعتمد على FastAPI وSQLAlchemy.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /traffic/ | تسجيل بيانات ازدحام جديدة | [create_traffic_data](#create_traffic_data) |
| GET     | /traffic/ | جلب بيانات الازدحام | [get_traffic_data](#get_traffic_data) |
| GET     | /traffic/route/{route_id} | جلب ازدحام خط محدد | [get_route_traffic](#get_route_traffic) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="create_traffic_data"></a>1. تسجيل بيانات ازدحام جديدة
- **المسار:** `/traffic/`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن يحتوي على بيانات الازدحام (route_id, congestion_level, timestamp)
- **المخرجات:**
  - كائن يحتوي على بيانات الازدحام المسجلة
- **المنطق:**
  - يسجل مستوى الازدحام لخط معين في وقت محدد.
  - يحفظ البيانات لاستخدامها في تحسين المسارات.
- **أمثلة:**
```json
POST /traffic/
{
  "route_id": 1,
  "congestion_level": 0.7,
  "timestamp": "2024-01-01T08:30:00"
}
```

---

#### <a name="get_traffic_data"></a>2. جلب بيانات الازدحام
- **المسار:** `/traffic/`
- **الطريقة:** GET
- **المدخلات:**
  - Query: hours (int, default=24) - عدد الساعات للبحث
- **المخرجات:**
  - قائمة من بيانات الازدحام
- **المنطق:**
  - يجلب بيانات الازدحام للساعات المحددة.
  - يرتب النتائج حسب الوقت.
- **أمثلة:**
```http
GET /traffic/?hours=12
```

---

#### <a name="get_route_traffic"></a>3. جلب ازدحام خط محدد
- **المسار:** `/traffic/route/{route_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Path: route_id (int)
  - Query: hours (int, default=24) - عدد الساعات للبحث
- **المخرجات:**
  - قائمة من بيانات الازدحام للخط المحدد
- **المنطق:**
  - يجلب بيانات الازدحام لخط محدد خلال الفترة المحددة.
  - يساعد في تحليل أنماط الازدحام لخط معين.
- **أمثلة:**
```http
GET /traffic/route/1?hours=6
```

---

### استنتاجات تقنية وتحليل أمني
- نظام بسيط لتتبع الازدحام.
- يمكن استخدامه لتحسين توصيات المسارات.
- لا يتطلب مصادقة، مما يسهل تسجيل البيانات.

---

### توصيات
- إضافة مصادقة لمنع التلاعب بالبيانات.
- إضافة تحليلات متقدمة للازدحام.
- ربط بيانات الازدحام بخوارزمية البحث.
- إضافة تنبؤات الازدحام باستخدام التعلم الآلي.

