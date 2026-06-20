# Design System Reference
## چک‌بازار — پلتفرم تنزیل چک

> **دستورالعمل استفاده:**
> این سند را در ابتدای هر مکالمه‌ای که خروجی UI/UX یا HTML تولید می‌کند ضمیمه کنید و از Claude بخواهید «کاملاً مطابق این Design System عمل کند». هیچ رنگ، فونت، یا تصمیم طراحی خارج از این سند نباید اعمال شود مگر با تأیید صریح.

---

## ۱. CSS Variables (کد آماده — کپی مستقیم)

```css
:root {
  /* Brand — Navy */
  --navy:       #0C2340;
  --navy-mid:   #1A3D6B;
  --navy-light: #2A5FA8;

  /* Accent — Amber Gold */
  --gold:       #C9960A;
  --gold-light: #EAC84A;
  --gold-pale:  #FDF5DC;

  /* Semantic — Teal (success / low-risk) */
  --teal:       #0D7A72;
  --teal-light: #E6F4F3;

  /* Semantic — Orange (warning / mid-risk) */
  --orange:       #D4730A;
  --orange-light: #FEF3E6;

  /* Semantic — Red (danger / high-risk) */
  --red:       #C0392B;
  --red-light: #FDECEA;

  /* Neutrals */
  --bg:       #F5F4F0;   /* warm paper — page background */
  --surface:  #FFFFFF;   /* cards, modals, panels */
  --surface2: #F8F7F3;   /* secondary surface, form summaries */
  --border:   #E0DDD5;   /* default borders */
  --border2:  #C8C4BA;   /* hover / emphasis borders */

  /* Typography */
  --text1: #1A1613;   /* headings, primary values */
  --text2: #4A4540;   /* labels, descriptions */
  --text3: #7A7570;   /* hints, metadata, keys */

  /* Radii */
  --radius-sm: 6px;
  --radius:    10px;
  --radius-lg: 14px;

  /* Shadows */
  --shadow:    0 1px 3px rgba(12,35,64,.08), 0 4px 12px rgba(12,35,64,.05);
  --shadow-lg: 0 4px 16px rgba(12,35,64,.12), 0 12px 40px rgba(12,35,64,.08);
}
```

---

## ۲. پالت رنگ — جدول کامل

| متغیر | Hex | کاربرد |
|---|---|---|
| `--navy` | `#0C2340` | ناوبار، هدر کارت، دکمه اصلی، آواتار |
| `--navy-mid` | `#1A3D6B` | hover دکمه اصلی، گرادیان Hero |
| `--navy-light` | `#2A5FA8` | focus ring، border hover |
| `--gold` | `#C9960A` | دکمه CTA، آیکون لوگو |
| `--gold-light` | `#EAC84A` | متن روی پس‌زمینه نیلی |
| `--gold-pale` | `#FDF5DC` | پس‌زمینه اطلاعیه‌های اطلاعاتی |
| `--teal` | `#0D7A72` | نرخ تنزیل، ابراز تمایل، موفقیت، کم‌ریسک |
| `--teal-light` | `#E6F4F3` | پس‌زمینه badge موفقیت، CTA ثانوی |
| `--orange` | `#D4730A` | ریسک متوسط، وضعیت در انتظار |
| `--orange-light` | `#FEF3E6` | پس‌زمینه badge ریسک متوسط |
| `--red` | `#C0392B` | ریسک بالا، خطا |
| `--red-light` | `#FDECEA` | پس‌زمینه badge پرریسک |
| `--bg` | `#F5F4F0` | پس‌زمینه کل صفحه (warm paper) |
| `--surface` | `#FFFFFF` | کارت‌ها، Modal، پنل فیلتر |
| `--surface2` | `#F8F7F3` | مبلغ چک در کارت، خلاصه فرم |
| `--border` | `#E0DDD5` | بوردر پیش‌فرض |
| `--border2` | `#C8C4BA` | بوردر در hover |
| `--text1` | `#1A1613` | متن اصلی، عنوان‌ها |
| `--text2` | `#4A4540` | توضیحات، برچسب‌ها |
| `--text3` | `#7A7570` | راهنما، متا‌داده، کلید جدول |

### نقشه معنایی رنگ‌ها

