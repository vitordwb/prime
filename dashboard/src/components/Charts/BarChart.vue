<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import {
  Chart,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  BarElement,
  BarController,
  Filler
} from 'chart.js'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const root = ref(null)

let chart

Chart.register(BarElement, PointElement, BarController, LinearScale, CategoryScale, Tooltip, Filler)

onMounted(() => {
  chart = new Chart(root.value, {
    type: 'bar',
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          display: false
        },
        x: {
          display: true
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  })
})

const chartData = computed(() => props.data)

watch(chartData, (data) => {
  if (chart) {
    chart.data = data
    chart.update()
  }
})
</script>

<template>
  <canvas ref="root" />
</template>
