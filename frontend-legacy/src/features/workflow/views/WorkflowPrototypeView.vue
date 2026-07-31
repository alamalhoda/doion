<template>
  <div class="workflow-prototype-view">
    <div class="view-header">
      <div>
        <h1>نمونه اولیه واسط کاربری جریان عملیاتی</h1>
        <p>
          بازسازی UI لایه Marketplace بر اساس سند «نمای کلی جریان عملیاتی»؛ تمرکز روی ثبت، اعتبارسنجی، انتشار، match، توافق خارج از پلتفرم و audit.
        </p>
      </div>
      <span class="view-badge">MVP / Layer 1</span>
    </div>

    <div class="role-panel">
      <span>نقش کاربری:</span>
      <button
        v-for="role in roles"
        :key="role.id"
        class="role-tab"
        :class="{ active: selectedRole === role.id }"
        type="button"
        @click="selectRole(role.id)"
      >
        {{ role.label }}
      </button>
    </div>

    <div class="boundary-alert">
      مرز حقوقی MVP: پلتفرم وجه یا چک را نگهداری نمی‌کند، تسویه را انجام نمی‌دهد، ضمانت وصول نمی‌دهد و قیمت الزام‌آور تعیین نمی‌کند.
    </div>

    <div class="prototype-grid">
      <aside class="timeline-panel">
        <div class="panel-title">
          گام‌های جریان
        </div>
        <button
          v-for="step in visibleSteps"
          :key="step.id"
          class="timeline-item"
          :class="{ active: activeStep.id === step.id }"
          type="button"
          @click="selectStep(step.id)"
        >
          <span class="step-index">{{ step.index }}</span>
          <span class="timeline-copy">
            <strong>{{ step.title }}</strong>
            <small>{{ step.subtitle }}</small>
          </span>
        </button>
      </aside>

      <main class="screen-panel">
        <div class="screen-card">
          <div class="screen-header">
            <div>
              <h2>{{ activeStep.title }}</h2>
              <p>{{ activeStep.subtitle }}</p>
            </div>
            <span
              class="step-tag"
              :class="`step-tag--${activeStep.tagType}`"
            >{{ roleLabel }}</span>
          </div>

          <div class="screen-mock">
            <div class="mock-topbar">
              <span>{{ activeStep.actor }}</span>
              <span>{{ activeStep.output }}</span>
            </div>

            <div
              v-if="activeStep.screen === 'register'"
              class="mock-form"
            >
              <div class="mock-field">
                <span>شماره موبایل</span><em>0912...</em>
              </div>
              <div class="mock-field">
                <span>نام و نام خانوادگی</span><em>علی رضایی</em>
              </div>
              <div class="mock-field">
                <span>نوع کاربر</span><em>دارنده چک</em>
              </div>
              <div class="mock-field">
                <span>رمز عبور</span><em>••••••••</em>
              </div>
            </div>

            <div
              v-else-if="activeStep.screen === 'kyc'"
              class="mock-form"
            >
              <div class="mock-field">
                <span>کد ملی / شناسه شرکت</span><em>0012345678</em>
              </div>
              <div class="mock-field">
                <span>تصویر کارت ملی</span><em>uploaded</em>
              </div>
              <div class="mock-field">
                <span>مدارک حقوقی</span><em>pending</em>
              </div>
              <div class="mock-field">
                <span>سطح KYC</span><em>در انتظار تأیید</em>
              </div>
            </div>

            <div
              v-else-if="activeStep.screen === 'listing'"
              class="mock-form"
            >
              <div class="mock-field wide">
                <span>مبلغ اسمی چک</span><em>۵۰۰,۰۰۰,۰۰۰ ریال</em>
              </div>
              <div class="mock-field">
                <span>تاریخ سررسید</span><em>۱۴۰۵/۰۳/۲۰</em>
              </div>
              <div class="mock-field">
                <span>صادرکننده</span><em>شرکت نمونه</em>
              </div>
              <div class="mock-field">
                <span>نرخ پیشنهادی</span><em>۱۲٪</em>
              </div>
              <div class="mock-field wide">
                <span>توضیحات فرصت</span><em>تأمین مالی کوتاه‌مدت...</em>
              </div>
            </div>

            <div
              v-else-if="activeStep.screen === 'moderation'"
              class="mock-table"
            >
              <div class="table-row header-row">
                <span>آگهی</span><span>مبلغ</span><span>ریسک</span><span>وضعیت</span>
              </div>
              <div class="table-row">
                <span>چک شرکت نمونه</span><span>۵۰۰M ریال</span><span>متوسط</span><span>در انتظار بررسی</span>
              </div>
              <div class="table-row">
                <span>چک پیمانکار الف</span><span>۲۵۰M ریال</span><span>کم</span><span>منتشرشده</span>
              </div>
            </div>

            <div
              v-else-if="activeStep.screen === 'marketplace'"
              class="mock-cards"
            >
              <div class="mock-opportunity">
                <strong>چک شرکت نمونه</strong>
                <span>۵۰۰M ریال · سررسید ۱۴۰۵/۰۳/۲۰</span>
                <em>ریسک متوسط · نرخ پیشنهادی ۱۲٪</em>
              </div>
              <div class="mock-opportunity">
                <strong>چک پیمانکار الف</strong>
                <span>۲۵۰M ریال · سررسید ۱۴۰۵/۰۲/۱۰</span>
                <em>ریسک کم · نرخ پیشنهادی ۹٪</em>
              </div>
            </div>

            <div
              v-else-if="activeStep.screen === 'match'"
              class="mock-card"
            >
              <strong>درخواست علاقه‌مندی</strong>
              <span>سرمایه‌گذار: شرکت تأمین مالی البرز</span>
              <span>پیام: آمادگی بررسی با نرخ ۱۱٪</span>
              <span>نوع تسویه: خارج از پلتفرم</span>
            </div>

            <div
              v-else-if="activeStep.screen === 'deal'"
              class="mock-checklist"
            >
              <div><span />مذاکره نرخ و شرایط</div>
              <div><span />امضای قرارداد خارج از پلتفرم</div>
              <div><span />ظهرنویسی یا انتقال چک</div>
              <div><span />تسویه مستقیم بین طرفین</div>
            </div>

            <div
              v-else-if="activeStep.screen === 'settlement'"
              class="mock-card"
            >
              <strong>ثبت رخداد تسویه خارج از پلتفرم</strong>
              <span>وضعیت: انجام‌شده</span>
              <span>ارجاع خارجی: شماره قرارداد / رسید بانکی</span>
              <span>توضیح: پلتفرم فقط رخداد را ثبت می‌کند.</span>
            </div>

            <div
              v-else
              class="mock-table"
            >
              <div class="table-row header-row">
                <span>زمان</span><span>بازیگر</span><span>رخداد</span><span>وضعیت</span>
              </div>
              <div class="table-row">
                <span>۱۴۰۵/۰۱/۰۲ ۱۰:۲۰</span><span>دارنده چک</span><span>ثبت آگهی</span><span>ثبت‌شده</span>
              </div>
              <div class="table-row">
                <span>۱۴۰۵/۰۱/۰۲ ۱۱:۰۵</span><span>ناظر</span><span>تأیید انتشار</span><span>تکمیل</span>
              </div>
              <div class="table-row">
                <span>۱۴۰۵/۰۱/۰۳ ۰۹:۱۵</span><span>سرمایه‌گذار</span><span>ایجاد match</span><span>در انتظار پاسخ</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <aside class="data-panel">
        <div class="data-card">
          <div class="panel-title">
            ورودی / خروجی / داده‌های لازم
          </div>
          <div class="data-section">
            <span>بازیگر اصلی</span>
            <strong>{{ activeStep.actor }}</strong>
          </div>
          <div class="data-section">
            <span>ورودی‌ها</span>
            <div class="chips">
              <span
                v-for="input in activeStep.inputs"
                :key="input"
              >{{ input }}</span>
            </div>
          </div>
          <div class="data-section">
            <span>خروجی</span>
            <strong>{{ activeStep.output }}</strong>
          </div>
          <div class="data-section">
            <span>داده‌های سیستم</span>
            <div class="field-list">
              <span
                v-for="field in activeStep.dataFields"
                :key="field"
              >{{ field }}</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type WorkflowRole = 'holder' | 'investor' | 'moderator' | 'admin'
