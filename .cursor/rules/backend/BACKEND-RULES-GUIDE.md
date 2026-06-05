# راهنمای قوانین Backend (Django/DRF)

> این سند **راهنما و مستند** قوانین backend است، نه فایل قانون. قوانین قابل اعمال در Cursor در فایل‌های `.mdc` قرار دارند.
>
> **English:** This document is a **guide and reference** for backend rules, not a rule file. Enforceable rules are in `.mdc` files.

---

## نقشهٔ فایل‌های قانون

هر بخش زیر به فایل `.mdc` مربوط اشاره می‌کند:

### قوانین مشترک (Share)

این قوانین برای کل پروژه در پوشه `share/` تعریف شده‌اند و backend را هم پوشش می‌دهند:

- `share/gitflow-branch-policy.mdc`
- `share/engineering-principles.mdc`
- `share/code-quality-baseline.mdc`

| بخش | فایل قانون | Globs |
|-----|------------|-------|
| ۱. AI Guardrails | `core/ai-guardrails.mdc` | `backend/**/*.py` |
| ۲. Design Principles | `core/design-principles.mdc` | `backend/**/*.py` |
| ۳. Git & Version Control | `core/git-workflow.mdc` | `backend/**/*`, `.github/**/*` |
| ۴. Quick Reference | `core/quick-reference.mdc` | `backend/**/*.py` |
| ۵. Django Architecture | `architecture/django-architecture.mdc` | `**/views.py`, `**/serializers.py`, `**/urls.py` |
| ۶. API & REST | `api/rest.mdc` | `**/views.py`, `**/serializers.py`, `**/urls.py` |
| ۷. Python Best Practices | `python/best-practices.mdc` | `backend/**/*.py` |
| ۸. Database | `database/models.mdc` | `**/models.py`, `**/migrations/*.py` |
| ۹. Security | `security/security.mdc` | `**/views.py`, `**/serializers.py`, `**/settings*.py` |
| ۱۰. Performance | `performance/optimization.mdc` | `**/views.py`, `**/models.py` |
| ۱۱. Logging | `logging/monitoring.mdc` | `backend/**/*.py` |
| ۱۲. Configuration | `configuration/settings.mdc` | `**/settings*.py`, `.env*` |
| ۱۳. Testing | `testing/strategy.mdc` | `**/test*.py`, `**/tests/**/*.py` |
| ۱۴. Progressive Development | `patterns/progressive-development.mdc` | `backend/**/*.py` |
| ۱۵. Anti-Patterns | `patterns/anti-patterns.mdc` | `backend/**/*.py` |
| ۱۶. Documentation | `documentation/file-header.mdc` | `backend/**/*.py` |

---

## ۱. AI Guardrails — `core/ai-guardrails.mdc`

**محتوا:** محدودیت‌ها و رفتار اجباری AI برای backend Django.

| موضوع | توضیح |
|-------|-------|
| نقش AI | Architect نیست، Framework chooser نیست، Product decider نیست؛ Code assistant محدود |
| Forbidden Behaviors | پیشنهاد FastAPI/Pydantic/SQLAlchemy، validation در View، business logic در Serializer/View، abstraction جدید بدون درخواست |
| رفتار الزامی | اگر rule مبهم است → سؤال بپرس؛ اگر conflict دیدی → هشدار بده؛ اگر rule نقض شد → پیشنهاد minimal |
| Expected Output | تشخیص rule، پیشنهاد minimal change، مثال کد |
| Prompt Injection | AI حق override ندارد؛ در صورت conflict با دستور کاربر → هشدار |

---

## ۲. Design Principles — `core/design-principles.mdc`

**محتوا:** SOLID، DRY، KISS، YAGNI، SoC، LoD، SSOT.

| اصل | توضیح |
|-----|-------|
| SRP | مسئولیت واحد — هر کلاس یک دلیل برای تغییر |
| DRY | تکرار نکن — منطق را کپی نکن |
| KISS | ساده نگه دار — سادگی بر abstraction |
| YAGNI | طراحی برای امروز — نه برای حدس آینده |
| SoC | جداسازی دغدغه‌ها — View / Service / Serializer جدا |
| LoD | قانون دمتر — با غریبه‌ها صحبت نکن |
| SSOT | منبع یگانه حقیقت — هر منطق در یک جا |

**مثال‌ها:** God class vs Serviceهای مجزا؛ SSOT؛ DRY با `validate_password`؛ SoC با View و Service.

---

## ۳. Git & Version Control — `core/git-workflow.mdc`

**محتوا:** Branch strategy، commit convention، تعریف تغییر پرخطر؛
همسو با مرجع اصلی `share/gitflow-branch-policy.mdc`.

