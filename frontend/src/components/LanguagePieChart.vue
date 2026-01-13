<template>
  <div ref="chartRef" class="language-pie-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { LanguageStat } from '@/stores/stats'

// 注册ECharts组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  PieChart,
  CanvasRenderer
])

// Props定义
interface Props {
  data: LanguageStat[]
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

  const chartData = props.data.map(item => ({
    value: item.percentage,
    name: item.name,
    itemStyle: {
      color: item.color
    }
  }))

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      borderColor: '#4a90e2',
      borderWidth: 1,
      textStyle: {
        color: '#e2e8f0'
      },
      formatter: (params: any) => {
        return `${params.name}<br/>占比: <strong>${params.value}%</strong><br/>提交: ${params.data.commits || 0}次`
      }
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: {
        color: '#94a3b8',
        fontSize: 11
      },
      itemGap: 8,
      itemWidth: 12,
      itemHeight: 12
    },
    series: [
      {
        name: '语言分布',
        type: 'pie',
        radius: ['45%', '75%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: 'rgba(74, 144, 226, 0.3)',
          borderWidth: 2,
          shadowBlur: 10,
          shadowColor: 'rgba(74, 144, 226, 0.2)'
        },
        label: {
          show: true,
          position: 'outside',
          color: '#e2e8f0',
          fontSize: 11,
          fontWeight: 'bold',
          formatter: '{b}\n{d}%',
          textBorderColor: 'rgba(74, 144, 226, 0.5)',
          textBorderWidth: 1,
          textShadowColor: 'rgba(0, 0, 0, 0.8)',
          textShadowBlur: 2
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
            color: '#ffffff'
          },
          itemStyle: {
            shadowBlur: 15,
            shadowOffsetX: 0,
            shadowColor: 'rgba(74, 144, 226, 0.8)'
          },
          scale: true,
          scaleSize: 8
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10,
          lineStyle: {
            color: '#4a90e2',
            width: 1.5
          }
        },
        data: chartData.map((item, index) => ({
          ...item,
          commits: props.data[index].commits
        }))
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
.language-pie-chart {
  width: 100%;
  height: 100%;
  min-height: 250px;
}
</style>