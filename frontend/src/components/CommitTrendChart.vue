<template>
  <div ref="chartRef" class="commit-trend-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { TrendData } from '@/stores/stats'

// 注册ECharts组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer
])

// Props定义
interface Props {
  data: TrendData[]
}

const props = defineProps<Props>()

// Refs
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

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
  if (!chartInstance || !props.data.length) return

  const dates = props.data.map(item => item.date.slice(5)) // MM-DD格式
  const commits = props.data.map(item => item.commits)

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#4a90e2',
      borderWidth: 1,
      textStyle: {
        color: '#e2e8f0'
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
      boundaryGap: false,
      data: dates,
      axisLine: {
        lineStyle: {
          color: '#334155'
        }
      },
      axisLabel: {
        color: '#94a3b8',
        fontSize: 12
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
        type: 'line',
        smooth: true,
        data: commits,
        lineStyle: {
          color: '#4a90e2',
          width: 3
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(74, 144, 226, 0.3)' },
            { offset: 1, color: 'rgba(74, 144, 226, 0.05)' }
          ])
        },
        itemStyle: {
          color: '#4a90e2',
          borderColor: '#1e293b',
          borderWidth: 2
        },
        emphasis: {
          itemStyle: {
            color: '#60a5fa',
            borderColor: '#4a90e2',
            borderWidth: 3,
            shadowBlur: 10,
            shadowColor: 'rgba(74, 144, 226, 0.5)'
          }
        }
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
.commit-trend-chart {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>