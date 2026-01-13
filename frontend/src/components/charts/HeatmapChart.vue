<template>
  <div ref="chartRef" class="heatmap-chart"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { HeatmapData } from '@/stores/stats'

interface Props {
  data: HeatmapData[]
}

const props = defineProps<Props>()

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

// 格式化日期显示
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 初始化图表
function initChart() {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)
  
  // 准备数据格式 [[date, commits]]
  const chartData = props.data.map(item => [item.date, item.commits])
  
  // 计算日期范围
  const startDate = props.data[0]?.date || new Date().toISOString().split('T')[0]
  const endDate = props.data[props.data.length - 1]?.date || new Date().toISOString().split('T')[0]

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 20, 25, 0.95)',
      borderColor: '#4a90e2',
      borderWidth: 1,
      textStyle: {
        color: '#e8eaed',
        fontSize: 13
      },
      formatter: function (params: any) {
        const date = params.data[0]
        const commits = params.data[1]
        return `
          <div style="padding: 4px;">
            <div style="font-weight: 600; margin-bottom: 4px;">${formatDate(date)}</div>
            <div style="color: #9ba3af;">
              <span style="color: #4a90e2;">●</span> ${commits} 次提交
            </div>
          </div>
        `
      }
    },
    visualMap: {
      show: false,
      min: 0,
      max: 20,
      inRange: {
        color: [
          '#0f1419',      // 0次 - 深色背景
          '#0e4429',      // 1-3次 - 深绿
          '#006d32',      // 4-6次 - 绿色
          '#26a641',      // 7-10次 - 亮绿
          '#39d353'       // 10+次 - 鲜绿
        ]
      }
    },
    calendar: {
      top: 20,
      left: 50,
      right: 20,
      bottom: 10,
      range: [startDate, endDate],
      cellSize: ['auto', 13],
      splitLine: {
        show: true,
        lineStyle: {
          color: '#1f2937',
          width: 2,
          type: 'solid'
        }
      },
      itemStyle: {
        borderColor: '#0f1419',
        borderWidth: 3
      },
      yearLabel: {
        show: true,
        color: '#9ba3af',
        fontSize: 14,
        fontWeight: 600
      },
      monthLabel: {
        show: true,
        color: '#6b7280',
        fontSize: 11
      },
      dayLabel: {
        show: true,
        firstDay: 1,
        color: '#6b7280',
        fontSize: 11,
        nameMap: ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      }
    },
    series: [
      {
        type: 'heatmap',
        coordinateSystem: 'calendar',
        data: chartData,
        emphasis: {
          itemStyle: {
            borderColor: '#4a90e2',
            borderWidth: 2,
            shadowBlur: 10,
            shadowColor: 'rgba(74, 144, 226, 0.5)'
          }
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

// 响应式调整
function handleResize() {
  chartInstance?.resize()
}

// 监听数据变化
watch(() => props.data, () => {
  if (chartInstance) {
    initChart()
  }
}, { deep: true })

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.heatmap-chart {
  width: 100%;
  height: 100%;
  min-height: 200px;
}
</style>