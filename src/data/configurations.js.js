export const CONFIGURATIONS = {
  A: { name: 'Series 2Ex1S', description: 'سری 2 استخراج‌گر و 1 جداکننده' },
  B: { name: 'Series 2Ex2S', description: 'سری 2 استخراج‌گر و 2 جداکننده' },
  C: { name: 'Series 3Ex1S', description: 'سری 3 استخراج‌گر و 1 جداکننده' },
  D: { name: 'Series 3Ex2S', description: 'سری 3 استخراج‌گر و 2 جداکننده' },
  E: { name: 'Series parallel 2Ex1Px1S', description: 'سری موازی 2 استخراج‌گر' },
  F: { name: 'Series parallel 2Ex1Px2S', description: 'سری موازی 2 استخراج‌گر و 2 جداکننده' },
  G: { name: 'Optimum series parallel 1Ex1Px1Ex1S', description: 'سری موازی بهینه' },
  H: { name: 'Optimum series parallel 1Ex1Px1Ex2S', description: 'سری موازی بهینه با 2 جداکننده' },
  I: { name: 'Triple parallel 1Ex1Px1Px1S', description: 'موازی سه‌گانه' },
  J: { name: 'Triple parallel 1Ex1Px1Px2S', description: 'موازی سه‌گانه با 2 جداکننده' },
  K: { name: 'Interlaced 1Ex1Px1Ex1Px1S', description: 'درهم‌تنیده' },
  L: { name: 'Interlaced 1Ex1Px1Ex1Px2S', description: 'درهم‌تنیده با 2 جداکننده' },
  M: { name: 'Double series parallel 2Ex2Px1S', description: 'سری موازی دوگانه' },
  N: { name: 'Double series parallel 2Ex2Px2S', description: 'سری موازی دوگانه با 2 جداکننده' },
  O: { name: 'Optimum triple parallel 1Ex1Px1Px1Ex1S', description: 'موازی سه‌گانه بهینه' },
  P: { name: 'Optimum triple parallel 1Ex1Px1Px1Ex2S', description: 'موازی سه‌گانه بهینه با 2 جداکننده' },
  Q: { name: 'Organic by pass 2Ex2Px1S', description: 'گذرگاه آلی' },
  R: { name: 'Organic by pass 2Ex2Px2S', description: 'گذرگاه آلی با 2 جداکننده' }
};

export const EXTRACTANTS = {
  Lix984N: {
    name: 'Lix984N',
    properties: {
      density: 0.89,
      molecularWeight: 360
    }
  }
};

export const DEFAULT_PARAMETERS = {
  PLS_flow: 400,
  PLS_Cu: 2.5,
  PLS_Ac: 1.6,
  SR: 92,
  Ratio_O_A_Ext: 1,
  Mef1e: 92,
  Mef2e: 95,
  SP_Cu: 30,
  SPAc: 190,
  AD_Cu: 50,
  Mef1s: 98,
  v_v_percent: 8.66
};