<script>
import { computed, ref, onMounted } from 'vue'
import { useFirebaseStore }         from '@/stores/firebaseStore'
import LineChart                    from '@/components/Charts/LineChart.vue'
import SectionTitleLineWithButton   from '@/components/SectionTitleLineWithButton.vue'
import BaseButton                   from '@/components/BaseButton.vue'

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
  Title
  , Tooltip
  , Legend
  , BarElement
  , LineElement
  , CategoryScale
  , LinearScale
)

export default {
  name: 'TemperaturaInternaChart',
  components: { BaseButton, SectionTitleLineWithButton, LineChart },
  setup() {
    const firebaseStore = useFirebaseStore();
    const chartData = ref({
      labels: [],
      datasets: [{
        label: 'Temperatura Interna',
        data: [],
        backgroundColor: [],
        borderColor: [],
        borderWidth: 1
      }]
    });

    const processedData = computed(() => firebaseStore.getProcessedData());

    const fillChartData = () => {
      const newData = firebaseStore.getProcessedData();
      if (newData) {
        chartData.value.labels = newData.getDatetime();
        chartData.value.datasets[0].data = newData.getTemperaturaInterna();
        chartData.value.datasets[0].backgroundColor = newData.getTemperaturaInterna().map(() => 'rgba(75, 192, 192, 0.2)');
        chartData.value.datasets[0].borderColor = newData.getTemperaturaInterna().map(() => 'rgba(75, 192, 192, 1)');
      }
    };

    onMounted(() => {
      firebaseStore.fetchRelayData();
      fillChartData();
    });

    return {
      processedData,
      chartData,
      fillChartData
    };
  },

  watch: {
    processedData: {
      immediate: true,

      handler(newData) {
        if (newData) {
          this.chartData.labels = newData.getDatetime();
          this.chartData.datasets[0].data = newData.getTemperaturaInterna();
          this.chartData.datasets[0].backgroundColor = newData.getTemperaturaInterna().map(() => 'rgba(75, 192, 192, 0.2)');
          this.chartData.datasets[0].borderColor = newData.getTemperaturaInterna().map(() => 'rgba(75, 192, 192, 1)');
        }
      }
    }
  }
}
</script>

<template>
  <div>
    <SectionTitleLineWithButton :icon="mdiChartPie" title="Correntes (A)">
      <BaseButton :icon="mdiReload" color="whiteDark" @click="fillChartData" />
    </SectionTitleLineWithButton>
    <div class="chart-container">
      <LineChart :data="chartData" :options="{ responsive: true, maintainAspectRatio: false }" class="h-96" />
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
}
</style>
