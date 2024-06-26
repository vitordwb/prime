export const chartColors = {
  default: {
    primary: '#00D1B2',
    info: '#209CEE',
    danger: '#FF3860'
  }
}

const randomChartData = () => {
    const data = []

    // Primeiros 10 elementos variando entre 4800 e 5100
    for (let i = 0; i < 25; i++) {
      data.push(Math.round(Math.random() * 4) + 22)
    }

    // // Próximos 8 elementos iguais a 0
    // for (let i = 0; i < 8; i++) {
    //   data.push(0)
    // }
    //
    // // Últimos 5 elementos variando entre 4800 e 5100
    // for (let i = 0; i < 5; i++) {
    //   data.push(Math.round(Math.random() * 300) + 4800)
    // }

    return data
  }



const datasetObject = (color, points) => {
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
    data: randomChartData(points),
    tension: 0.5,
    cubicInterpolationMode: 'default'
  }
}

function generateTimestamps(startTimeStr, numIterations, intervalMinutes) {
  // Converte a string de tempo inicial para um objeto Date
  let startTime = new Date(startTimeStr);

  // Cria uma array para armazenar os timestamps
  let timestamps = [];

  // Itera e cria os timestamps
  for (let i = 0; i < numIterations; i++) {
    let newTime = new Date(startTime.getTime() + i * intervalMinutes * 60000);
    timestamps.push(newTime.toISOString().replace('T', ' ').substring(0, 19));
  }

  return timestamps;
}


export const sampleChartData = (points = 25) => {
  // const labels = []

  // for (let i = 1; i <= points; i++) {
  //   labels.push(`0${i}`)

  let startTimeStr = '2024-02-30T09:24:44';
  let numIterations = 23;
  let intervalMinutes = 5;

  const labels = generateTimestamps(startTimeStr, numIterations, intervalMinutes)

  return {
    labels,
    datasets: [
      datasetObject('primary', points),
      datasetObject('info', points),
      datasetObject('danger', points)
    ]
  }
}
