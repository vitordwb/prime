export function processRelayData(data) {
  return {
    getCycle:                 () => data.map(item => item.counter[1]),
    getDatetime:              () => data.map(item => item.datetime),
    getState:                 () => data.map(item => item.state),

    getTemperaturaCobre:      () => data.map(item => item.temperatura_cobre[1]),
    getTemperaturaInterna:    () => data.map(item => item.temperatura_interna[1]),
    getTemperaturaExterna:    () => data.map(item => item.temperatura_externa[1]),

    getConsumoBaixo:          () => data.map(item => item.corrente_baixo[1].consumo),
    getPotenciaAparenteBaixo: () => data.map(item => item.corrente_baixo[1].potencia_apa),
    getPotenciaAtivaBaixo:    () => data.map(item => item.corrente_baixo[1].potencia_ativ),
    getPotenciaRmsBaixo:      () => data.map(item => item.corrente_baixo[1].corrente_rms),

    getConsumoCima:           () => data.map(item => item.corrente_cima[1].consumo),
    getPotenciaAparenteCima:  () => data.map(item => item.corrente_cima[1].potencia_apa),
    getPotenciaAtivaCima:     () => data.map(item => item.corrente_cima[1].potencia_ativ),
    getPotenciaRmsCima:       () => data.map(item => item.corrente_cima[1].corrente_rms),

    getRpmCima:               () => data.map(item => item.rpm_cima[1]),
    getRpmBaixo:              () => data.map(item => item.rpm_baixo[1]),

    getVentiladorCima:        () => data.map(item => item.ventilador_cima_status[1]),
    getVentiladorBaixo:       () => data.map(item => item.ventilador_baixo_status[1]),
  };
}
