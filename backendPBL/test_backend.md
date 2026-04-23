# طرق اختبار الباك إند

## 🔍 طريقة سريعة للتحقق

### 1. فتح المتصفح
اذهب إلى: `http://localhost:8000`

**إذا رأيت:**
- صفحة Django الافتراضية ✅
- أو رسالة 404 ✅
- أو صفحة خطأ ✅

**كل هذا يعني أن الباك إند يعمل!**

---

### 2. اختبار API مباشرة

#### أ) اختبار endpoint بدون مصادقة:
افتح في المتصفح:
```
http://localhost:8000/api/account/register/learner/
```

**النتيجة المتوقعة:**
- إذا رأيت صفحة API أو رسالة خطأ JSON → الباك إند يعمل ✅
- إذا رأيت "This site can't be reached" → الباك إند لا يعمل ❌

#### ب) اختبار endpoint مع مصادقة:
افتح في المتصفح:
```
http://localhost:8000/api/courses/
```

**النتيجة المتوقعة:**
- رسالة خطأ 401 (Unauthorized) → الباك إند يعمل ✅
- رسالة خطأ 404 → تحقق من المسار
- "This site can't be reached" → الباك إند لا يعمل ❌

---

### 3. استخدام PowerShell (curl)

افتح PowerShell واكتب:

```powershell
curl http://localhost:8000/api/courses/
```

**النتيجة المتوقعة:**
- JSON response أو رسالة خطأ → الباك إند يعمل ✅
- "Could not resolve host" → الباك إند لا يعمل ❌

---

### 4. اختبار Admin Panel

افتح في المتصفح:
```
http://localhost:8000/admin/
```

**النتيجة المتوقعة:**
- صفحة تسجيل دخول Django Admin → الباك إند يعمل ✅
- "This site can't be reached" → الباك إند لا يعمل ❌

---

## ✅ علامات أن الباك إند يعمل بشكل صحيح

1. ✅ Terminal يظهر: `Starting development server at http://127.0.0.1:8000/`
2. ✅ لا توجد أخطاء حمراء في Terminal
3. ✅ المتصفح على `http://localhost:8000` يعطي response
4. ✅ API endpoints تعطي responses (حتى لو كانت أخطاء)

---

## ❌ علامات أن الباك إند لا يعمل

1. ❌ Terminal يظهر أخطاء حمراء
2. ❌ "This site can't be reached" في المتصفح
3. ❌ Port 8000 غير متاح
4. ❌ أخطاء في قاعدة البيانات

---

## 🔧 حل المشاكل

### إذا كان Port 8000 مستخدم:
```powershell
python manage.py runserver 8001
```

### إذا كانت هناك أخطاء في قاعدة البيانات:
```powershell
python manage.py migrate
```

### إذا كانت هناك أخطاء في الحزم:
```powershell
pip install -r requirements.txt
```

---

## 📝 ملاحظة مهمة

**حتى لو رأيت رسالة خطأ 401 أو 404، هذا يعني أن الباك إند يعمل!**

- 401 = غير مصرح (الباك إند يعمل لكن يحتاج تسجيل دخول)
- 404 = الصفحة غير موجودة (الباك إند يعمل لكن المسار خاطئ)
- "This site can't be reached" = الباك إند لا يعمل
