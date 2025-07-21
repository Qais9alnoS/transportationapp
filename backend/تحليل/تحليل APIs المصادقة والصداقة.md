# تحليل APIs المصادقة والصداقة

## تحليل ملف `src/routers/auth.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بالمصادقة (Authentication) وإدارة المستخدمين في النظام. يوفر تسجيل المستخدمين، تسجيل الدخول، إدارة الرموز المميزة (tokens)، وإدارة ملفات المستخدمين الشخصية. يعتمد على FastAPI وJWT وOAuth2 وGoogle OAuth.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /auth/register | تسجيل مستخدم جديد | [register](#register) |
| POST    | /auth/login | تسجيل الدخول | [login](#login) |
| POST    | /auth/refresh | تجديد الرمز المميز | [refresh_token](#refresh_token) |
| GET     | /auth/me | جلب بيانات المستخدم الحالي | [get_current_user_info](#get_current_user_info) |
| PUT     | /auth/me | تحديث بيانات المستخدم الحالي | [update_current_user](#update_current_user) |
| POST    | /auth/upload-profile-picture | رفع صورة الملف الشخصي | [upload_profile_picture](#upload_profile_picture) |
| POST    | /auth/google | تسجيل الدخول عبر Google | [google_auth](#google_auth) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="register"></a>1. تسجيل مستخدم جديد
- **المسار:** `/auth/register`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `UserCreate` (username, email, password, full_name, is_admin)
- **المخرجات:**
  - كائن من نوع `UserWithToken` (بيانات المستخدم + access_token + refresh_token)
- **المنطق:**
  - يتحقق من عدم تكرار البريد الإلكتروني أو اسم المستخدم.
  - يشفر كلمة المرور باستخدام bcrypt.
  - ينشئ المستخدم في قاعدة البيانات.
  - يولد رموز الوصول والتجديد.
- **أمثلة:**
```json
POST /auth/register
{
  "username": "user1",
  "email": "user1@email.com",
  "password": "12345678",
  "full_name": "User One",
  "is_admin": false
}
```
- **ملاحظات أمنية:** كلمة المرور مشفرة، التحقق من التكرار، إنشاء رموز آمنة.

---

#### <a name="login"></a>2. تسجيل الدخول
- **المسار:** `/auth/login`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `UserLogin` (email, password)
- **المخرجات:**
  - كائن Token (access_token, refresh_token, token_type, expires_in)
- **المنطق:**
  - يتحقق من وجود المستخدم بالبريد الإلكتروني.
  - يتحقق من صحة كلمة المرور.
  - يولد رموز الوصول والتجديد.
- **أمثلة:**
```json
POST /auth/login
{
  "email": "user1@email.com",
  "password": "12345678"
}
```
- **ملاحظات أمنية:** التحقق من كلمة المرور مشفرة، إنشاء رموز آمنة.

---

#### <a name="refresh_token"></a>3. تجديد الرمز المميز
- **المسار:** `/auth/refresh`
- **الطريقة:** POST
- **المدخلات:**
  - Body: {"refresh_token": "..."}
- **المخرجات:**
  - كائن Token جديد
- **المنطق:**
  - يتحقق من صحة رمز التجديد.
  - يولد رمز وصول جديد.
- **أمثلة:**
```json
POST /auth/refresh
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **ملاحظات أمنية:** التحقق من صحة رمز التجديد قبل إنشاء رمز جديد.

---

#### <a name="get_current_user_info"></a>4. جلب بيانات المستخدم الحالي
- **المسار:** `/auth/me`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - كائن من نوع `UserResponse`
- **المنطق:**
  - يستخرج المستخدم من الرمز المميز.
  - يعيد بيانات المستخدم.
- **أمثلة:**
```http
GET /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب رمز وصول صحيح.

---

#### <a name="update_current_user"></a>5. تحديث بيانات المستخدم الحالي
- **المسار:** `/auth/me`
- **الطريقة:** PUT
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن تحديث المستخدم (username, email, full_name)
- **المخرجات:**
  - كائن من نوع `UserResponse` بعد التحديث
- **المنطق:**
  - يستخرج المستخدم من الرمز المميز.
  - يحدث البيانات المطلوبة فقط.
  - يتحقق من عدم تكرار البريد الإلكتروني أو اسم المستخدم.
- **أمثلة:**
```json
PUT /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "full_name": "Updated Name"
}
```
- **ملاحظات أمنية:** يتطلب رمز وصول صحيح، التحقق من التكرار.

---

#### <a name="upload_profile_picture"></a>6. رفع صورة الملف الشخصي
- **المسار:** `/auth/upload-profile-picture`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Form: file (UploadFile)
- **المخرجات:**
  - {"message": "Profile picture uploaded successfully", "profile_picture": "path/to/file"}
- **المنطق:**
  - يتحقق من نوع الملف (صورة).
  - يحفظ الملف في مجلد uploads/profile_pictures/.
  - يحدث مسار الصورة في قاعدة البيانات.
- **أمثلة:**
```http
POST /auth/upload-profile-picture
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: multipart/form-data
file: [image file]
```
- **ملاحظات أمنية:** يتطلب رمز وصول صحيح، التحقق من نوع الملف.

---

#### <a name="google_auth"></a>7. تسجيل الدخول عبر Google
- **المسار:** `/auth/google`
- **الطريقة:** POST
- **المدخلات:**
  - Body: {"token": "google_oauth_token"}
- **المخرجات:**
  - كائن من نوع `UserWithToken`
- **المنطق:**
  - يتحقق من صحة رمز Google OAuth.
  - يجلب بيانات المستخدم من Google.
  - ينشئ مستخدم جديد أو يسجل دخول المستخدم الموجود.
- **أمثلة:**
```json
POST /auth/google
{
  "token": "google_oauth_token_here"
}
```
- **ملاحظات أمنية:** التحقق من صحة رمز Google، إنشاء أو تحديث المستخدم.

---

### استنتاجات تقنية وتحليل أمني
- نظام مصادقة قوي يعتمد على JWT مع رموز الوصول والتجديد.
- دعم OAuth2 مع Google للتسجيل السريع.
- تشفير كلمات المرور باستخدام bcrypt.
- التحقق من التكرار في البريد الإلكتروني واسم المستخدم.
- دعم رفع الملفات مع التحقق من النوع.
- حماية جميع العمليات الحساسة بالمصادقة.

---

### توصيات
- إضافة تحقق من قوة كلمة المرور.
- إضافة نظام تأكيد البريد الإلكتروني.
- إضافة نظام استرداد كلمة المرور.
- تحسين أمان رفع الملفات (حجم، نوع، مسح الفيروسات).
- إضافة rate limiting لمنع هجمات brute force.

---

## تحليل ملف `src/routers/friendship.py`

### نظرة عامة

هذا الملف مسؤول عن جميع نقاط النهاية (APIs) المتعلقة بإدارة علاقات الصداقة بين المستخدمين في النظام. يوفر إرسال طلبات الصداقة، قبولها أو رفضها، وإدارة قوائم الأصدقاء. يعتمد على FastAPI وSQLAlchemy.

---

### قائمة نقاط النهاية (APIs) في هذا الملف

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /friends/request | إرسال طلب صداقة | [send_friend_request](#send_friend_request) |
| POST    | /friends/respond | الرد على طلب صداقة | [respond_to_friend_request](#respond_to_friend_request) |
| GET     | /friends/ | جلب قائمة الأصدقاء | [get_friends](#get_friends) |
| GET     | /friends/requests | جلب طلبات الصداقة المعلقة | [get_friend_requests](#get_friend_requests) |
| DELETE  | /friends/{friend_id} | حذف صديق | [remove_friend](#remove_friend) |

---

### تحليل وتوثيق كل API بالتفصيل

#### <a name="send_friend_request"></a>1. إرسال طلب صداقة
- **المسار:** `/friends/request`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن من نوع `FriendshipCreate` (friend_id)
- **المخرجات:**
  - كائن من نوع `FriendshipResponse`
- **المنطق:**
  - يتحقق من وجود المستخدم المطلوب إضافته.
  - يتحقق من عدم وجود علاقة صداقة سابقة.
  - ينشئ طلب صداقة بحالة "pending".
- **أمثلة:**
```json
POST /friends/request
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "friend_id": 2
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من وجود المستخدم، منع التكرار.

---

#### <a name="respond_to_friend_request"></a>2. الرد على طلب صداقة
- **المسار:** `/friends/respond`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن من نوع `FriendshipUpdate` (friend_id, status)
- **المخرجات:**
  - كائن من نوع `FriendshipResponse`
- **المنطق:**
  - يجد طلب الصداقة المعلق.
  - يحدث حالة الطلب (accepted/rejected).
  - إذا تم القبول، ينشئ علاقة صداقة متبادلة.
- **أمثلة:**
```json
POST /friends/respond
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "friend_id": 1,
  "status": "accepted"
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من وجود الطلب، إنشاء علاقة متبادلة.

---

#### <a name="get_friends"></a>3. جلب قائمة الأصدقاء
- **المسار:** `/friends/`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `FriendshipWithUserResponse`
- **المنطق:**
  - يجلب جميع علاقات الصداقة المقبولة للمستخدم الحالي.
  - يضمن العلاقات المتبادلة (في كلا الاتجاهين).
- **أمثلة:**
```http
GET /friends/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، يعرض فقط الأصدقاء المقبولين.

---

#### <a name="get_friend_requests"></a>4. جلب طلبات الصداقة المعلقة
- **المسار:** `/friends/requests`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `FriendRequestResponse`
- **المنطق:**
  - يجلب جميع طلبات الصداقة المعلقة الموجهة للمستخدم الحالي.
- **أمثلة:**
```http
GET /friends/requests
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، يعرض فقط الطلبات المعلقة.

---

#### <a name="remove_friend"></a>5. حذف صديق
- **المسار:** `/friends/{friend_id}`
- **الطريقة:** DELETE
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: friend_id (int)
- **المخرجات:**
  - {"message": "Friend removed successfully"}
- **المنطق:**
  - يجد علاقة الصداقة بين المستخدم الحالي والصديق.
  - يحذف العلاقة من كلا الاتجاهين.
- **أمثلة:**
```http
DELETE /friends/2
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، حذف العلاقة المتبادلة.

---

### استنتاجات تقنية وتحليل أمني
- نظام صداقة متكامل يدعم الطلبات والردود.
- العلاقات متبادلة (إذا A صديق B، فإن B صديق A).
- حماية جميع العمليات بالمصادقة.
- التحقق من وجود المستخدمين قبل إنشاء العلاقات.
- منع التكرار في طلبات الصداقة.

---

### توصيات
- إضافة إشعارات للطلبات الجديدة والردود.
- إضافة حد أقصى لعدد الأصدقاء.
- إضافة نظام حظر المستخدمين.
- تحسين الأداء بإضافة فهارس على جدول friendships.
- إضافة إحصائيات عن عدد الأصدقاء والطلبات.

---

## نقاط نهاية إضافية وتحليل مفصل

### أولاً: نقاط نهاية المصادقة (auth) الإضافية

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| POST    | /auth/forgot-password | طلب إعادة تعيين كلمة المرور | [forgot_password](#forgot_password) |
| POST    | /auth/reset-password | إعادة تعيين كلمة المرور | [reset_password](#reset_password) |
| POST    | /auth/change-password | تغيير كلمة المرور للمستخدم الحالي | [change_password](#change_password) |
| GET     | /auth/google/url | جلب رابط Google OAuth | [get_google_auth_url](#get_google_auth_url) |
| GET     | /auth/profile | جلب الملف الشخصي للمستخدم الحالي | [get_user_profile](#get_user_profile) |
| PUT     | /auth/profile | تحديث الملف الشخصي للمستخدم الحالي | [update_user_profile](#update_user_profile) |

---

#### <a name="forgot_password"></a>1. طلب إعادة تعيين كلمة المرور
- **المسار:** `/auth/forgot-password`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `PasswordResetRequest` (email)
- **المخرجات:**
  - {"message": "If the email exists, a password reset link has been sent"}
- **المنطق:**
  - يتحقق من وجود المستخدم بالبريد الإلكتروني.
  - إذا وجد، يرسل رابط إعادة تعيين كلمة المرور (في التطبيق الحالي رسالة فقط، لكن في الإنتاج يجب إرسال بريد إلكتروني).
  - لا يكشف إذا كان البريد موجودًا أم لا (لأسباب أمنية).
- **أمثلة:**
```json
POST /auth/forgot-password
{
  "email": "user@email.com"
}
```
- **ملاحظات أمنية:** لا يكشف عن وجود البريد، لمنع جمع بيانات المستخدمين.

---

#### <a name="reset_password"></a>2. إعادة تعيين كلمة المرور
- **المسار:** `/auth/reset-password`
- **الطريقة:** POST
- **المدخلات:**
  - Body: كائن من نوع `PasswordReset` (عادة: token, new_password)
- **المخرجات:**
  - {"message": "Password reset successfully"}
- **المنطق:**
  - يتحقق من صحة رمز إعادة التعيين (token).
  - إذا كان صالحًا، يغير كلمة المرور للمستخدم.
- **أمثلة:**
```json
POST /auth/reset-password
{
  "token": "reset_token_here",
  "new_password": "newStrongPassword123"
}
```
- **ملاحظات أمنية:** يجب التحقق من صلاحية الرمز، وتشفير كلمة المرور الجديدة.

---

#### <a name="change_password"></a>3. تغيير كلمة المرور للمستخدم الحالي
- **المسار:** `/auth/change-password`
- **الطريقة:** POST
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن من نوع `ChangePassword` (current_password, new_password)
- **المخرجات:**
  - {"message": "Password changed successfully"}
- **المنطق:**
  - يتحقق من صحة كلمة المرور الحالية.
  - إذا كانت صحيحة، يغير كلمة المرور إلى الجديدة (مع التشفير).
- **أمثلة:**
```json
POST /auth/change-password
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "current_password": "oldPass123",
  "new_password": "newStrongPass456"
}
```
- **ملاحظات أمنية:** التحقق من كلمة المرور الحالية، وتشفير الجديدة.

---

#### <a name="get_google_auth_url"></a>4. جلب رابط Google OAuth
- **المسار:** `/auth/google/url`
- **الطريقة:** GET
- **المدخلات:** لا شيء
- **المخرجات:**
  - {"auth_url": "https://accounts.google.com/o/oauth2/v2/auth?..."}
- **المنطق:**
  - يبني رابط OAuth الخاص بـ Google مع جميع المعاملات المطلوبة (client_id, redirect_uri, scope...).
  - يستخدم في الواجهة الأمامية لبدء تسجيل الدخول عبر Google.
- **أمثلة:**
```http
GET /auth/google/url
```
- **ملاحظات تقنية:** يجب أن تكون القيم (client_id, redirect_uri) صحيحة ومطابقة لإعدادات Google Console.

---

#### <a name="get_user_profile"></a>5. جلب الملف الشخصي للمستخدم الحالي
- **المسار:** `/auth/profile`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - كائن من نوع `UserResponse`
- **المنطق:**
  - يستخرج المستخدم من الرمز المميز.
  - يعيد بيانات الملف الشخصي (full_name, profile_picture, ...).
- **أمثلة:**
```http
GET /auth/profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="update_user_profile"></a>6. تحديث الملف الشخصي للمستخدم الحالي
- **المسار:** `/auth/profile`
- **الطريقة:** PUT
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Body: كائن يحتوي على الحقول المسموح بتحديثها (full_name, profile_picture)
- **المخرجات:**
  - كائن من نوع `UserResponse` بعد التحديث
- **المنطق:**
  - يحدث فقط الحقول المسموح بها (full_name, profile_picture).
  - يحفظ التغييرات في قاعدة البيانات.
- **أمثلة:**
```json
PUT /auth/profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "full_name": "New Name",
  "profile_picture": "path/to/new/pic.png"
}
```
- **ملاحظات أمنية:** لا يمكن تحديث الحقول الحساسة (مثل is_admin أو البريد).

---

### استنتاجات تقنية وتحليل أمني (إضافي)
- النظام يدعم استعادة كلمة المرور وتغييرها بشكل آمن.
- لا يكشف عن وجود البريد الإلكتروني في النظام.
- تحديث الملف الشخصي مقيد للحقول المسموح بها فقط.
- جلب رابط Google OAuth يسهل التكامل مع الواجهة الأمامية.

### توصيات (إضافية)
- تفعيل إرسال البريد الإلكتروني الفعلي في forgot/reset-password.
- إضافة تحقق من قوة كلمة المرور الجديدة.
- مراقبة محاولات إعادة تعيين كلمة المرور لمنع الإساءة.

---

### ثانياً: نقاط نهاية الصداقة (friendship) الإضافية

| الطريقة | المسار | الوظيفة | التوثيق |
|---------|--------|---------|---------|
| PUT     | /friends/request/{friendship_id}/respond | الرد على طلب صداقة (قبول/رفض) | [respond_to_friend_request_ex](#respond_to_friend_request_ex) |
| GET     | /friends/requests/received | جلب الطلبات المستلمة | [get_received_friend_requests](#get_received_friend_requests) |
| GET     | /friends/requests/sent | جلب الطلبات المرسلة | [get_sent_friend_requests](#get_sent_friend_requests) |
| DELETE  | /friends/request/{friendship_id}/cancel | إلغاء طلب صداقة مرسل | [cancel_friend_request](#cancel_friend_request) |
| GET     | /friends/search | البحث عن مستخدمين | [search_users](#search_users) |
| GET     | /friends/status/{user_id} | جلب حالة الصداقة مع مستخدم آخر | [get_friendship_status](#get_friendship_status) |

---

#### <a name="respond_to_friend_request_ex"></a>1. الرد على طلب صداقة (قبول/رفض)
- **المسار:** `/friends/request/{friendship_id}/respond`
- **الطريقة:** PUT
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: friendship_id (int)
  - Body: كائن من نوع `FriendshipUpdate` (status: accepted/rejected)
- **المخرجات:**
  - كائن من نوع `FriendshipResponse`
- **المنطق:**
  - يتحقق من وجود الطلب للمستخدم الحالي.
  - يحدث حالة الطلب (accepted/rejected).
  - إذا تم القبول، ينشئ علاقة صداقة متبادلة.
- **أمثلة:**
```json
PUT /friends/request/5/respond
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
{
  "status": "accepted"
}
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من ملكية الطلب.

---

#### <a name="get_received_friend_requests"></a>2. جلب الطلبات المستلمة
- **المسار:** `/friends/requests/received`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `FriendRequestResponse`
- **المنطق:**
  - يجلب جميع طلبات الصداقة المعلقة الموجهة للمستخدم الحالي.
- **أمثلة:**
```http
GET /friends/requests/received
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_sent_friend_requests"></a>3. جلب الطلبات المرسلة
- **المسار:** `/friends/requests/sent`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
- **المخرجات:**
  - قائمة من كائنات `FriendRequestResponse`
- **المنطق:**
  - يجلب جميع طلبات الصداقة المرسلة من المستخدم الحالي والتي لم يتم الرد عليها بعد.
- **أمثلة:**
```http
GET /friends/requests/sent
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="cancel_friend_request"></a>4. إلغاء طلب صداقة مرسل
- **المسار:** `/friends/request/{friendship_id}/cancel`
- **الطريقة:** DELETE
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: friendship_id (int)
- **المخرجات:**
  - {"message": "Friend request cancelled successfully"}
- **المنطق:**
  - يتحقق من ملكية الطلب.
  - يحذف الطلب من قاعدة البيانات.
- **أمثلة:**
```http
DELETE /friends/request/5/cancel
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة، التحقق من ملكية الطلب.

---

#### <a name="search_users"></a>5. البحث عن مستخدمين
- **المسار:** `/friends/search`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Query: query (string, اسم المستخدم أو الاسم الكامل), limit (int, افتراضي 10)
- **المخرجات:**
  - قائمة من كائنات `UserFriendResponse`
- **المنطق:**
  - يبحث عن مستخدمين آخرين بناءً على الاسم أو اسم المستخدم.
  - يستثني المستخدم الحالي وأصدقاءه الحاليين.
- **أمثلة:**
```http
GET /friends/search?query=ahmad&limit=5
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

#### <a name="get_friendship_status"></a>6. جلب حالة الصداقة مع مستخدم آخر
- **المسار:** `/friends/status/{user_id}`
- **الطريقة:** GET
- **المدخلات:**
  - Header: Authorization: Bearer <access_token>
  - Path: user_id (int)
- **المخرجات:**
  - {"status": "accepted" | "pending" | "none"}
- **المنطق:**
  - يتحقق من وجود علاقة صداقة أو طلب مع المستخدم المحدد.
  - يعيد الحالة (مقبول، معلق، لا يوجد).
- **أمثلة:**
```http
GET /friends/status/7
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
- **ملاحظات أمنية:** يتطلب مصادقة.

---

### استنتاجات تقنية وتحليل أمني (إضافي)
- النظام يدعم إدارة كاملة لطلبات الصداقة (إرسال، قبول، رفض، إلغاء، جلب المرسلة والمستلمة).
- البحث عن المستخدمين يسهل إضافة الأصدقاء الجدد.
- جلب حالة الصداقة يحسن تجربة المستخدم في الواجهة.
- جميع العمليات محمية بالمصادقة والتحقق من الملكية.

### توصيات (إضافية)
- إضافة إشعارات عند قبول/رفض/إلغاء الطلبات.
- مراقبة محاولات البحث لمنع الإساءة.
- دعم التصفية والفرز في البحث عن المستخدمين.

