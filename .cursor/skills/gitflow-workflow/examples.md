# مثال‌های عملی GitFlow

## سناریو ۱: شروع یک Feature جدید (نقطه ۱)

ابتدا وضعیت فعلی را ببین، `develop` را با `--ff-only` آینه کن، بعد branch بساز:

```bash
git status
git branch --show-current
git checkout develop
git fetch origin
git pull --ff-only origin develop
git checkout -b feature/add-service-history develop
```

نام شاخه یک هدف باشد، نه `feature/ali-work`.

## سناریو ۲: همگام‌سازی branch قبل از PR (نقطه ۲)

قبل از PR دوباره با `origin/develop` sync کن (پیش‌فرض merge):

```bash
git checkout feature/add-service-history
git fetch origin
git merge origin/develop
git push
```

## سناریو ۳: جریان Rebase با Push امن

فقط اگر rebase صریح خواسته شد:

```bash
git checkout feature/add-service-history
git fetch origin
git rebase origin/develop
git push --force-with-lease origin feature/add-service-history
```

## سناریو ۴: ادغام feature به develop فقط با PR

مسیر درست ادغام:
- از branch کاری (`feature/*` یا `bugfix/*`) PR بساز
- مقصد PR باید `develop` باشد
- merge مستقیم محلی روی `develop` برای جریان عادی انجام نده

نمونه صحیح:

```bash
git checkout feature/add-service-history
git fetch origin
git merge origin/develop
git push -u origin feature/add-service-history
gh pr create --base develop --head feature/add-service-history --title "feat(service): add service history" --body "## Summary\n- add service history flow"
```

## سناریو ۵: بعد از merge (نقطه ۳)

شاخه را از local بردار و remoteهای مرده را prune کن:

```bash
git checkout develop
git pull --ff-only origin develop
git branch -d feature/add-service-history
git fetch --prune
```

اگر GitHub هنوز `feature/add-service-history` را دارد:

```bash
git push origin --delete feature/add-service-history
```

## سناریو ۶: تگ SemVer (انتشار، نه هر PR)

تگ محصول را روی `feature/*` با `git tag` نزن. از workflow `Release` استفاده کن (Skill `semver-release`):

```bash
gh workflow run Release --ref develop -f version=0.1.0-test.1
```

بعد از merge یک feat/fix به `develop`، اگر کاربر از انتشار حرف زد یک‌بار یادآوری کن.
