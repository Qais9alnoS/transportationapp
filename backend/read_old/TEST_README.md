# 🧪 دليل الاختبارات الشاملة - مشروع مكروجي

## 📋 نظرة عامة

هذا الدليل يوضح كيفية تشغيل الاختبارات الشاملة لمشروع مكروجي، والتي تغطي جميع ميزات النظام من الأساسية إلى المتقدمة.

## 🚀 الملفات المتاحة

### 1. `test_comprehensive.py` - الاختبارات الشاملة
الملف الرئيسي الذي يحتوي على **80+ اختبار** يغطي جميع ميزات المشروع.

### 2. `test_api.py` - الاختبارات الأساسية
اختبارات سريعة للـ API الأساسية (6 اختبارات).

### 3. `test_full_api.py` - الاختبارات المتوسطة
اختبارات متوسطة الشمولية (13 اختبار).

## 🛠️ المتطلبات

```bash
# تثبيت المكتبات المطلوبة
pip install requests sqlalchemy psycopg2-binary

# التأكد من تشغيل الخادم
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# التأكد من تشغيل قاعدة البيانات
# PostgreSQL مع PostGIS
```

## 🎯 تشغيل الاختبارات

### الاختبارات الشاملة (الموصى بها)
```bash
python src/test_comprehensive.py
```

### الاختبارات الأساسية
```bash
python src/test_api.py
```

### الاختبارات المتوسطة
```bash
python src/test_full_api.py
```

## 📊 فئات الاختبارات

### 🔐 **نظام المصادقة (8 اختبارات)**
- ✅ تسجيل مستخدمين عاديين ومديرين
- ✅ تسجيل الدخول والخروج
- ✅ Google OAuth
- ✅ إعادة تعيين كلمة المرور
- ✅ إدارة الملف الشخصي
- ✅ التحقق من الصلاحيات

### 🚏 **إدارة المحطات (7 اختبارات)**
- ✅ إنشاء محطات جديدة
- ✅ جلب محطات محددة وجميع المحطات
- ✅ تحديث وحذف المحطات
- ✅ العمليات المجمعة
- ✅ الاستعلامات الجغرافية

### 🚌 **إدارة الخطوط (8 اختبارات)**
- ✅ إنشاء خطوط جديدة مع محطات ومسارات
- ✅ جلب خطوط محددة وجميع الخطوط
- ✅ تحديث وحذف الخطوط
- ✅ إدارة محطات ومسارات الخط
- ✅ تحسين المسارات

### 🔍 **البحث عن المسارات (4 اختبارات)**
- ✅ البحث عن أسرع مسار
- ✅ البحث عن أرخص مسار
- ✅ البحث عن مسار بأقل تبديلات
- ✅ سجلات البحث

### 👥 **نظام الصداقة (4 اختبارات)**
- ✅ إرسال طلبات صداقة
- ✅ جلب طلبات الصداقة
- ✅ قبول طلبات الصداقة
- ✅ جلب قائمة الأصدقاء

### 📍 **مشاركة الموقع (2 اختبارات)**
- ✅ مشاركة موقع المستخدم
- ✅ جلب مواقع الأصدقاء

### 📝 **الشكاوى والملاحظات (4 اختبارات)**
- ✅ إنشاء شكاوى وملاحظات
- ✅ جلب الشكاوى والملاحظات

### 🚗 **تتبع مواقع المكروجي (3 اختبارات)**
- ✅ إنشاء مواقع مكروجي
- ✅ جلب وتحديث مواقع المكروجي

### 🏛️ **لوحة تحكم الحكومة (7 اختبارات)**
- ✅ تحليلات شاملة
- ✅ التنبؤات والذكاء الاصطناعي
- ✅ الذكاء الجغرافي
- ✅ تحليل الشكاوى
- ✅ صحة النظام
- ✅ المقاييس في الوقت الفعلي
- ✅ جمع البيانات التحليلية

### 🔒 **الأمان والصلاحيات (5 اختبارات)**
- ✅ التحقق من صلاحيات المدير
- ✅ حماية النقاط المحمية
- ✅ تحديد معدل الطلبات
- ✅ رؤوس CORS
- ✅ رؤوس نوع المحتوى

### ⚡ **الأداء والاستقرار (4 اختبارات)**
- ✅ قياس وقت استجابة API
- ✅ الطلبات المتزامنة
- ✅ تجمع اتصالات قاعدة البيانات
- ✅ آلية التخزين المؤقت