type WorkflowStepId = 'register' | 'kyc' | 'listing' | 'moderation' | 'marketplace' | 'match' | 'deal' | 'settlement'

interface WorkflowRoleItem {
  id: WorkflowRole
  label: string
}

interface WorkflowStep {
  id: WorkflowStepId
  title: string
  subtitle: string
  index: number
  roles: WorkflowRole[]
  actor: string
  inputs: string[]
  output: string
  dataFields: string[]
  screen: WorkflowStepId
  tagType: 'default' | 'info' | 'success' | 'warning' | 'error'
}

const roles: WorkflowRoleItem[] = [
  { id: 'holder', label: 'دارنده چک' },
  { id: 'investor', label: 'سرمایه‌گذار' },
  { id: 'moderator', label: 'ناظر' },
  { id: 'admin', label: 'مدیر' },
]

const roleLabelMap: Record<WorkflowRole, string> = {
  holder: 'دارنده چک',
  investor: 'سرمایه‌گذار',
  moderator: 'ناظر',
  admin: 'مدیر',
}

const selectedRole = ref<WorkflowRole>('holder')
const selectedStep = ref<WorkflowStepId>('register')

const steps: WorkflowStep[] = [
  {
    id: 'register',
    title: 'ثبت‌نام و ایجاد حساب',
    subtitle: 'ساخت حساب کاربری و انتخاب نقش اولیه',
    index: 1,
    roles: ['holder', 'investor', 'admin'],
    actor: 'دارنده چک / سرمایه‌گذار / مدیر',
    inputs: ['موبایل یا ایمیل', 'نام', 'رمز عبور', 'نقش کاربری'],
    output: 'حساب کاربری و user_id',
    dataFields: ['user_id', 'full_name', 'phone', 'role', 'account_status'],
    screen: 'register',
    tagType: 'info',
  },
  {
    id: 'kyc',
    title: 'احراز هویت و تعیین سطح دسترسی',
    subtitle: 'KYC پایه و تأیید نقش',
    index: 2,
    roles: ['holder', 'investor', 'moderator', 'admin'],
    actor: 'کاربر / ماژول KYC / ناظر',
    inputs: ['مدارک هویتی', 'اطلاعات شخصی یا حقوقی', 'سطح KYC'],
    output: 'KYC تأیید یا رد و سطح دسترسی',
    dataFields: ['verification_id', 'kyc_status', 'role', 'verification_log'],
    screen: 'kyc',
    tagType: 'warning',
  },
  {
    id: 'listing',
    title: 'ثبت فرصت / آگهی چک',
    subtitle: 'ثبت مشخصات چک و ارسال به moderation',
    index: 3,
    roles: ['holder', 'admin'],
    actor: 'دارنده چک',
    inputs: ['مبلغ چک', 'سررسید', 'صادرکننده', 'مشخصات چک', 'توضیحات'],
    output: 'listing با وضعیت pending_moderation',
    dataFields: ['listing_id', 'face_amount', 'due_date', 'issuer_profile', 'asking_terms'],
    screen: 'listing',
    tagType: 'default',
  },
  {
    id: 'moderation',
    title: 'اعتبارسنجی اولیه و بررسی ناظر',
    subtitle: 'کنترل کیفیت داده و تصمیم انتشار',
    index: 4,
    roles: ['moderator', 'admin'],
    actor: 'ناظر / Moderator',
    inputs: ['آگهی ثبت‌شده', 'مدارک', 'قوانین محتوا'],
    output: 'تأیید، رد یا بازگشت برای اصلاح',
    dataFields: ['moderation_result', 'rejection_reason', 'audit_log'],
    screen: 'moderation',
    tagType: 'error',
  },
  {
    id: 'marketplace',
    title: 'انتشار و جست‌وجوی فرصت‌ها',
    subtitle: 'نمایش آگهی‌های منتشرشده با فیلتر و ریسک',
    index: 5,
    roles: ['investor', 'admin'],
    actor: 'سرمایه‌گذار / سرمایه‌گذار نهادی',
    inputs: ['مبلغ', 'سررسید', 'ریسک', 'جست‌وجو'],
    output: 'فهرست فرصت‌های قابل مشاهده',
    dataFields: ['status', 'risk_tier', 'tags', 'score'],
    screen: 'marketplace',
    tagType: 'success',
  },
  {
    id: 'match',
    title: 'Match و ارتباط‌گیری',
    subtitle: 'اعلام علاقه‌مندی و ایجاد thread ارتباطی',
    index: 6,
    roles: ['investor', 'holder', 'admin'],
    actor: 'سرمایه‌گذار / دارنده چک',
    inputs: ['مشاهده listing', 'پیام', 'نرخ پیشنهادی'],
    output: 'match_id و اعلان به طرفین',
    dataFields: ['match_id', 'listing_id', 'actor_user_id', 'message', 'status'],
    screen: 'match',
    tagType: 'info',
  },
  {
    id: 'deal',
    title: 'مذاکره و توافق خارج از پلتفرم',
    subtitle: 'توافق نهایی بدون مداخله مالی پلتفرم',
    index: 7,
    roles: ['holder', 'investor', 'admin'],
    actor: 'دارنده چک / سرمایه‌گذار',
    inputs: ['نرخ نهایی', 'شرایط معامله', 'اسناد بیرونی'],
    output: 'توافق خارج از پلتفرم',
    dataFields: ['final_discount_rate', 'terms', 'external_reference'],
    screen: 'deal',
    tagType: 'warning',
  },
  {
    id: 'settlement',
    title: 'تسویه خارج از پلتفرم و audit',
    subtitle: 'ثبت رخداد، بدون لمس وجه یا چک',
    index: 8,
    roles: ['holder', 'investor', 'moderator', 'admin'],
    actor: 'طرفین معامله / سیستم audit',
    inputs: ['نتیجه معامله', 'تأیید تسویه', 'ارجاع خارجی'],
    output: 'ثبت settlement status و audit trail',
    dataFields: ['settlement_status', 'timestamp', 'reference', 'event_log'],
    screen: 'settlement',
    tagType: 'success',
  },
]

