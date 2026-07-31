<template>
  <div class="create-listing">
    <div class="create-header">
      <h1 class="create-title">
        ثبت آگهی چک
      </h1>
      <p class="create-subtitle">
        اطلاعات چک خود را وارد کنید تا سرمایه‌گذاران مناسب پیدا کنند.
      </p>
    </div>

    <Stepper
      :steps="steps"
      :current="currentStep"
    />

    <div class="form-panel">
      <!-- Step 1: Cheque Info -->
      <div v-if="currentStep === 1">
        <div class="form-grid-2">
          <div class="form-row">
            <label class="form-label">مبلغ اسمی چک <span class="required">*</span></label>
            <input
              v-model="form.amount"
              class="form-input"
              placeholder="مثال: ۵۰۰٬۰۰۰٬۰۰۰"
              type="number"
              min="1"
            >
            <div class="form-hint">
              واحد: ریال
            </div>
          </div>
          <div class="form-row">
            <label class="form-label">تاریخ سررسید <span class="required">*</span></label>
            <input
              v-model="form.dueDate"
              class="form-input"
              placeholder="مثال: ۱۴۰۴/۰۶/۱۵"
              type="date"
            >
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-row">
            <label class="form-label">نام بانک صادرکننده <span class="required">*</span></label>
            <select
              v-model="form.bank"
              class="form-input"
            >
              <option value="">
                انتخاب بانک
              </option>
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
            <input
              v-model="form.sayad"
              class="form-input"
              placeholder="کد ۱۶ رقمی صیاد"
              maxlength="16"
            >
            <div class="form-hint">
              از سامانه صیاد بانک مرکزی
            </div>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">نوع صادرکننده چک <span class="required">*</span></label>
          <div class="form-radio-group">
            <label class="form-radio">
              <input
                v-model="form.issuerType"
                type="radio"
                value="legal"
              >
              <span>حقوقی (شرکت)</span>
            </label>
            <label class="form-radio">
              <input
                v-model="form.issuerType"
                type="radio"
                value="natural"
              >
              <span>حقیقی (شخص)</span>
            </label>
          </div>
        </div>

        <div class="form-grid-2">
          <div class="form-row">
            <label class="form-label">نام صادرکننده <span class="required">*</span></label>
            <input
              v-model="form.issuer"
              class="form-input"
              placeholder="نام کامل یا نام شرکت"
            >
          </div>
          <div class="form-row">
            <label class="form-label">کد ملی / شناسه ملی <span class="required">*</span></label>
            <input
              v-model="form.nationalId"
              class="form-input"
              placeholder="۱۰ رقم"
            >
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">توضیحات تکمیلی</label>
          <textarea
            v-model="form.notes"
            class="form-input form-textarea"
            rows="3"
            placeholder="هر اطلاعات اضافی درباره صادرکننده یا دلیل نقد کردن چک..."
          />
        </div>

        <div class="rate-banner">
          <strong>نرخ تنزیل پیشنهادی:</strong> بر اساس اطلاعات وارد‌شده، سامانه نرخی بین ۳٪ تا ۸٪ پیشنهاد خواهد داد. نرخ نهایی توسط سرمایه‌گذار تعیین می‌شود.
        </div>

        <div class="form-actions">
          <button
            class="btn btn--primary"
            :disabled="!isStep1Valid"
            @click="goStep(2)"
          >
            ادامه — بارگذاری مدارک
          </button>
        </div>
      </div>

      <!-- Step 2: Documents -->
      <div v-if="currentStep === 2">
        <div class="form-row">
          <label class="form-label">تصویر چک <span class="required">*</span></label>
          <UploadArea
            accept="image/*,.pdf"
            :max-size="5 * 1024 * 1024"
            label="تصویر واضح از جلو و پشت چک را بارگذاری کنید"
            hint="فرمت‌های مجاز: JPG، PNG، PDF — حداکثر ۵ مگابایت"
            document-type="cheque_image"
            @change="onChequeImageChange"
            @error="onUploadError"
          />
        </div>

        <div class="form-row">
          <label class="form-label">مدارک صادرکننده <span class="required">*</span></label>
          <UploadArea
            accept="image/*,.pdf"
            :max-size="5 * 1024 * 1024"
            label="تصویر کارت ملی یا شناسه صادرکننده"
            document-type="id_document"
            @change="onIdDocChange"
            @error="onUploadError"
          />
        </div>

        <div class="form-row">
          <label class="form-label">مدارک تکمیلی (اختیاری)</label>
          <UploadArea
            accept="image/*,.pdf"
            :max-size="5 * 1024 * 1024"
            label="گواهی امضاء، قرارداد مرتبط، یا سایر مستندات"
            document-type="supplementary"
            @change="onSupplementaryChange"
            @error="onUploadError"
          />
        </div>

        <div class="form-actions">
          <button
            class="btn btn--secondary"
            @click="goStep(1)"
          >
            بازگشت
          </button>
          <button
            class="btn btn--primary"
            :disabled="!hasChequeImage"
            @click="goStep(3)"
          >
            ادامه — تأیید نهایی
          </button>
        </div>
      </div>

      <!-- Step 3: Review -->
      <div v-if="currentStep === 3">
        <ReviewSummary :listing="reviewListing" />

        <div class="info-banner">
          پس از ثبت، آگهی شما توسط تیم بررسی (Moderation) پلتفرم بازبینی می‌شود. در صورت تأیید، در اسرع وقت منتشر خواهد شد.
        </div>

        <div class="form-row">
          <label class="form-checkbox">
            <input
              v-model="acceptedTerms"
              type="checkbox"
            >
            <span>قوانین و مقررات پلتفرم را خوانده‌ام و می‌پذیرم. درک می‌کنم که چک‌بازار صرفاً یک بازارچه اطلاعاتی است و مسئولیت صحت حقوقی معامله با طرفین است.</span>
          </label>
        </div>

        <div
          v-if="error"
          class="error-banner"
        >
          {{ error }}
        </div>

        <div class="form-actions">
          <button
            class="btn btn--secondary"
            :disabled="isSubmitting"
            @click="goStep(2)"
          >
            بازگشت
          </button>
          <button
            class="btn btn--primary"
            :disabled="!acceptedTerms || isSubmitting"
            @click="submit"
          >
            {{ isSubmitting ? 'در حال ثبت...' : 'ثبت نهایی آگهی' }}
          </button>
        </div>
      </div>

      <!-- Success -->
      <div
        v-if="currentStep === 'success'"
        class="success-box"
      >
        <div class="success-icon">
          ✓
        </div>
        <h3 class="success-title">
          آگهی شما با موفقیت ثبت شد!
        </h3>
        <p class="success-text">
          آگهی در صف بررسی قرار گرفت. پس از تأیید توسط تیم مدیریت، در بازارچه منتشر می‌شود.
        </p>
        <div class="success-actions">
          <button
            class="btn btn--primary"
            @click="goToDashboard"
          >
            مشاهده داشبورد
          </button>
          <button
            class="btn btn--secondary"
            @click="goToMarketplace"
          >
            بازگشت به بازارچه
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Stepper from '@/components/Stepper.vue'
import { useToast } from '@/composables'
import { useListingStore } from '../stores/listingStore'
import UploadArea from '../components/UploadArea.vue'
import ReviewSummary from '../components/ReviewSummary.vue'
import type { ChequeListing } from '../types/listing'
import { ListingService } from '../services/listingService'
import { IssuerProfileService } from '../services/issuerProfileService'
import { normalizeApiError } from '@/api/errors'