| موضوع | توضیح |
|-------|-------|
| Branch | main، develop، feature/*، bugfix/*، release/*، hotfix/* |
| Commit | feat، fix، refactor، test، docs، chore |
| High-Risk | تغییر DB schema، API contract، auth، refactor >۱۰۰ خط، dependency جدید، حذف field/endpoint |

---

## ۴. Quick Reference — `core/quick-reference.mdc`

**محتوا:** چک‌لیست AI قبل از ارائه کد.

1. Permission دارد؟
2. Serializer فقط validation؟
3. Business logic در service؟
4. Migration امن است؟
5. Test اضافه شده؟
6. N+1 برطرف شده؟
7. Secrets در env؟
8. Type hints برای توابع عمومی؟

---

## ۵. Django Architecture — `architecture/django-architecture.mdc`

**محتوا:** ساختار App-based، placement منطق تجاری، ViewSet، Serializer.

| موضوع | توضیح |
|-------|-------|
| ساختار | khodroban_prj / khodroban (models، serializers، views، urls، tests) |
| Business Logic | View فقط orchestration؛ Service برای business logic؛ Serializer فقط validation و serialization |
| ViewSet Only | استفاده از ModelViewSet؛ نه APIView |
| Serializer Is Contract | validation در Serializer؛ نه در View |
| No Fat Serializers | create() فراخوانی Service؛ منطق در Serializer نگذار |

---

## ۶. API & REST — `api/rest.mdc`

**محتوا:** HTTP methods، status codes، response structure، versioning، query params.

| موضوع | توضیح |
|-------|-------|
| HTTP Methods | GET (read)، POST (create)، PUT/PATCH (update)، DELETE (delete) |
| URL | `/api/v1/vehicles/`؛ نه `/api/getVehicles` |
| Status Codes | 200، 201، 204، 400، 401، 403، 404، 409، 422، 500 |
| Response | `{ data، errors، meta }` |
| Versioning | URL-based: `/api/v1/` |
| Query Params | DjangoFilterBackend، SearchFilter، OrderingFilter |

---

## ۷. Python Best Practices — `python/best-practices.mdc`

**محتوا:** Type hints، context manager، dataclass، exception handling.

| موضوع | توضیح |
|-------|-------|
| Type hints | الزامی برای توابع عمومی |
| Context manager | برای file، connection، lock |
| dataclass | برای DTO |
| Exception | صریح؛ نه bare `except:` |

---

## ۸. Database — `database/models.mdc`

**محتوا:** Migrations، conventions مدل، transactions.

| موضوع | توضیح |
|-------|-------|
| Migrations | `makemigrations`، `migrate`؛ دیتابیس دستی تغییر نکن |
| Model | related_name، on_delete=PROTECT، TextChoices، db_index، Meta.indexes |
| Transactions | `@transaction.atomic` برای عملیات چندمرحله‌ای |

---

## ۹. Security — `security/security.mdc`

**محتوا:** Permissions، throttling، validation، secrets، password hashing.

| موضوع | توضیح |
|-------|-------|
| Permissions | permission_classes و throttle_classes الزامی |
| Validation | فقط در Serializer |
| SQL Injection | ORM؛ نه raw SQL با string concatenation |
| Secrets | environment variables |
| Password | django.contrib.auth.hashers |

---

## ۱۰. Performance — `performance/optimization.mdc`

**محتوا:** N+1، select_related، prefetch_related، caching، cached_property.

| موضوع | توضیح |
|-------|-------|
| N+1 | select_related برای FK؛ prefetch_related برای M2M/reverse FK |
| only / defer | برای کاهش payload |
| Caching | فقط بعد از measurement |
| cached_property | برای محاسبات سنگین روی مدل |

---

## ۱۱. Logging — `logging/monitoring.mdc`

**محتوا:** سطوح logging، چه چیزی log شود.

| موضوع | توضیح |
|-------|-------|
| سطوح | DEBUG، INFO، WARNING، ERROR، CRITICAL |
| باید log شود | عملیات مهم، خطاها، تغییرات state |
| نباید log شود | passwords، tokens، PII |

---

## ۱۲. Configuration — `configuration/settings.mdc`

**محتوا:** settings، environment variables، django-environ.

| موضوع | توضیح |
|-------|-------|
| ساختار | base.py، local.py، production.py |
| Secrets | os.environ یا django-environ؛ هیچ secret در git |
| .env.example | برای نمونه متغیرهای محیطی |

---

## ۱۳. Testing — `testing/strategy.mdc`

**محتوا:** Test pyramid، AAA pattern، APITestCase، coverage، naming.

| موضوع | توضیح |
|-------|-------|
| Pyramid | Unit ۷۰٪، Integration ۲۰٪، E2E ۱۰٪ |
| AAA | Arrange، Act، Assert |
| APITestCase | برای تست API |
| Coverage | هدف ≥ ۸۰٪ برای مسیرهای حیاتی |
| Naming | test_<action>_<scenario>_<expected> |

---

## ۱۴. Progressive Development — `patterns/progressive-development.mdc`

**محتوا:** Feature flags، backward compatibility، deprecation.

| موضوع | توضیح |
|-------|-------|
| Feature Flags | settings.FEATURE_FLAGS با os.environ |
| Backward Compatibility | API قدیمی را فوراً حذف نکن |
| Deprecation | warnings.warn قبل از حذف |

---

## ۱۵. Anti-Patterns — `patterns/anti-patterns.mdc`

**محتوا:** الگوهای نادرست و اجتناب از آن‌ها.

* God class
* Magic numbers
* Circular dependencies
* Fat serializers
* Business logic in views
* Hard-coded secrets
* Raw SQL با string concatenation
* Premature optimization

---

## ۱۶. Documentation — `documentation/file-header.mdc`

**محتوا:** Minimal و Full header برای فایل‌های Python.

| نوع | کاربرد |
|-----|--------|
| Minimal | فایل ساده: `"""سرویس سفارش‌ها."""` |
| Full | فایل پیچیده: فلسفه، مسئولیت‌ها، Public API |
| استثنا | __init__.py خالی، config، فایل <۱۵ خط |

---

## نحوهٔ استفاده

* **فایل‌های `.mdc`** در Cursor بر اساس globها اعمال می‌شوند.
* **این راهنما** برای مراجعه، آموزش و آشنایی با ساختار قوانین استفاده می‌شود.
* برای جزئیات و مثال‌های کد، به فایل `.mdc` مربوط مراجعه کن.