| موقعیت | رنگ | متغیر |
|---|---|---|
| ناوبار / هدر کارت | نیلی عمیق | `--navy` |
| دکمه CTA اصلی | کهربا | `--gold` |
| نرخ تنزیل / موفقیت | فیروزه‌ای | `--teal` |
| ریسک کم (badge) | `#0D4F2A` پس‌زمینه / `#7FFAB0` متن | hardcoded |
| ریسک متوسط (badge) | `#5C3700` پس‌زمینه / `#FFBE68` متن | hardcoded |
| ریسک بالا (badge) | `#4D1500` پس‌زمینه / `#FFB0A0` متن | hardcoded |
| پس‌زمینه صفحه | کاغذ گرم | `--bg` |
| پس‌زمینه کارت | سفید | `--surface` |

---

## ۳. تایپوگرافی

### فونت
```
font-family: 'Vazirmatn', sans-serif;
```
فقط از Google Fonts لود می‌شود:
```html
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### مقیاس اندازه و وزن

| نقش | اندازه | وزن | رنگ |
|---|---|---|---|
| عنوان Hero | `2.8rem` | `700` | `#FFFFFF` |
| عنوان صفحه | `1.5rem` | `700` | `--navy` |
| عنوان بخش | `1.1rem–1.3rem` | `600–700` | `--navy` |
| مبلغ چک در کارت | `1.65rem` | `700` | `--navy` |
| مبلغ چک در Modal | `2.25rem` | `700` | `--gold-light` |
| نرخ تنزیل | `1.15rem` | `700` | `--teal` |
| متن بدنه | `15px` | `400` | `--text1` |
| برچسب فرم | `0.85rem` | `500` | `--text2` |
| متا‌داده / کلید | `0.7–0.75rem` | `400` | `--text3` |
| badge / pill | `0.7–0.72rem` | `600` | بستگی به نوع |
| section title (uppercase) | `0.75rem` | `600` | `--text3` |

### قانون متن روی پس‌زمینه رنگی
- روی `--navy`: از `#FFFFFF` یا `--gold-light` یا `rgba(255,255,255,.75)` استفاده کن.
- روی رنگ‌های badge: از رنگ‌های hardcoded جدول ریسک استفاده کن، نه black.
- هرگز از `--text1` مستقیم روی پس‌زمینه رنگی استفاده نکن.

---

## ۴. فاصله‌گذاری و Border Radius

| متغیر | مقدار | کاربرد |
|---|---|---|
| `--radius-sm` | `6px` | دکمه‌های کوچک، badge، input |
| `--radius` | `10px` | کارت‌های داخلی، Modal CTA |
| `--radius-lg` | `14px` | کارت اصلی listing، Modal، پنل فیلتر |

### padding استاندارد
- کارت listing: `1.1rem`
- پنل فیلتر: `1.25rem`
- Modal body: `1.5rem`
- ناوبار: `0 2rem` (height: `60px`)
- فرم: `1.75rem`
- داشبورد wrap: `2rem 1.5rem`

---

## ۵. کامپوننت‌های کلیدی

### دکمه اصلی (Primary Button)
```css
background: var(--navy);
color: #fff;
padding: .6rem 1.75rem;
border-radius: var(--radius-sm);
font-size: .9rem;
font-weight: 600;
/* hover: */ background: var(--navy-mid);
```

### دکمه CTA طلایی (Gold Button)
```css
background: var(--gold);
color: #1A1200;
padding: .45rem 1.25rem;
border-radius: var(--radius-sm);
font-size: .875rem;
font-weight: 600;
/* hover: */ background: var(--gold-light);
```

### دکمه Ghost (ناوبار)
```css
background: transparent;
border: 1px solid rgba(255,255,255,.3);
color: #fff;
/* hover: */ background: rgba(255,255,255,.1);
```

### کارت آگهی (Listing Card)
```css
background: var(--surface);
border: 1px solid var(--border);
border-radius: var(--radius-lg);
/* hover: */
border-color: var(--navy-light);
box-shadow: var(--shadow-lg);
transform: translateY(-2px);
```

**هدر کارت:**
```css
background: var(--navy);
/* خط دکوراتیو در پایین هدر — الگوی چک: */
background: repeating-linear-gradient(90deg,
  rgba(201,150,10,.4) 0, rgba(201,150,10,.4) 12px,
  transparent 12px, transparent 18px);
height: 2px;
```

**مبلغ چک:**
```css
border: 1px solid var(--border);
border-radius: var(--radius-sm);
background: var(--surface2);
font-size: 1.65rem;
font-weight: 700;
color: var(--navy);
```

### Status Pills

