<script>
import { computed, onMounted }    from 'vue'
import { useFirebaseStore }       from '@/stores/firebaseStore'
import LineChart                  from '@/components/Charts/LineChart.vue'

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
  name: 'CorrenteBaixoChart',
  components: { LineChart },
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
            "label": "Consumo",
            "fill": false,
            "borderColor": "#00D1B2",
            "borderWidth": 2,
            "borderDash": [],
            "borderDashOffset": 0,
            "pointBackgroundColor": "#00D1B2",
            "pointBorderColor": "rgba(255,255,255,0)",
            "pointHoverBackgroundColor": "#00D1B2",
            "pointBorderWidth": 20,
            "pointHoverRadius": 4,
            "pointHoverBorderWidth": 15,
            "pointRadius": 4,
            "data": this.processedData.getConsumoBaixo(),
            "tension": 0.5,
            "cubicInterpolationMode": "default"
          },
          {
            "label": "Potencia Aparente",
            "fill": false,
            "borderColor": "#209CEE",
            "borderWidth": 2,
            "borderDash": [],
            "borderDashOffset": 0,
            "pointBackgroundColor": "#209CEE",
            "pointBorderColor": "rgba(255,255,255,0)",
            "pointHoverBackgroundColor": "#209CEE",
            "pointBorderWidth": 20,
            "pointHoverRadius": 4,
            "pointHoverBorderWidth": 15,
            "pointRadius": 4,
            "data": this.processedData.getPotenciaAparenteBaixo(),
            "tension": 0.5,
            "cubicInterpolationMode": "default"
          },
          {
            "label": "Potencia Ativa",
            "fill": false,
            "borderColor": "#FF3860",
            "borderWidth": 2,
            "borderDash": [],
            "borderDashOffset": 0,
            "pointBackgroundColor": "#FF3860",
            "pointBorderColor": "rgba(255,255,255,0)",
            "pointHoverBackgroundColor": "#FF3860",
            "pointBorderWidth": 20,
            "pointHoverRadius": 4,
            "pointHoverBorderWidth": 15,
            "pointRadius": 4,
            "data": this.processedData.getPotenciaAtivaBaixo(),
            "tension": 0.5,
            "cubicInterpolationMode": "default"
          },
          {
            "label": "Potencia Rms",
            "fill": false,
            "borderColor": "#FF3860",
            "borderWidth": 2,
            "borderDash": [],
            "borderDashOffset": 0,
            "pointBackgroundColor": "#FF3860",
            "pointBorderColor": "rgba(255,255,255,0)",
            "pointHoverBackgroundColor": "#FF3860",
            "pointBorderWidth": 20,
            "pointHoverRadius": 4,
            "pointHoverBorderWidth": 15,
            "pointRadius": 4,
            "data": this.processedData.getPotenciaRmsBaixo(),
            "tension": 0.5,
            "cubicInterpolationMode": "default"
          }
        ]
      }
    }
  }
}
</script>

<template>
    <line-chart :data="chartData" class="h-96" />
</template>
