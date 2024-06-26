<script>
import { useFirebaseStore }       from '@/stores/firebaseStore'
import { computed, onMounted }    from 'vue'

import LayoutAuthenticated        from '@/layouts/LayoutAuthenticated.vue'
import SectionMain                from '@/components/SectionMain.vue'
import CardBox                    from '@/components/CardBox.vue'
// import CardBoxWidget              from '@/components/CardBoxWidget.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
// import BaseButton                 from '@/components/BaseButton.vue'
// import TemperaturaInternaChart    from '@/components/Charts/TemperaturaInternaChart.vue'
// import TemperaturaExternaChart    from '@/components/Charts/TemperaturaExternaChart.vue'
// import TemperaturasChart          from '@/components/Charts/TemperaturasChart.vue'
// import CiclosChart                from '@/components/Charts/CiclosChart.vue'
// import CorrenteBaixoChart         from '@/components/Charts/CorrenteBaixoChart.vue'
import CorrenteCimaChart from '@/components/Charts/CorrenteCimaChart.vue'

import {
    mdiChartTimelineVariant
  , mdiReload
  , mdiChartPie
  , mdiMonitorDashboard
  , mdiGithub
  , mdiCoolantTemperature
  , mdiLightningBolt
  , mdiPowerPlug
} from '@mdi/js'

import { Chart as ChartJS
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
  name: 'BarChart',
  components: {
      CorrenteCimaChart
    , CardBox
    , LayoutAuthenticated
    , SectionMain
    , SectionTitleLineWithButton
  },
  setup() {
    const firebaseStore = useFirebaseStore();

    const relayData = computed(() => firebaseStore.relayData);
    const loading   = computed(() => firebaseStore.loading);
    const error     = computed(() => firebaseStore.error);

    onMounted(() => {
      firebaseStore.fetchRelayData();
    });

    return {
        relayData
      , loading
      , error
    };
  },

  data() {
    return {
        mdiChartPie
      , mdiReload
      , mdiChartTimelineVariant
      , mdiMonitorDashboard
      , mdiGithub
      , mdiCoolantTemperature
      , mdiLightningBolt
      , mdiPowerPlug
    }
  }
}
</script>

<template>
  <LayoutAuthenticated>
    <SectionMain>

      <SectionTitleLineWithButton :icon="mdiMonitorDashboard" title="Monitoramento" main>
      </SectionTitleLineWithButton>

<!--      <corrente-baixo-chart/>-->

<!--      <temperaturas-chart/>-->

<!--      <CardBox class="mb-6">-->
<!--        <div>-->
<!--          <temperatura-interna-chart/>-->
<!--        </div>-->
<!--      </CardBox>-->

      <CardBox class="mb-6">
        <div>
          <corrente-cima-chart/>
        </div>
      </CardBox>

<!--      <CardBox class="mb-6">-->
<!--        <div>-->
<!--          <temperatura-externa-chart/>-->
<!--        </div>-->
<!--      </CardBox>-->

<!--      <ciclos-chart/>-->

<!--      <SectionTitleLineWithButton :icon="mdiChartPie" title="Sensor Baixo">-->
<!--        <BaseButton :icon="mdiReload" color="whiteDark" />-->
<!--      </SectionTitleLineWithButton>-->


<!--      <CardBox class="mb-6">-->
<!--        <div>-->
<!--          <corrente-baixo-chart/>-->
<!--        </div>-->
<!--      </CardBox>-->

    </SectionMain>
  </LayoutAuthenticated>
</template>