const roleLabel = computed(() => roleLabelMap[selectedRole.value])

const visibleSteps = computed(() => steps.filter(step => step.roles.includes(selectedRole.value)))

const activeStep = computed(() => steps.find(step => step.id === selectedStep.value) || steps[0])

function selectRole(role: WorkflowRole): void {
  selectedRole.value = role
  const firstVisibleStep = visibleSteps.value.find(step => step.roles.includes(role))
  if (firstVisibleStep) {
    selectedStep.value = firstVisibleStep.id
  }
}

function selectStep(stepId: WorkflowStepId): void {
  selectedStep.value = stepId
}
</script>

<style scoped>
.workflow-prototype-view {
  max-width: 1440px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-6);
  margin-bottom: var(--space-10);
}

.view-header h1 {
  color: var(--navy);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-3);
}

.view-header p {
  color: var(--text2);
  line-height: 1.8;
  max-width: 900px;
  font-size: var(--font-size-base);
}

.view-badge {
  display: inline-block;
  background: var(--navy);
  color: #fff;
  padding: 0.35rem 0.9rem;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
}

.role-panel {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
  margin-bottom: var(--space-6);
  color: var(--text2);
  font-size: var(--font-size-base);
}

.role-tab {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text2);
  border-radius: var(--radius-lg);
  padding: var(--space-2) var(--space-4);
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-family);
  font-size: var(--font-size-base);
}

