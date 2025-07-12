# مشروع مكروجي (Makroji Backend)

هذا المشروع هو الواجهة الخلفية (Backend) لتطبيق مكروجي لإدارة خطوط المكاري، المحطات، البحث عن المسارات، وتتبع مواقع المكاري في مدينة دمشق.

---

## ما الذي تم إنجازه حتى الآن؟

### 1. **إعداد البيئة وقاعدة البيانات**
- تم إعداد مشروع FastAPI مع PostgreSQL وPostGIS.
- تم إنشاء جميع جداول قاعدة البيانات المطلوبة (خطوط، محطات، مسارات، مواقع مكاري، إلخ) باستخدام Alembic.
- تم إعداد الاتصال بقاعدة البيانات عبر SQLAlchemy.

### 2. **APIs لإدارة خطوط المكاري والمحطات**
- يمكنك إضافة/تعديل/حذف/عرض خطوط المكاري (routes) مع محطاتها ومساراتها.
- يمكنك إدارة المحطات (stops) بشكل منفصل (إضافة، تعديل، حذف، عرض).

### 3. **خدمة البحث عن المسارات**
- يوجد API للبحث عن أفضل مسار بين نقطتين (بناءً على أسرع طريق، أرخص طريق، أقل تبديلات).
- الخدمة تعيد تفاصيل المسار (المشي، ركوب المكرو، التكلفة، الزمن).

### 4. **تتبع مواقع المكاري (MakroLocations)**
- يمكنك إضافة موقع مكرو جديد (POST /makro-locations/).
- يمكنك جلب جميع مواقع المكاري الحالية (GET /makro-locations/).

### 5. **اختبارات شاملة**
- يوجد سكربت اختبار آلي (src/test_full_api.py) يختبر كل وظائف الـ API خطوة بخطوة.
- يشمل الاختبار: الهجرات، الجداول، CRUD، البحث، تتبع المواقع.

## دعم بيانات الازدحام المروري (Google Traffic API)

يدعم النظام دمج بيانات الازدحام المروري في حساب أسرع طريق بين نقطتين، وذلك عبر Google Directions API:

- عند البحث عن "أسرع طريق"، يتم جلب زمن الازدحام الفعلي بين نقطتي البداية والنهاية (إذا كان مفتاح Google API متوفراً).
- إذا لم يكن هناك مفتاح API، يتم استخدام زمن ازدحام وهمي (mock) لأغراض التطوير والاختبار.

### تفعيل الخدمة:
1. احصل على مفتاح Google Directions API من Google Cloud Console.
2. أضف متغير البيئة التالي عند تشغيل الخادم:
   
   ```bash
   export GOOGLE_TRAFFIC_API_KEY=your_google_api_key_here
   ```
3. أعد تشغيل الخادم.

### التأثير:
- عند تفعيل الخدمة، ستأخذ نتائج البحث عن أسرع طريق في الاعتبار الازدحام المروري الفعلي، مما يجعل التقديرات الزمنية أكثر دقة.
- إذا لم يتم تفعيلها، سيبقى النظام يعمل بشكل طبيعي مع تقديرات زمنية ثابتة.

## التخزين المؤقت (Caching) المتقدم

تم توسيع الكاش ليشمل:
- نتائج البحث (search-route)
- بيانات الخطوط (routes)
- بيانات المحطات (stops)
- بيانات لوحة التحكم (dashboard: top-routes, usage-statistics, complaints, heatmap-data, recommendations)

### آلية العمل:
- عند جلب البيانات (GET)، يتم أولًا البحث في الكاش (Redis). إذا كانت البيانات موجودة وصالحة، تُعاد فورًا.
- عند إضافة/تعديل/حذف أي عنصر (route, stop, complaint)، يتم حذف الكاش المرتبط تلقائيًا لضمان التحديث الفوري.
- مفاتيح الكاش واضحة مثل:
  - `routes:all`, `routes:{id}`
  - `stops:all`, `stops:{id}`
  - `dashboard:top-routes`, `dashboard:usage-statistics`, ...

### تخصيص مدة الكاش:
- يمكن تعديل مدة صلاحية الكاش (TTL) لكل نوع بيانات من الكود بسهولة.

### مثال برمجي:
```python
from src.services.cache_service import cache_get, cache_set, redis_client
# جلب جميع الخطوط مع كاش:
cached = cache_get("routes:all")
if cached:
    return cached
# ... جلب من قاعدة البيانات وتخزين في الكاش ...
cache_set("routes:all", result, ttl=300)
```

