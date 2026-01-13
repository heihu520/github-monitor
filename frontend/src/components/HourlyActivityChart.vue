<template>
  <div ref="chartRef" class="hourly-activity-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

// 注册ECharts组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  BarChart,
  CanvasRenderer
])

// Props定义
interface Props {
  data?: number[]
}

const props = withDefaults(defineProps<Props>(), {
  data: () => []
})

// Refs
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

/**
 * 生成24小时模拟数据
 */
function generateMockData(): number[] {
  if (props.data && props.data.length > 0) {
    return props.data
  }
  
  // 模拟24小时活跃度数据（早9点到晚11点较活跃）
  return Array.from({ length: 24 }, (_, hour) => {
    if (hour >= 9 && hour <= 23) {
      return Math.floor(Math.random() * 15) + 5
    }
    return Math.floor(Math.random() * 3)
  })
}

/**
 * 初始化图表
 */
function initChart() {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

/**
 * 更新图表数据
 */
function updateChart() {
  if (!chartInstance) return

  const hourlyData = generateMockData()
  const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#4a90e2',
      borderWidth: 1,
      textStyle: {
        color: '#e2e8f0'
      },
      axisPointer: {
        type: 'shadow',
        shadowStyle: {
          color: 'rgba(74, 144, 226, 0.1)'
        }
      },
      formatter: (params: any) => {
        const data = params[0]
        return `${data.name}<br/>提交数: <strong>${data.value}</strong>`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hours,
      axisLine: {
        lineStyle: {
          color: '#334155'
        }
      },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 10,
        interval: 2
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#334155'
        }
      },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 12
      },
      splitLine: {
        lineStyle: {
          color: '#1e293b',
          type: 'dashed'
        }
      }
    },
    series: [
      {
        name: '提交数',
        type: 'bar',
        data: hourlyData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#4a90e2' },
            { offset: 1, color: '#7c5cdb' }
          ]),
          borderRadius: [4, 4, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#60a5fa' },
              { offset: 1, color: '#9d7ce8' }
            ]),
            shadowBlur: 10,
            shadowColor: 'rgba(74, 144, 226, 0.5)'
          }
        },
        barWidth: '60%'
      }
    ]
  }

  chartInstance.setOption(option)
}

/**
 * 监听数据变化
 */
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

/**
 * 组件挂载
 */
onMounted(() => {
  initChart()
  
  // 响应式调整
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})

/**
 * 组件卸载
 */
onBeforeUnmount(() => {
  chartInstance?.dispose()
})
</script>

<style scoped>
.hourly-activity-chart {
  width: 100%;
  height: 100%;
  min-height: 250px;
}
</style>