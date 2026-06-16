---
id: backend-architecture-django-architecture
kind: architecture
domain: backend
---

# Architecture Blueprint: Django Architecture

---
title: Django Architecture
summary: Django Architecture — App-based structure، View/Service/Serializer، business logic placement
domain: backend
category: architecture
applies_to:
  - "backend/**/views.py"
  - "backend/**/serializers.py"
  - "backend/**/urls.py"
priority: 50
kind: architecture
---

# Django Architecture Rules

## ساختار پروژه Django

```
backend/                            # ریشه بک‌اند (Django)
│
├── config/                         # تنظیمات مرکزی پروژه
│   ├── __init__.py
│   ├── settings/                   # تنظیمات محیطی ماژول‌بندی‌شده
│   │   ├── __init__.py
│   │   ├── base.py                 # تنظیمات پایه مشترک بین همه محیط‌ها
│   │   ├── local.py                # تنظیمات محیط توسعه
│   │   ├── production.py           # تنظیمات محیط تولید
│   │   └── test.py                 # تنظیمات محیط تست
│   ├── urls.py                     # مسیریابی اصلی URL
│   ├── api_router.py               # مسیریابی API با DefaultRouter / SimpleRouter
│   └── wsgi.py                     # نقطه ورود WSGI
│
├── doion/                          # دایرکتوری اپلیکیشن‌ها (APPS_DIR)
│   ├── __init__.py
│   ├── conftest.py                 # تنظیمات تست پایه
│   │
│   ├── users/                      # اپ مدیریت کاربران
│   │   ├── __init__.py
│   │   ├── models.py               # مدل User سفارشی مبتنی بر AbstractUser
│   │   ├── views.py                # ویوهای کاربر Detail، Update و Redirect
│   │   ├── urls.py                 # URLهای مربوط به کاربران
│   │   ├── admin.py                # تنظیمات پنل ادمین
│   │   ├── forms.py                # فرم‌های ثبت‌نام و احراز هویت
│   │   ├── adapters.py             # آداپتورهای django-allauth
│   │   ├── apps.py                 # تنظیمات اپ
│   │   ├── context_processors.py   # پردازشگرهای زمینه
│   │   ├── api/                    # لایه REST API برای کاربران
│   │   │   ├── __init__.py
│   │   │   ├── views.py            # UserViewSet برای Retrieve، List، Update و Me
│   │   │   └── serializers.py      # UserSerializer
│   │   └── migrations/             # مایگریشن‌های دیتابیس
│   │       ├── __init__.py
│   │       └── 0001_initial.py
│   │
│   ├── contrib/                    # کدهای کمکی
│   │   └── sites/                  # اپ sites جنگو
│   │       └── migrations/
│   │           ├── 0001_initial.py
│   │           ├── 0002_alter_domain_unique.py
│   │           ├── 0003_set_site_domain_and_name.py
│   │           └── 0004_alter_options_ordering_domain.py
│   │
│   ├── static/                     # فایل‌های استاتیک
│   │   ├── css/
│   │   │   └── project.css
│   │   ├── fonts/
│   │   │   └── .gitkeep
│   │   ├── images/
│   │   │   └── favicons/
│   │   │       └── favicon.ico
│   │   └── js/
│   │       └── project.js
│   │
│   └── templates/                  # قالب‌های HTML
│       ├── base.html               # قالب پایه سایت
│       ├── 403.html
│       ├── 403_csrf.html
│       ├── 404.html
│       ├── 500.html
│       ├── pages/
│       │   ├── home.html
│       │   └── about.html
│       ├── account/
│       │   └── base_manage_password.html
│       ├── allauth/
│       │   ├── elements/
│       │   └── layouts/
│       └── users/
│           ├── user_detail.html
│           └── user_form.html
│
├── .env
├── .editorconfig
├── .gitignore
├── .gitattributes
├── manage.py
├── pyproject.toml
└── uv.lock
```

## Business Logic Placement

* View فقط orchestration
* Service برای business logic
* Serializer فقط validation و serialization
* Circular dependency ممنوع

❌ نادرست (در View):

```python
class OrderViewSet(ModelViewSet):
    def create(self, request):
        if request.user.profile.balance < 0:
            raise ValidationError("No balance")
```

✅ درست (Service):

```python
class CreateOrderService:
    def execute(self, user, validated_data):
        if user.profile.balance < 0:
            raise DomainError("No balance")
        return Order.objects.create(**validated_data, user=user)
```

## ViewSet Only

❌ نادرست:

```python
class CreateOrder(APIView):
    def post(self, request): ...
```

✅ درست:

```python
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]
```

## Serializer Is the Contract

❌ نادرست:

```python
# validation در view
if "email" not in request.data:
    raise ValidationError("Email required")
```

✅ درست:

```python
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["id", "email", "name"]
```

## No Fat Serializers

❌ نادرست:

```python
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        charge_user()
        send_notification()
        return Order.objects.create(**validated_data)
```

✅ درست:

```python
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CreateOrderService().execute(
            user=self.context["request"].user,
            validated_data=validated_data,
        )
```