.role-tab:hover,
.role-tab.active {
  background: var(--navy);
  color: #fff;
  border-color: var(--navy);
}

.boundary-alert {
  background: var(--teal-light);
  border: 1px solid rgba(13, 122, 114, 0.2);
  border-radius: var(--radius);
  padding: var(--space-4) var(--space-5);
  margin-bottom: var(--space-10);
  color: var(--teal);
  font-size: var(--font-size-base);
  line-height: 1.7;
}

.prototype-grid {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr) 320px;
  gap: var(--space-6);
  align-items: start;
}

.timeline-panel,
.data-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.panel-title {
  color: var(--text1);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-base);
  margin-bottom: var(--space-2);
}

.timeline-item {
  width: 100%;
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--surface);
  cursor: pointer;
  text-align: right;
  transition: all 0.2s;
  font-family: var(--font-family);
}

.timeline-item:hover,
.timeline-item.active {
  border-color: var(--navy-light);
  box-shadow: var(--shadow);
  transform: translateY(-1px);
}

.timeline-item.active {
  background: var(--surface2);
  border-color: var(--navy);
}

.step-index {
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--navy);
  color: #fff;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-sm);
}

.timeline-copy {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.timeline-copy strong {
  color: var(--text1);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
}

.timeline-copy small {
  color: var(--text3);
  line-height: 1.6;
  font-size: var(--font-size-xs);
}

.screen-card {
  min-height: 680px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.screen-header {
  display: flex;
  justify-content: space-between;
  gap: var(--space-4);
  align-items: flex-start;
  padding: var(--space-5);
  border-bottom: 1px solid var(--border);
}

.screen-header h2 {
  margin: 0 0 var(--space-2);
  color: var(--navy);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
}

.screen-header p {
  margin: 0;
  color: var(--text3);
  font-size: var(--font-size-base);
}

.step-tag {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  white-space: nowrap;
}

.step-tag--info {
  background: var(--surface2);
  color: var(--text2);
}

.step-tag--success {
  background: var(--teal-light);
  color: var(--teal);
}

.step-tag--warning {
  background: var(--orange-light);
  color: var(--orange);
}

.step-tag--error {
  background: var(--red-light);
  color: var(--red);
}

.step-tag--default {
  background: var(--surface2);
  color: var(--text2);
}

.screen-mock {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg);
  margin: var(--space-5);
}

.mock-topbar {
  display: flex;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-5);
  background: var(--surface2);
  color: var(--navy);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  border-bottom: 1px solid var(--border);
}

