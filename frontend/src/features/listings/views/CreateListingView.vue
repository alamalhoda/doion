<template>
  <div class="create-listing">
    <div class="create-header">
      <h1 class="create-title">ثبت آگهی چک</h1>
      <p class="create-subtitle">اطلاعات چک خود را وارد کنید تا سرمایه‌گذاران مناسب پیدا کنند.</p>
    </div>

    <Stepper :steps="steps" :current="currentStep" />

    <div class="form-panel">
      <!-- Step 1: Cheque Info -->
      <div v-if="currentStep === 1">
        <div class="form-grid-2">
          <div class="form-row">
            <label class="form-label">مبلغ اسمی چک <span class="required">*</span></label>
            <input v-model="form.amount" class="form-input" placeholder="مثال: ۵۰۰٬۰۰۰٬۰۰۰" />
            <div class="form-hint">واحد: ریال</div>
          </div>
          <div class="form-row">
            <label class="form-label">تاریخ سررسید <span class="required">*</span></label>
            <input v-model="form.dueDate" class="form-input" placeholder="مثال: ۱۴۰۴/۰۶/۱۵" />
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-row">
            <label class="form-label">نام بانک صادرکننده <span class="required">*</span></label>
            <select v-model="form.bank" class="form-input">
              <option value="">انتخاب بانک</option>
              <option>بانک ملی ایران</option>
              <option>بانک صادرات</option>
              <option>بانک تجارت</option>
              <option>بانک ملت</option>
              <option>بانک پارسیان</option>
              <option>بانک پاسارگاد</option>
              <option>سایر</option>
            </select>
          </div>
          <div class="form-row">
            <label class="form-label">شماره صیاد چک <span class="required">*</span></label>
            <input v-model="form.sayad" class="form-input" placeholder="کد ۱۶ رقمی صیاد" />
            <div class="form-hint">از سامانه صیاد بانک مرکزی</div>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">نوع صادرکننده چک <span class="required">*</span></label>
          <div class="form-radio-group">
            <label class="form-radio">
              <input type="radio" v-model="form.issuerType" value="legal" />
              <span>حقوقی (شرکت)</span>
            </label>
            <label class="form-radio">
              <input type="radio" v-model="form.issuerType" value="natural" />
              <span>حقیقی (شخص)</span>
            </label>
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-row">
            <label class="form-label">نام صادرکننده <span class="required">*</span></label>
            <input v-model="form.issuer" class="form-input" placeholder="نام کامل یا نام شرکت" />
          </div>
          <div class="form-row">
            <label class="form-label">کد ملی / شناسه ملی <span class="required">*</span></label>
            <input v-model="form.nationalId" class="form-input" placeholder="۱۰ رقم" />
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">توضیحات تکمیلی</label>
          <textarea v-model="form.notes" class="form-input form-textarea" rows="3" placeholder="هر اطلاعات اضافی درباره صادرکننده یا دلیل نقد کردن چک..." />
        </div>

        <div class="rate-banner">
          <strong>نرخ تنزیل پیشنهادی:</strong> بر اساس اطلاعات وارد‌شده، سامانه نرخی بین ۳٪ تا ۸٪ پیشنهاد خواهد داد. نرخ نهایی توسط سرمایه‌گذار تعیین می‌شود.
        </div>

        <div class="form-actions">
          <button class="btn btn--primary" @click="goStep(2)">ادامه — بارگذاری مدارک</button>
        </div>
      </div>

      <!-- Step 2: Documents -->
      <div v-if="currentStep === 2">
        <div class="form-row">
          <label class="form-label">تصویر چک <span class="required">*</span></label>
          <div class="upload-area" @click="toast('در نسخه نمونه، بارگذاری فایل فعال نیست')">
            <div class="upload-icon">📄</div>
            <p>تصویر واضح از جلو و پشت چک را بارگذاری کنید</p>
            <p class="upload-hint">فرمت‌های مجاز: JPG، PNG، PDF — حداکثر ۵ مگابایت</p>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">مدارک صادرکننده <span class="required">*</span></label>
          <div class="upload-area" @click="toast('در نسخه نمونه، بارگذاری فایل فعال نیست')">
            <div class="upload-icon">🪪</div>
            <p>تصویر کارت ملی یا شناسه صادرکننده</p>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">مدارک تکمیلی (اختیاری)</label>
          <div class="upload-area" @click="toast('در نسخه نمونه، بارگذاری فایل فعال نیست')">
            <div class="upload-icon">📋</div>
            <p>گواهی امضاء، قرارداد مرتبط، یا سایر مستندات</p>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn btn--secondary" @click="goStep(1)">بازگشت</button>
          <button class="btn btn--primary" @click="goStep(3)">ادامه — تأیید نهایی</button>
        </div>
      </div>

      <!-- Step 3: Review -->
      <div v-if="currentStep === 3">
        <div class="review-box">
          <div class="review-title">خلاصه آگهی شما</div>
          <div class="review-grid">
            <div class="review-item">
              <div class="review-key">مبلغ</div>
              <div class="review-value">۵۰۰٬۰۰۰٬۰۰۰ ریال</div>
            </div>
            <div class="review-item">
              <div class="review-key">سررسید</div>
              <div class="review-value">۱۴۰۴/۰۶/۱۵</div>
            </div>
            <div class="review-item">
              <div class="review-key">بانک</div>
              <div class="review-value">بانک ملت</div>
            </div>
            <div class="review-item">
              <div class="review-key">سطح ریسک</div>
              <div class="review-value review-value--teal">کم ریسک</div>
            </div>
            <div class="review-item">
              <div class="review-key">نرخ تنزیل پیشنهادی</div>
              <div class="review-value review-value--teal">۴.۲٪</div>
            </div>
            <div class="review-item">
              <div class="review-key">وضعیت</div>
              <div class="review-value review-value--orange">در انتظار بررسی</div>
            </div>
          </div>
        </div>

        <div class="info-banner">
          پس از ثبت، آگهی شما توسط تیم بررسی (Moderation) پلتفرم بازبینی می‌شود. در صورت تأیید، در اسرع وقت منتشر خواهد شد.
        </div>

        <div class="form-row">
          <label class="form-checkbox">
            <input type="checkbox" />
            <span>قوانین و مقررات پلتفرم را خوانده‌ام و می‌پذیرم. درک می‌کنم که چک‌بازار صرفاً یک بازارچه اطلاعاتی است و مسئولیت صحت حقوقی معامله با طرفین است.</span>
          </label>
        </div>

        <div class="form-actions">
          <button class="btn btn--secondary" @click="goStep(2)">بازگشت</button>
          <button class="btn btn--primary" @click="submit">ثبت نهایی آگهی</button>
        </div>
      </div>

      <!-- Success -->
      <div v-if="currentStep === 'success'" class="success-box">
        <div class="success-icon">✓</div>
        <h3 class="success-title">آگهی شما با موفقیت ثبت شد!</h3>
        <p class="success-text">آگهی در صف بررسی قرار گرفت. پس از تأیید توسط تیم مدیریت، در بازارچه منتشر می‌شود.</p>
        <div class="success-actions">
          <button class="btn btn--primary" @click="goToDashboard">مشاهده داشبورد</button>
          <button class="btn btn--secondary" @click="goToMarketplace">بازگشت به بازارچه</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentStep = ref(1)