const router = useRouter()
const { showToast } = useToast()
const listingStore = useListingStore()

const currentStep = ref<number | string>(1)
const isSubmitting = ref(false)
const acceptedTerms = ref(false)

const steps = [
  { index: 1, label: 'اطلاعات چک' },
  { index: 2, label: 'مدارک' },
  { index: 3, label: 'تأیید نهایی' },
]

const form = ref({
  amount: null as number | null,
  dueDate: '',
  bank: '',
  sayad: '',
  issuerType: 'natural' as 'legal' | 'natural',
  issuer: '',
  nationalId: '',
  notes: '',
})

const chequeImageFile = ref<File | null>(null)
const idDocFile = ref<File | null>(null)

const error = computed(() => listingStore.error)

const isStep1Valid = computed(() => {
  return (
    form.value.amount != null &&
    form.value.amount > 0 &&
    form.value.dueDate &&
    form.value.bank &&
    form.value.sayad &&
    form.value.sayad.length === 16 &&
    form.value.issuer &&
    form.value.nationalId
  )
})

const hasChequeImage = computed(() => chequeImageFile.value !== null)

const reviewListing = computed<ChequeListing>(() => ({
  id: 0,
  owner_id: 0,
  bank_name: form.value.bank,
  cheque_serial_number: form.value.sayad,
  face_amount: String(form.value.amount || 0),
  due_date: form.value.dueDate,
  issuer_type: form.value.issuerType,
  issuer_name: form.value.issuer,
  issuer_national_id: form.value.nationalId,
  description: form.value.notes,
  suggested_discount_rate: null,
  risk_tier: null,
  status: 'pending_moderation',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
}))

