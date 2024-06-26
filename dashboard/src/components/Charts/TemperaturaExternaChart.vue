<script>
import { computed, onMounted, ref } from 'vue'
import { useFirebaseStore }         from '@/stores/firebaseStore'
import LineChart                    from '@/components/Charts/LineChart.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import BaseButton from '@/components/BaseButton.vue'

import {
    Chart as ChartJS
  , Title
  , Tooltip
  , Legend
  , BarElement
  , CategoryScale
  , LinearScale
  , LineElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  LineElement,
  CategoryScale,
  LinearScale
)

export default {
  name: 'TemperaturaExternaChart',
  components: { BaseButton, SectionTitleLineWithButton, LineChart },
  setup() {
    const firebaseStore = useFirebaseStore();
    const chartData = ref(null);

    const processedData = computed(() => firebaseStore.getProcessedData());

    onMounted(() => {
      firebaseStore.getProcessedData();
      this.fillChartData();
    });

    return {
      processedData,
      chartData
    };
  },

  data() {
    return {
      chartOptions: {
        responsive: true
      }
    }
  },

  methods: {
    fillChartData() {
      const data = this.processedData;
      this.chartData = sampleChartData(data);
    }
  }
}

const chartColors = {
  default: {
    primary: '#00D1B2',
    info: '#209CEE',
    danger: '#FF3860'
  }
}

const datasetObject = (color, data) => {
  return {
    fill: false,
    borderColor: chartColors.default[color],
    borderWidth: 2,
    borderDash: [],
    borderDashOffset: 0.0,
    pointBackgroundColor: chartColors.default[color],
    pointBorderColor: 'rgba(255,255,255,0)',
    pointHoverBackgroundColor: chartColors.default[color],
    pointBorderWidth: 20,
    pointHoverRadius: 4,
    pointHoverBorderWidth: 15,
    pointRadius: 4,
    data: data,
    tension: 0.5,
    cubicInterpolationMode: 'default'
  }
}

const sampleChartData = (processedData) => {
  const labels = [...processedData.getDatetime()];

  return {
    labels,
    datasets: [
      datasetObject('primary', processedData.getTemperaturaExterna())
    ]
  }
}
</script>

<template>
  <SectionTitleLineWithButton :icon="mdiChartPie" title="Temperatura Externa">
    <BaseButton :icon="mdiReload" color="whiteDark" @click="fillChartData" />
  </SectionTitleLineWithButton>
  <line-chart :data="chartData" :options="chartOptions" class="h-96" />
</template>
