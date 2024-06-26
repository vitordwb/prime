<script>
import { computed, onMounted }    from 'vue'
import { useFirebaseStore }       from '@/stores/firebaseStore'
import BarChart                   from '@/components/Charts/BarChart.vue'
import BaseButton                 from '@/components/BaseButton.vue'
import SectionTitleLineWithButton from '@/components/SectionTitleLineWithButton.vue'
import CardBox                    from '@/components/CardBox.vue'

import {
  mdiReload,
  mdiChartPie,
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
  name: 'CiclosChart',
  components: { CardBox, SectionTitleLineWithButton, BaseButton, BarChart },
  setup() {
    const firebaseStore = useFirebaseStore();
    const processedData = computed(() => firebaseStore.getProcessedData());

    onMounted(() => {
      firebaseStore.getProcessedData();
    });

    return {
      processedData
    };
  },

  data() {
    return {
      mdiReload,
      mdiChartPie,
      chartData: {
        "labels": this.processedData.getDatetime(),
        "datasets": [
          {
            "fill": true,
            "borderColor": "#00D1B2",
            "borderWidth": 2,
            "borderDash": [],
            "borderDashOffset": 0,
            "data": this.processedData.getCycle(),
          }
        ]
      }
    }
  },

  methods: {
    getAlert() {
      alert('funcionou')
    }
  }
}
</script>

<template>
  <SectionTitleLineWithButton :icon="mdiChartPie" title="Ciclos">
    <BaseButton :icon="mdiReload" color="whiteDark" @click="getAlert" />
  </SectionTitleLineWithButton>

  <CardBox class="mb-6">
    <div>
      <bar-chart :data="chartData" class="h-96" />
    </div>
  </CardBox>
</template>
