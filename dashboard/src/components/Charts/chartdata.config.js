export const chartColors = {
  default: {
    primary: '#00D1B2',
    info: '#209CEE',
    danger: '#FF3860'
  }
}

const datasetObject = (color, data, label) => {
  return {
    label: label,
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

export const getChartData = (time, ...dataSets) => {
  const colors = ['primary', 'info', 'danger'];
  const datasets = dataSets.map((dataSet, index) => datasetObject(colors[index], dataSet.data, dataSet.label));

  return {
    labels: time,
    datasets: datasets
  }
}
