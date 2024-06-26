<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useFirebaseStore }         from '@/stores/firebaseStore'
import LayoutAuthenticated          from '@/layouts/LayoutAuthenticated.vue'
import * as chartConfig             from '@/components/Charts/chart.config.js'
import SectionTitleLineWithButton   from '@/components/SectionTitleLineWithButton.vue'
import SectionMain                  from '@/components/SectionMain.vue'
import CardBoxWidget                from '@/components/CardBoxWidget.vue'
import TemperaturasChart            from '@/components/Charts/TemperaturasChart.vue'
import CorrentesRmsChart            from '@/components/Charts/CorrentesRmsChart.vue'
import VentiladoresChart            from '@/components/Charts/VentiladoresChart.vue'
import RpmChart                     from '@/components/Charts/RpmChart.vue'
import NotificationBar              from '@/components/NotificationBar.vue'
import {
    mdiChartTimelineVariant
  , mdiCoolantTemperature
  , mdiReload
  , mdiAlertCircle
} from '@mdi/js'


const chartData = ref(null)
const firebaseStore = useFirebaseStore();
const relayData = computed(() => firebaseStore.relayData);

const showAlerta = ref(false);
const messageAlert = ref('');
const colorAlert = ref('info');

const fillChartData = () => {
  chartData.value = chartConfig.sampleChartData()
}

onMounted(() => {
  if (!relayData.value) {
    firebaseStore.fetchRelayData();
  }
  fillChartData();
})

const cycle        = () => relayData.value[relayData.value.length - 1].counter
const temp_interna = () => relayData.value[relayData.value.length - 1].temperatura_interna[1].toFixed(1)
const temp_externa = () => relayData.value[relayData.value.length - 1].temperatura_externa[1].toFixed(1)

const changeColor = (state) => {
  if (
       state === 'TEMPERATURA MUITO ALTA'
    || state === 'TEMPERATURA INTERNA E EXTERNA MUITO ALTAS'
  ) {
    return 'danger'
  }

  if (state === 'TEMPERATURA MUITO BAIXA') return 'info'

  return 'warning';
}

const updateAlertState = () => {
  const lastItem = relayData.value[relayData.value.length - 1];
  if (lastItem && lastItem.state) {
    const state = lastItem.state;

    if (
         state === 'TEMPERATURA MUITO BAIXA'
      || state === 'TEMPERATURA MUITO ALTA'
      || state === 'TENTATIVA DE REFRIGERACAO FREE COOLING'
      || state === 'TEMPERATURA INTERNA E EXTERNA MUITO ALTA'
      || state === 'TEMPERATURA ABAIXANDO'
      || state === 'PORTA ABERTA'
    ) {
      colorAlert.value = changeColor(state);
      showAlerta.value = true;
      messageAlert.value = state;
    }

    else {
      showAlerta.value = false;
      messageAlert.value = '';
    }
  }
};

// função reativa para receber quando chegam novos dados no banco de dados
watch(() => relayData.value, updateAlertState,  { immediate: true });

</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>

      <NotificationBar v-if="showAlerta" :color="colorAlert" :icon="mdiAlertCircle" >
        <b>ALERTA</b>. {{ messageAlert }}
      </NotificationBar>

      <SectionTitleLineWithButton :icon="mdiChartTimelineVariant" title="Visão Geral" main>
      </SectionTitleLineWithButton>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 mb-6">
        <CardBoxWidget
          :trend="cycle() > 10000 ? 'trocar relé' : 'normal'"
          :trend-type="cycle() > 10000 ? 'alert' : 'normal'"
          color="text-emerald-500"
          :icon="mdiReload"
          :number="cycle()"
          label="Ciclos"
        />
        <CardBoxWidget
          :trend="temp_interna() > 40 ? 'quente' : 'normal'"
          :trend-type="temp_interna() > 40 ? 'alert' : 'normal'"
          color="text-blue-500"
          :icon="mdiCoolantTemperature"
          :number="temp_interna()"
          suffix="ºC"
          label="Temperatura Interna"
        />
        <CardBoxWidget
          :trend="temp_externa > 40 ? 'quente' : 'normal'"
          :trend-type="temp_externa > 40 ? 'alert' : 'normal'"
          color="text-red-500"
          :icon="mdiChartTimelineVariant"
          :number="temp_externa()"
          suffix="ºC"
          label="Temperatura Externa"
        />
      </div>

      <temperaturas-chart/>

      <rpm-chart/>

      <ventiladores-chart/>

      <correntes-rms-chart/>

    </SectionMain>
  </LayoutAuthenticated>
</template>