### حذف الكاش تلقائيًا:
- عند أي تعديل (إضافة/تحديث/حذف)، يتم حذف الكاش المرتبط تلقائيًا:
```python
redis_client.delete("routes:all")
redis_client.delete(f"routes:{route_id}")
```
- في الشكاوى:
```python
from src.services.cache_service import delete_pattern
# حذف جميع كاش الشكاوى:
delete_pattern("dashboard:complaints*")
```

## النشر عبر Docker و Docker Compose

يمكنك تشغيل النظام بالكامل (الخلفية + قاعدة البيانات + Redis) بسهولة عبر Docker:

### 1. بناء وتشغيل الخدمات:

```bash
docker-compose up --build
```

- سيتم تشغيل:
  - قاعدة بيانات PostgreSQL على المنفذ 5432
  - Redis على المنفذ 6379
  - تطبيق FastAPI على المنفذ 8000

### 2. متغيرات البيئة:
- يمكنك ضبط متغير GOOGLE_TRAFFIC_API_KEY في ملف .env أو مباشرة في سطر الأوامر.
- يمكنك تعديل DB_URL وREDIS_URL حسب الحاجة.

### 3. إيقاف جميع الخدمات:

```bash
docker-compose down
```

### 4. ملاحظات:
- تأكد من أن المنافذ 5432 و6379 و8000 غير مستخدمة مسبقًا.
- يمكنك الدخول إلى الحاوية الخلفية عبر:

```bash
docker-compose exec backend bash
```

---

## كيف يعمل المشروع؟

1. **تشغيل السيرفر:**
   - شغّل قاعدة بيانات PostgreSQL مع PostGIS.
   - شغّل السيرفر:
     ```bash
     uvicorn src.main:app --reload
     ```
   - ستجد التوثيق التفاعلي للـ API على: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

2. **تشغيل الاختبارات:**
   - شغّل سكربت الاختبار:
     ```bash
     python src/test_full_api.py
     ```
   - إذا نجح كل شيء ستظهر رسالة نجاح شاملة.

3. **إضافة بيانات أو تجربة الـ API:**
   - استخدم Swagger UI أو Postman لإرسال طلبات إلى أي endpoint (routes, stops, search-route, makro-locations).

---

## بنية الكود