### 🛡️ **معالجة الأخطاء (3 اختبارات)**
- ✅ معالجة الأخطاء العامة
- ✅ نظام التسجيل
- ✅ التراجع عن المعاملات

### 📄 **واجهة المستخدم (2 اختبارات)**
- ✅ الصفحات
- ✅ التصفية والترتيب

### ✅ **التحقق من البيانات (3 اختبارات)**
- ✅ التحقق من صحة البيانات
- ✅ حالات حدودية للتحقق
- ✅ قيود قاعدة البيانات

### 🏥 **صحة النظام (3 اختبارات)**
- ✅ فحص صحة النظام
- ✅ نقطة نهاية المقاييس
- ✅ توثيق API

## 📈 فهم النتائج

### ✅ نجح
- الاختبار اكتمل بنجاح
- جميع التأكيدات صحيحة
- النتيجة كما هو متوقع

### ❌ فشل
- حدث خطأ أثناء الاختبار
- فشل في أحد التأكيدات
- استجابة غير متوقعة

### 📊 الإحصائيات
```
📊 نتائج الاختبارات:
✅ نجح: 75
❌ فشل: 2
📈 نسبة النجاح: 97.4%
```

## 🔧 إعدادات الاختبار

### متغيرات البيئة
```python
BASE_URL = "http://127.0.0.1:8000"
DB_URL = "postgresql://postgres:PostgreSQL@localhost:5432/makroji_db_clean"
```

### تعديل الإعدادات
يمكنك تعديل هذه المتغيرات في بداية الملف حسب إعداداتك:

```python
# تغيير عنوان الخادم
BASE_URL = "http://your-server:8000"

# تغيير إعدادات قاعدة البيانات
DB_URL = "postgresql://username:password@host:port/database"
```

## 🐛 استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### 1. خطأ في الاتصال بالخادم
```
❌ Connection refused
```
**الحل:** تأكد من تشغيل الخادم
```bash
uvicorn main:app --reload
```

#### 2. خطأ في قاعدة البيانات
```
❌ Database connection failed
```
**الحل:** تأكد من تشغيل PostgreSQL وتشغيل الهجرات
```bash
alembic upgrade head
```

#### 3. خطأ في المصادقة
```
❌ 401 Unauthorized
```
**الحل:** تأكد من صحة بيانات تسجيل الدخول

#### 4. خطأ في الصلاحيات
```
❌ 403 Forbidden
```
**الحل:** تأكد من أن المستخدم لديه صلاحيات المدير

## 📝 إضافة اختبارات جديدة

### هيكل الاختبار الجديد
```python
def test_new_feature():
    """اختبار الميزة الجديدة"""
    # إعداد البيانات
    payload = {
        "key": "value"
    }
    
    # إجراء الطلب
    r = requests.post(f"{BASE_URL}/new-endpoint", json=payload)
    assert_status(r, 200)
    
    # التحقق من النتيجة
    data = r.json()
    assert data["expected_field"] == "expected_value"
```

### إضافة الاختبار للقائمة
```python
tests = [
    # ... الاختبارات الموجودة
    ("الميزة الجديدة", test_new_feature),
]
```

## 🎯 أفضل الممارسات

### 1. ترتيب الاختبارات
- ابدأ بالاختبارات الأساسية (قاعدة البيانات، المصادقة)
- ثم اختبارات الميزات الأساسية
- وأخيراً اختبارات الأداء والأمان

### 2. تنظيف البيانات
- استخدم بيانات اختبار منفصلة
- نظف البيانات بعد كل اختبار
- تجنب التأثير على البيانات الإنتاجية

### 3. معالجة الأخطاء
- استخدم `try-except` لمعالجة الأخطاء
- اطبع رسائل واضحة للأخطاء
- سجل الأخطاء للتحليل

### 4. الأداء
- اختبر الأداء تحت الحمل
- قم بقياس وقت الاستجابة
- اختبر الطلبات المتزامنة

## 📞 الدعم

إذا واجهت أي مشاكل في الاختبارات:

1. تحقق من تشغيل الخادم وقاعدة البيانات
2. راجع رسائل الخطأ بعناية
3. تأكد من صحة إعدادات الاتصال
4. تحقق من صلاحيات المستخدمين

## 🎉 الخلاصة

هذه الاختبارات الشاملة تضمن:
- ✅ جودة عالية للكود
- ✅ استقرار النظام
- ✅ أمان البيانات
- ✅ أداء ممتاز
- ✅ تجربة مستخدم سلسة

**تشغيل الاختبارات بانتظام يساعد في اكتشاف المشاكل مبكراً والحفاظ على جودة النظام!** 🚀 