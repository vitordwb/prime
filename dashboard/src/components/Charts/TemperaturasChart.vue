<script>
import { computed, onMounted, ref } from 'vue'
import { useFirebaseStore } from '@/stores/firebaseStore'
import LineChart from '@/components/Charts/LineChart.vue'
import BaseButton from '@/components/BaseButton.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox from '@/components/CardBox.vue'
import { getChartData } from '@/components/Charts/chartdata.config.js'

import {
  mdiReload,
  mdiChartPie,
} from '@mdi/js'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement
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
  name: 'TemperaturasChart',
  components: { CardBox, SectionTitleLineWithButton, BaseButton, LineChart },
  setup() {
    const firebaseStore = useFirebaseStore();
    const processedData = computed(() => firebaseStore.getProcessedData());
    const chartData = ref({});

    const fillChartData = () => {
      chartData.value = getChartData(
        processedData.value.getDatetime(),
        { data: processedData.value.getTemperaturaCobre(), label: 'Temperatura Cobre' },
        { data: processedData.value.getTemperaturaExterna(), label: 'Temperatura Externa' },
        { data: processedData.value.getTemperaturaInterna(), label: 'Temperatura Interna' }
      );
    };

    onMounted(() => {
      fillChartData();
    });

    return {
      chartData,
      fillChartData,
      mdiReload,
      mdiChartPie
    };
  }
}
</script>

<template>
  <SectionTitleLineWithButton :icon="mdiChartPie" title="Temperaturas (ºC)">
    <BaseButton :icon="mdiReload" color="whiteDark" @click="fillChartData" />
  </SectionTitleLineWithButton>

  <CardBox class="mb-6">
    <div>
      <line-chart :data="chartData" class="h-96" />
    </div>
  </CardBox>
</template>