```css
/* منتشرشده */ background:#E6F4F3; color:#0A4E49;
/* در انتظار */ background:#FEF3E6; color:#7A4000;
/* تطابق‌یافته */ background:#EEF0FE; color:#3D34A0;
/* در بررسی */  background:#F5F4F0; color:#4A4540;
font-size: .72rem; font-weight: 600;
padding: .25rem .65rem; border-radius: 100px;
```

### Risk Badges

```css
/* کم‌ریسک */   background:#0D4F2A; color:#7FFAB0;
/* ریسک متوسط */ background:#5C3700; color:#FFBE68;
/* پرریسک */    background:#4D1500; color:#FFB0A0;
font-size: .7rem; font-weight: 600;
padding: .2rem .6rem; border-radius: var(--radius-sm);
```

### Section Title (Uppercase Label)
```css
font-size: .75rem;
font-weight: 600;
color: var(--text3);
text-transform: uppercase;
letter-spacing: .08em;
padding-bottom: .5rem;
border-bottom: 1px solid var(--border);
```

---

## ۶. جهت و زبان

```html
<html lang="fa" dir="rtl">
```

- **همه‌ی متن‌های رابط کاربری فارسی** هستند.
- اعداد به فارسی نمایش داده می‌شوند (۱٬۲۰۰٬۰۰۰ نه 1,200,000).
- تاریخ‌ها به شمسی هستند (مثل ۱۴۰۴/۰۳/۲۰).
- `line-height: 1.7` برای خوانایی فارسی.

---

## ۷. Grid و Layout

| Layout | ساختار |
|---|---|
| بازارچه | `grid-template-columns: 240px 1fr` |
| listing grid | `grid-template-columns: repeat(2, 1fr)` |
| modal grid | `grid-template-columns: repeat(3, 1fr)` |
| داشبورد stats | `grid-template-columns: repeat(4, 1fr)` |
| فرم دو‌ستونه | `grid-template-columns: 1fr 1fr` |

**Responsive breakpoint: `max-width: 768px`**
- بازارچه: یک‌ستونه
- listing grid: یک‌ستونه
- داشبورد stats: دو‌ستونه
- modal grid: دو‌ستونه

---

## ۸. ساختار صفحات (Page Map)

| صفحه | ID | محتوا |
|---|---|---|
| خانه | `page-landing` | Hero + Stats + How It Works |
| بازارچه | `page-marketplace` | فیلتر + grid آگهی‌ها |
| ثبت آگهی | `page-create` | فرم ۳ مرحله‌ای |
| داشبورد | `page-dashboard` | تب‌های دارنده/سرمایه‌گذار/فعالیت |

SPA با `showPage(name)` و `display:none/block`.

---

## ۹. اصول طراحی (نقضشان مجاز نیست)

1. **هرگز** از رنگ آبی سرد یا خاکستری سرد به‌عنوان رنگ اصلی استفاده نکن — این پروژه عمداً از فین‌تک‌های رایج فاصله می‌گیرد.
2. **هرگز** `--text1` را مستقیم روی پس‌زمینه رنگی (navy، gold، teal) قرار نده.
3. **هرگز** بوردر ریدیوس را از `--radius-lg` (14px) بیشتر نبر — این UI مستطیل‌محور است نه دایره‌محور.
4. **همیشه** هدر کارت listing را با `--navy` رنگ بزن — شناسه بصری اصلی پلتفرم است.
5. **همیشه** مبلغ چک را در `--surface2` با بوردر نشان بده — این عنصر امضای بصری پلتفرم است.
6. **همیشه** فارسی و RTL. هیچ متن رابط کاربری انگلیسی در UI نهایی مجاز نیست.
7. **همیشه** disclaimer "بازارچه اطلاعاتی" در صفحات مالی حاضر باشد.

---

## ۱۰. دستورالعمل Prompt

هر بار که بخش جدیدی از UI می‌سازید، این دستور را به Claude بدهید:

```
این فایل Design System پروژه چک‌بازار است.
تمام خروجی HTML/CSS باید:
- دقیقاً از CSS Variables این سند استفاده کند (هیچ رنگ hardcode جدیدی مجاز نیست)
- از فونت Vazirmatn و RTL استفاده کند
- از همان Border Radius ها و spacing های تعریف‌شده پیروی کند
- هدر کارت‌های listing را با --navy رنگ بزند
- مبلغ چک را در کادر --surface2 نمایش دهد
- badge ریسک را با رنگ‌های تعریف‌شده در بخش Risk Badges نشان دهد
هیچ تصمیم طراحی خارج از این سند بدون تأیید صریح مجاز نیست.
```