function goStep(step: number | string) {
  currentStep.value = step
}

function onChequeImageChange(fileList: FileList) {
  chequeImageFile.value = fileList[0]
}

function onIdDocChange(fileList: FileList) {
  idDocFile.value = fileList[0]
}

function onSupplementaryChange(_fileList: FileList) {
}

function onUploadError(message: string) {
  showToast(message, 'error')
}

async function submit() {
  if (!acceptedTerms.value) {
    showToast('لطفاً قوانین و مقررات را تأیید کنید', 'warning')
    return
  }

  isSubmitting.value = true
  listingStore.error = null

  try {
    const issuerProfile = await IssuerProfileService.findOrCreate({
      national_or_company_id: form.value.nationalId,
      name: form.value.issuer,
    })

    const listing = await listingStore.createListing({
      issuer: issuerProfile.id,
      bank_name: form.value.bank,
      cheque_serial_number: form.value.sayad,
      face_amount: form.value.amount || 0,
      due_date: form.value.dueDate,
      issuer_type: form.value.issuerType,
      issuer_name: form.value.issuer,
      issuer_national_id: form.value.nationalId,
      description: form.value.notes,
    })

    if (chequeImageFile.value) {
      try {
        await ListingService.uploadDocument(listing.id, chequeImageFile.value, 'cheque_image')
      } catch {
        showToast('آگهی ثبت شد اما در آپلود تصویر چک خطا رخ داد', 'warning')
      }
    }

    if (idDocFile.value) {
      try {
        await ListingService.uploadDocument(listing.id, idDocFile.value, 'id_document')
      } catch {
        showToast('آگهی ثبت شد اما در آپلود مدرک خطا رخ داد', 'warning')
      }
    }

    currentStep.value = 'success'
    showToast('آگهی شما با موفقیت ثبت شد', 'success')
  } catch (err: unknown) {
    const normalized = normalizeApiError(err)
    showToast(normalized.message || 'خطا در ثبت آگهی. لطفاً دوباره تلاش کنید.', 'error')
  } finally {
    isSubmitting.value = false
  }
}

function goToDashboard() {
  router.push('/app')
}

function goToMarketplace() {
  router.push('/app/listings')
}
</script>

<style scoped>
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

/* Error Banner */
.error-banner {
  background: var(--red-light);
  border: 1px solid rgba(220, 38, 38, 0.2);
  border-radius: var(--radius-sm);
  padding: 0.85rem 1rem;
  font-size: var(--font-size-sm);
  color: var(--red);
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