- **src/models/**: نماذج ORM للجداول.
- **src/routers/**: جميع مسارات الـ API (routes, stops, search, makro_locations ...).
- **src/schemas/**: مخططات البيانات (Pydantic) للتحقق من صحة البيانات.
- **src/services/**: منطق الأعمال (مثل البحث عن المسارات).
- **config/**: إعدادات الاتصال بقاعدة البيانات.
- **alembic/**: إدارة ترحيلات قاعدة البيانات.

---

## ملاحظات
- كل شيء مبني على FastAPI وSQLAlchemy وPostGIS.
- جميع البيانات الجغرافية (المواقع) تُخزن وتُدار بشكل مكاني (GIS).
- الكود منظم وقابل للتوسعة لإضافة ميزات جديدة (feedback، الشكاوى، لوحة التحكم الحكومية، إلخ).

---

## للمطورين
- يمكنك البدء بإضافة ميزات جديدة بسهولة عبر إضافة راوتر جديد وschemas جديدة.
- كل endpoint موثق تلقائيًا في Swagger UI.
- يمكنك تعديل قاعدة البيانات عبر Alembic ثم تشغيل:
  ```bash
  alembic upgrade head
  ```

---

أي استفسار أو اقتراح تطوير؟ لا تتردد في التواصل مع مطور المشروع! 

## تفعيل HTTPS (اتصال مشفر وآمن)

لضمان الأمان الكامل، يجب تشغيل التطبيق دائمًا عبر HTTPS في بيئة الإنتاج. التفعيل يعتمد على بيئة السيرفر:

### 1. **النشر عبر Nginx (موصى به للإنتاج)**
- استخدم ملف `nginx.conf` المرفق مع المشروع:

```nginx
server {
    listen 80;
    server_name your_domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your_domain.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

- **توليد شهادة SSL مجانية (Let's Encrypt):**
```bash
sudo apt update && sudo apt install certbot
sudo certbot certonly --nginx -d your_domain.com
```
- عدّل مسارات الشهادة في nginx.conf حسب مخرجات certbot.
- أعد تحميل nginx:
```bash
sudo systemctl reload nginx
```

### 2. **النشر عبر Docker/Docker Compose**
- يمكنك استخدام Nginx كخدمة reverse proxy في docker-compose وربطه مع backend.
- تأكد من تمرير متغيرات البيئة الصحيحة (DB, REDIS, GOOGLE_TRAFFIC_API_KEY).
- يمكنك استخدام Traefik أو Caddy كبدائل تدعم SSL تلقائيًا.

### 3. **تشغيل محلي (للتطوير فقط)**
- يمكنك استخدام self-signed certificate:
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
- ثم تشغيل Uvicorn:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```
- **ملاحظة:** المتصفحات ستظهر تحذيرًا لأن الشهادة غير موثوقة.

### 4. **فرض HTTPS من الكود (اختياري/للتطوير فقط)**
- يفضل دائمًا فرض HTTPS من Nginx أو Traefik، لكن يمكنك إضافة Middleware في FastAPI:
```python
from fastapi import Request
from fastapi.responses import RedirectResponse

@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if request.url.scheme != "https":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url)
    return await call_next(request)
```
- **لا يُنصح بتفعيل هذا في الإنتاج إذا كان هناك Nginx/Traefik.**

### 5. **حماية الكوكيز وCORS**
- عند استخدام الكوكيز (مثلاً JWT في الكوكيز)، استخدم دائمًا:
  - `secure=True` (لمنع الإرسال عبر HTTP)
  - `httponly=True` (لمنع وصول الجافاسكريبت)
- تأكد من ضبط إعدادات CORS في FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your_domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. **أفضل الممارسات الأمنية**
- لا تشغل التطبيق أبدًا في الإنتاج على HTTP فقط.
- لا تحفظ الشهادات أو المفاتيح في مستودع الكود.
- استخدم متغيرات البيئة لإدارة الأسرار.
- راقب صلاحية الشهادات وجددها تلقائيًا (certbot يدعم ذلك).

---

## نظام التسجيل (Logging) المتقدم

يدعم النظام تسجيلًا متقدمًا عبر Python logging:

- **logs/app.log**: جميع العمليات والمعلومات العامة (INFO).
- **logs/error.log**: جميع الأخطاء (ERROR وما فوق).
- **logs/access.log**: كل طلب HTTP (الطريقة، المسار، الحالة، عنوان العميل).
- تدوير تلقائي للملفات (rotating).

### أمثلة على التسجيل:
- كل طلب HTTP يُسجل تلقائيًا في access.log.
- أي خطأ في نقطة نهاية يُسجل في error.log تلقائيًا.
- يمكنك إضافة تسجيل مخصص في أي مكان عبر:

```python
import logging
logging.info("عملية مهمة تمت بنجاح")
logging.error("حدث خطأ غير متوقع")
```

### دعم ELK/Sentry:
- يمكنك بسهولة ربط logging مع ELK (Filebeat/Logstash) أو Sentry عبر تغيير Handlers في logging_config.py.
- النظام جاهز للتوسع لأي نظام مراقبة مركزي. 

## طبقة بيانات الازدحام المروري (Traffic Provider Abstraction)

يدعم النظام جلب بيانات الازدحام من Google Directions API أو أي مزود آخر بسهولة عبر طبقة تجريدية:

- يمكنك اختيار المزود عبر متغير البيئة:
  - `TRAFFIC_PROVIDER=google` (الافتراضي)
  - `TRAFFIC_PROVIDER=mock` (للاختبار)
  - يمكن إضافة مزودات أخرى بسهولة
- يتم حقن مفتاح Google API عبر متغير البيئة `GOOGLE_API_KEY`.
- إذا لم يوجد مفتاح أو فشل الاتصال، يتم استخدام mock تلقائيًا.

### مثال برمجي:
```python
from src.services.traffic_data import get_directions_with_traffic
# جلب بيانات المسار مع الازدحام:
result = get_directions_with_traffic(33.5, 36.3, 33.6, 36.4)
```

### إضافة مزود جديد:
- أنشئ كلاس جديد يرث من `BaseTrafficProvider` وفعّل الدوال المطلوبة.
- أضف شرطًا في دالة `get_traffic_provider()` لربط اسم المزود بالكلاس.

```python
class MyTrafficProvider(BaseTrafficProvider):
    def get_directions(...):
        ...
# ثم في get_traffic_provider():
if provider == "my":
    return MyTrafficProvider()
```

### التبديل بين المزودات:
- فقط غيّر متغير البيئة `TRAFFIC_PROVIDER` ولن تحتاج لتعديل أي كود آخر. 