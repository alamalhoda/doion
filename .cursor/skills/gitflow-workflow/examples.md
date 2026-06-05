# مثال‌های عملی GitFlow

## سناریو ۱: شروع یک Feature جدید

ابتدا وضعیت فعلی را ببین، بعد از `develop` یک branch جدید بساز:

```bash
git status
git branch --show-current
git checkout develop
git pull origin develop
git checkout -b feature/add-service-history develop
```

## سناریو ۲: همگام‌سازی branch قبل از PR

قبل از PR، branch را با `origin/develop` sync کن:

```bash
git checkout feature/add-service-history
git fetch origin
git merge origin/develop
```

## سناریو ۳: جریان Rebase با Push امن

اگر rebase انجام دادی، push امن فقط با `--force-with-lease`:

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