const steps = [
  { index: 1, label: 'اطلاعات چک' },
  { index: 2, label: 'مدارک' },
  { index: 3, label: 'تأیید نهایی' },
]

const form = ref({
  amount: '',
  dueDate: '',
  bank: '',
  sayad: '',
  issuerType: 'natural',
  issuer: '',
  nationalId: '',
  notes: '',
})

const goStep = (step: number) => {
  currentStep.value = step
}

const submit = () => {
  currentStep.value = 'success' as any
}

const goToDashboard = () => navigateTo('/app')
const goToMarketplace = () => navigateTo('/app/listings')

const toast = (msg: string) => {
  console.log('Toast:', msg)
}
</script>

<style>
.create-listing {
  max-width: 680px;
  margin: 0 auto;
}

.create-header {
  margin-bottom: 2rem;
}

.create-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  margin: 0 0 0.3rem;
}

.create-subtitle {
  font-size: var(--font-size-base);
  color: var(--text3);
  margin: 0;
}

/* Form Panel */
.form-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .form-grid-2 {
    grid-template-columns: 1fr;
  }
}

.form-row {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
  margin-bottom: 0.4rem;
}

.required {
  color: var(--red);
}

.form-input {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.6rem 0.85rem;
  font-size: var(--font-size-md);
  color: var(--text1);
  background: var(--surface);
  transition: border-color var(--transition-fast);
}

.form-input:focus {
  outline: none;
  border-color: var(--navy-light);
  box-shadow: 0 0 0 3px rgba(42, 95, 168, 0.08);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-hint {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin-top: 0.3rem;
}

.form-radio-group {
  display: flex;
  gap: 1rem;
  margin-top: 0.4rem;
}

.form-radio {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  font-size: var(--font-size-base);
}

.form-radio input[type='radio'] {
  accent-color: var(--navy);
}

.form-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  cursor: pointer;
  font-size: var(--font-size-base);
  color: var(--text2);
}

.form-checkbox input[type='checkbox'] {
  accent-color: var(--navy);
  margin-top: 3px;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
}

/* Rate Banner */
.rate-banner {
  background: var(--gold-pale);
  border: 1px solid rgba(201, 150, 10, 0.25);
  border-radius: var(--radius-sm);
  padding: 0.85rem 1rem;
  font-size: var(--font-size-sm);
  color: #5c3700;
  margin-bottom: 1rem;
}

/* Upload Area */
.upload-area {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.upload-area:hover {
  border-color: var(--navy-light);
  background: rgba(26, 61, 107, 0.03);
}

.upload-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.upload-area p {
  font-size: var(--font-size-base);
  color: var(--text3);
  margin: 0;
}

.upload-hint {
  font-size: var(--font-size-xs);
  margin-top: 0.3rem;
}

/* Review Box */
.review-box {
  background: var(--surface2);
  border-radius: var(--radius);
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}

.review-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

.review-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.review-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.review-key {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.review-value {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
}

.review-value--teal {
  color: var(--teal);
}

.review-value--orange {
  color: var(--orange);
}

/* Info Banner */
.info-banner {
  background: var(--teal-light);
  border: 1px solid rgba(13, 122, 114, 0.2);
  border-radius: var(--radius-sm);
  padding: 0.85rem 1rem;
  font-size: var(--font-size-sm);
  color: var(--teal);
  margin-bottom: 1.25rem;
}

/* Success Box */
.success-box {
  text-align: center;
  padding: 2.5rem 1rem;
}

.success-icon {
  width: 70px;
  height: 70px;
  background: var(--teal-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
  font-size: 2rem;
  color: var(--teal);
}

.success-title {
  font-size: 1.25rem;
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  margin: 0 0 0.5rem;
}

.success-text {
  font-size: var(--font-size-base);
  color: var(--text3);
  max-width: 380px;
  margin: 0 auto 1.5rem;
}

.success-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}
</style>
