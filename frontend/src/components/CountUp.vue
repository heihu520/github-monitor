<template>
  <span class="count-up">{{ displayValue }}</span>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

interface Props {
  value: number
  duration?: number
  decimals?: number
}

const props = withDefaults(defineProps<Props>(), {
  duration: 1,
  decimals: 0
})

const displayValue = ref('0')

const animate = (start: number, end: number) => {
  const startTime = Date.now()
  const duration = props.duration * 1000

  const update = () => {
    const now = Date.now()
    const progress = Math.min((now - startTime) / duration, 1)
    
    // 使用easeOutCubic缓动函数
    const easeProgress = 1 - Math.pow(1 - progress, 3)
    const current = start + (end - start) * easeProgress

    if (props.decimals > 0) {
      displayValue.value = current.toFixed(props.decimals)
    } else {
      displayValue.value = Math.floor(current).toLocaleString()
    }

    if (progress < 1) {
      requestAnimationFrame(update)
    }
  }

  requestAnimationFrame(update)
}

watch(
  () => props.value,
  (newValue, oldValue) => {
    const start = oldValue || 0
    animate(start, newValue)
  }
)

onMounted(() => {
  animate(0, props.value)
})
</script>

<style scoped>
.count-up {
  display: inline-block;
  font-variant-numeric: tabular-nums;
}
</style>