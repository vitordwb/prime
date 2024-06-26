<script setup>
import { computed, onMounted, ref } from 'vue'
import { useFirebaseStore }         from '@/stores/firebaseStore'
import * as chartConfig             from '@/components/Charts/chartdata.config.js'
import BarChart                     from '@/components/Charts/BarChart.vue'
import SectionTitleLineWithButton   from '@/components/SectionTitleLineWithButton.vue'
import CardBox                      from '@/components/CardBox.vue'
import BaseButton                   from '@/components/BaseButton.vue'
import {
    mdiChartPie
  , mdiReload
} from '@mdi/js'


const chartData = ref(null)
const firebaseStore = useFirebaseStore();
const relayData = computed(() => firebaseStore.relayData);

const fillChartData = () => {
  chartData.value = chartConfig.getChartData()
}

onMounted(() => {
  if (!relayData.value) {
    firebaseStore.fetchRelayData();
  }
  fillChartData();
})

</script>

<template>

      <SectionTitleLineWithButton :icon="mdiChartPie" title="Corrente Cima">
        <BaseButton :icon="mdiReload" color="whiteDark" @click="fillChartData" />
      </SectionTitleLineWithButton>

      <CardBox class="mb-6">
        <div v-if="chartData">
          <bar-chart :data="chartData" class="h-96" />
        </div>
      </CardBox>

</template>
