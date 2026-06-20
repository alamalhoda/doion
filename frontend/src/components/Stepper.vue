<template>
  <div class="stepper" role="navigation" aria-label="مراحل فرم">
    <div
      v-for="step in steps"
      :key="step.index"
      class="stepper-step"
      :class="stepClasses(step)"
    >
      <div class="stepper-circle">{{ step.index }}</div>
      <div class="stepper-label">{{ step.label }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Step {
  index: number
  label: string
}

const props = defineProps<{
  steps: Step[]
  current: number
}>()

function stepClasses(step: Step) {
  if (step.index < props.current) return 'stepper-step--done'
  if (step.index === props.current) return 'stepper-step--active'
  return 'stepper-step--pending'
}
</script>

<style>
.stepper {
  display: flex;
  gap: 0;
  margin-bottom: 2rem;
}

.stepper-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  position: relative;
}

.stepper-step::before {
  content: '';
  position: absolute;
  top: 14px;
  left: -50%;
  width: 100%;
  height: 2px;
  background: var(--border);
  z-index: 0;
}

.stepper-step:first-child::before {
  display: none;
}

.stepper-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: var(--font-weight-semibold);
  position: relative;
  z-index: 1;
  transition: background-color var(--transition-base), color var(--transition-base);
}

.stepper-step--done .stepper-circle {
  background: var(--teal);
  color: #fff;
}

.stepper-step--active .stepper-circle {
  background: var(--navy);
  color: #fff;
}

.stepper-step--pending .stepper-circle {
  background: var(--border);
  color: var(--text3);
}

.stepper-label {
  font-size: var(--font-size-xs);
  color: var(--text3);
  text-align: center;
}
</style>
