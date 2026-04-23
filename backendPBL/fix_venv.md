# حل مشكلة venv - المسار الخاطئ

## 🔴 المشكلة
venv يشير إلى مسار خاطئ من جهاز آخر (LENOVO).

## ✅ الحل: إعادة إنشاء venv

### الطريقة 1: إعادة إنشاء venv (الأفضل)

#### الخطوة 1: إيقاف venv الحالي
```powershell
deactivate
```

#### الخطوة 2: حذف venv القديم
```powershell
# ارجع للمجلد الرئيسي
cd ..

# احذف venv القديم
Remove-Item -Recurse -Force venv
```

#### الخطوة 3: إنشاء venv جديد
```powershell
python -m venv venv
```

#### الخطوة 4: تفعيل venv الجديد
```powershell
.\venv\Scripts\Activate.ps1
```

#### الخطوة 5: ترقية pip
```powershell
python -m pip install --upgrade pip
```

#### الخطوة 6: تثبيت الحزم
```powershell
cd projectBPL
pip install -r requirements.txt
```

---

### الطريقة 2: استخدام python -m pip مباشرة (سريع)

بدلاً من `pip install`، استخدم:

```powershell
python -m pip install -r requirements.txt
```

---

### الطريقة 3: إصلاح venv الموجود

#### الخطوة 1: إيقاف venv
```powershell
deactivate
```

#### الخطوة 2: حذف venv وإعادة إنشائه
```powershell
# من المجلد الرئيسي
cd ..
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### الخطوة 3: تثبيت الحزم
```powershell
cd projectBPL
python -m pip install -r requirements.txt
```

---

## 🎯 الحل السريع (أنصح به)

افتح PowerShell في المجلد الرئيسي واكتب:

```powershell
# 1. إيقاف venv إذا كان مفعلاً
deactivate

# 2. حذف venv القديم
Remove-Item -Recurse -Force venv

# 3. إنشاء venv جديد
python -m venv venv

# 4. تفعيل venv
.\venv\Scripts\Activate.ps1

# 5. ترقية pip
python -m pip install --upgrade pip

# 6. الانتقال لمجلد المشروع
cd projectBPL

# 7. تثبيت الحزم
python -m pip install -r requirements.txt
```

---

## ✅ التحقق من الحل

بعد التثبيت، تحقق:

```powershell
pip list
```

يجب أن ترى:
- Django
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers

---

## 📝 ملاحظات

1. **لماذا حدثت المشكلة؟**
   - venv تم إنشاؤه على جهاز آخر (LENOVO)
   - أو تم نسخ المشروع من مكان آخر
   - venv يحتوي على مسارات مطلقة

2. **لماذا الحل يعمل؟**
   - إنشاء venv جديد يربطه بالمسار الصحيح
   - python -m pip يستخدم Python المثبت مباشرة

3. **نصيحة:**
   - لا تنسخ venv بين الأجهزة
   - أنشئ venv جديد في كل مشروع