.mock-form,
.mock-table,
.mock-cards,
.mock-card,
.mock-checklist {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.mock-field {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
}

.mock-field.wide {
  align-items: flex-start;
  flex-direction: column;
}

.mock-field span {
  color: var(--text3);
  font-size: var(--font-size-sm);
}

.mock-field em {
  color: var(--navy);
  font-style: normal;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-base);
}

.table-row {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr 1.2fr;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font-size: var(--font-size-sm);
}

.table-row.header-row {
  color: var(--text3);
  font-weight: var(--font-weight-semibold);
  background: transparent;
}

.mock-opportunity,
.mock-card {
  padding: var(--space-5);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--surface);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.mock-opportunity strong,
.mock-card strong {
  color: var(--navy);
  font-size: var(--font-size-md);
}

.mock-opportunity span,
.mock-opportunity em,
.mock-card span {
  color: var(--text2);
  font-style: normal;
  font-size: var(--font-size-base);
}

.mock-checklist {
  gap: var(--space-4);
}

.mock-checklist div {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--text1);
  font-size: var(--font-size-base);
}

.mock-checklist span {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border);
  border-radius: 4px;
  flex-shrink: 0;
}

.data-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  position: sticky;
  top: var(--space-8);
}

.data-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-4) 0;
  border-bottom: 1px solid var(--border);
}

.data-section:last-child {
  border-bottom: none;
}

.data-section span:first-child {
  color: var(--text3);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.data-section strong {
  color: var(--navy);
  line-height: 1.7;
  font-size: var(--font-size-base);
}

.chips,
.field-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.chips span,
.field-list span {
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-sm);
  background: var(--surface2);
  color: var(--text2);
  border: 1px solid var(--border);
  font-size: var(--font-size-xs);
}

@media (max-width: 1180px) {
  .prototype-grid {
    grid-template-columns: 1fr;
  }

  .data-card {
    position: static;
  }

  .timeline-panel {
    overflow-x: auto;
  }

  .timeline-item {
    min-width: 260px;
  }
}

@media (max-width: 720px) {
  .view-header {
    flex-direction: column;
  }

  .table-row {
    grid-template-columns: 1fr;
  }

  .mock-topbar {
    flex-direction: column;
  }
}
</style>
