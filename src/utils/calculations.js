// موتور محاسباتی شبیه‌سازی
export class SimulationEngine {
  constructor(config, option) {
    this.config = config;
    this.option = option;
  }

  // محاسبه AML (حداکثر بارگذاری وقتی اسید آزاد صفر است)
  calculateAML(v_v_percent) {
    if (v_v_percent <= 0) {
      return 0;
    }
    return 0.4108 * Math.pow(v_v_percent, 1.1);
  }

  // محاسبه ML (حداکثر بارگذاری)
  calculateML(PLS_Ac, PLS_Cu, v_v_percent, AML) {
    if (v_v_percent <= 0 || AML <= 0) {
      return 0;
    }
    const term1 = Math.pow(PLS_Ac, 2) / PLS_Cu;
    const term2 = (-28.511 * Math.pow(v_v_percent, -1.746) * AML + 
                  11.711 * Math.pow(v_v_percent, -0.646)) * 
                  Math.pow(3.303 * v_v_percent - 3.0842 * AML, 2) / AML;
    return term1 - term2;
  }

  // محاسبه بازیابی استخراج
  calculateExtractionRecovery(PLS_Cu, raffinate_Cu) {
    return ((PLS_Cu - raffinate_Cu) / PLS_Cu) * 100;
  }

  // محاسبه بازیابی stripping
  calculateStrippingRecovery(loaded_organic, stripped_organic) {
    return ((loaded_organic - stripped_organic) / loaded_organic) * 100;
  }

  // محاسبه انتقال خالص
  calculateNetTransfer(loaded_organic, stripped_organic, v_v_percent) {
    return (loaded_organic - stripped_organic) / v_v_percent;
  }

  // شبیه‌سازی Option 1
  simulateOption1(parameters) {
    const {
      PLS_flow,
      PLS_Cu,
      PLS_Ac,
      SR,
      Ratio_O_A_Ext,
      Mef1e,
      Mef2e,
      SP_Cu,
      SPAc,
      AD_Cu,
      Mef1s
    } = parameters;

    // محاسبات ساده‌شده برای نمایش
    const AML = this.calculateAML(parameters.v_v_percent);
    const ML = this.calculateML(PLS_Ac, PLS_Cu, parameters.v_v_percent, AML);
    const loaded_organic = ML * SR / 100;
    
    // محاسبات فرضی برای raffinate
    const raffinate_Cu = PLS_Cu * (1 - Mef1e/100) * (1 - Mef2e/100);
    const raffinate_Ac = PLS_Ac + (PLS_Cu - raffinate_Cu) * 1.54;
    
    const extraction_recovery = this.calculateExtractionRecovery(PLS_Cu, raffinate_Cu);
    
    // محاسبات stripping
    const stripped_organic = loaded_organic * 0.4; // مقدار فرضی
    const stripping_recovery = this.calculateStrippingRecovery(loaded_organic, stripped_organic);
    const net_transfer = this.calculateNetTransfer(loaded_organic, stripped_organic, parameters.v_v_percent);

    return {
      optimum_v_v_percent: parameters.v_v_percent,
      AML: AML,
      ML: ML,
      loaded_organic: loaded_organic,
      raffinate_Cu: raffinate_Cu,
      raffinate_Ac: raffinate_Ac,
      extraction_recovery: extraction_recovery,
      stripping_recovery: stripping_recovery,
      net_transfer: net_transfer,
      organic_flow: PLS_flow * Ratio_O_A_Ext
    };
  }

  // شبیه‌سازی Option 2
  simulateOption2(parameters) {
    // پیاده‌سازی مشابه Option 1 با پارامترهای مختلف
    const results = this.simulateOption1(parameters);
    
    // محاسبات اضافی برای Option 2
    results.saturation_ratio = results.ML > 0 ? (results.loaded_organic / results.ML) * 100 : 0;
    results.mixer_efficiency_E1 = parameters.Mef1e;
    results.mixer_efficiency_E2 = parameters.Mef2e;

    return results;
  }

  // تولید داده برای نمودار
  generateChartData(results, parameters) {
    const data = [];
    
    for (let i = 0; i <= 100; i += 10) {
      const v_v = i;
      const AML = this.calculateAML(v_v);
      const ML = this.calculateML(parameters.PLS_Ac, parameters.PLS_Cu, v_v, AML);
      
      data.push({
        v_v_percent: v_v,
        AML: AML,
        ML: ML,
        loaded_organic: ML * parameters.SR / 100,
        extraction_efficiency: Math.min(95, 80 + v_v * 0.15)
      });
    }
    
    return data;
  }
}