export const SHAROV_DATA = [
  { name: 'Prokaryotes', time: 3.5, logGenome: 5.70, genomeBp: 500_000, timeErr: 0.3, genomeErr: 0.3 },
  { name: 'Eukaryotes', time: 2.0, logGenome: 6.46, genomeBp: 2_900_000, timeErr: 0.25, genomeErr: 0.3 },
  { name: 'Worms', time: 1.0, logGenome: 7.86, genomeBp: 73_000_000, timeErr: 0.15, genomeErr: 0.15 },
  { name: 'Fish', time: 0.5, logGenome: 8.11, genomeBp: 130_000_000, timeErr: 0.05, genomeErr: 0.15 },
  { name: 'Mammals', time: 0.0, logGenome: 8.68, genomeBp: 480_000_000, timeErr: 0.0, genomeErr: 0.1 },
]

export const MARKOV_DATA = [
  { group: 'Bacteria', time: 4.0, logBp: 6.11, species: 'Pelagibacter ubique', genomeMb: 1.3 },
  { group: 'Eukaryotes', time: 2.0, logBp: 6.96, species: 'Ashbya gossypii', genomeMb: 9.2 },
  { group: 'Animals', time: 1.25, logBp: 7.29, species: 'Pratylenchus coffeae', genomeMb: 19.6 },
  { group: 'Chordates', time: 0.575, logBp: 7.84, species: 'Oikopleura dioica', genomeMb: 68.6 },
  { group: 'Vertebrates', time: 0.54, logBp: 8.53, species: 'Tetraodon fluviatilis', genomeMb: 342 },
  { group: 'Tetrapods', time: 0.375, logBp: 8.97, species: 'Limnodynastes ornatus', genomeMb: 931 },
  { group: 'Amniotes', time: 0.315, logBp: 8.98, species: 'Phasianus colchicus', genomeMb: 951 },
  { group: 'Mammals', time: 0.22, logBp: 9.23, species: 'Miniopterus schreibersi', genomeMb: 1695 },
  { group: 'Primates', time: 0.065, logBp: 9.35, species: 'Callicebus torquatus', genomeMb: 2215 },
]

export const ADDITIONAL_TAXA = [
  { name: 'Cyanobacteria', time: 2.7, logBp: 6.16, genomeMb: 1.44, source: 'Prochlorococcus marinus' },
  { name: 'Red algae', time: 1.6, logBp: 7.14, genomeMb: 13.7, source: 'Cyanidioschyzon merolae' },
  { name: 'Fungi', time: 1.0, logBp: 6.96, genomeMb: 9.2, source: 'Ashbya gossypii' },
  { name: 'Land plants', time: 0.47, logBp: 7.91, genomeMb: 82, source: 'Genlisea tuberosa' },
  { name: 'Insects', time: 0.4, logBp: 8.00, genomeMb: 99, source: 'Belgica antarctica' },
  { name: 'Flowering plants', time: 0.14, logBp: 7.80, genomeMb: 63, source: 'Utricularia gibba' },
]

export const LINEAR_MODEL = {
  slope: 0.877,
  intercept: 8.592,
  rSquared: 0.967,
  pValue: 0.0026,
  originBya: 9.8,
  doublingTimeMyr: 343,
  foldPerByr: 7.5,
  aic: -12.0,
}

export const LOGISTIC_MODEL = {
  L: 15.0,
  k: 0.239,
  t0: -1.237,
  rSquared: 0.969,
  originBya: 20.5,
  aic: -10.4,
}

export const MC_STATS = {
  nSimulations: 10_000,
  mean: 10.0,
  median: 9.9,
  std: 1.3,
  ciLow: 7.7,
  ciHigh: 12.8,
  pctPreEarth: 100.0,
  pctPreUniverse: 0.68,
}

export const BOOT_STATS = {
  nSamples: 10_000,
  mean: 9.57,
  ciLow: 7.67,
  ciHigh: 10.85,
  pctPreEarth: 100.0,
}

export const MC_HISTOGRAM = [
  { bin: '4.0', count: 0, mid: 4.0 },
  { bin: '4.5', count: 0, mid: 4.5 },
  { bin: '5.1', count: 0, mid: 5.1 },
  { bin: '5.7', count: 1, mid: 5.7 },
  { bin: '6.3', count: 4, mid: 6.3 },
  { bin: '6.9', count: 49, mid: 6.9 },
  { bin: '7.5', count: 252, mid: 7.5 },
  { bin: '8.1', count: 670, mid: 8.1 },
  { bin: '8.7', count: 1304, mid: 8.7 },
  { bin: '9.3', count: 1804, mid: 9.3 },
  { bin: '9.9', count: 1800, mid: 9.9 },
  { bin: '10.5', count: 1574, mid: 10.5 },
  { bin: '11.1', count: 1144, mid: 11.1 },
  { bin: '11.7', count: 721, mid: 11.7 },
  { bin: '12.3', count: 363, mid: 12.3 },
  { bin: '12.9', count: 172, mid: 12.9 },
  { bin: '13.5', count: 74, mid: 13.5 },
  { bin: '14.1', count: 37, mid: 14.1 },
  { bin: '14.7', count: 18, mid: 14.7 },
  { bin: '15.3', count: 10, mid: 15.3 },
  { bin: '15.9', count: 1, mid: 15.9 },
  { bin: '16.5', count: 1, mid: 16.5 },
]

export const THRESHOLDS = [
  { name: '1 bp — single nucleotide', logBp: 0, origin: 9.79, fitsEarth: false },
  { name: '100 bp — minimal replicator', logBp: 2, origin: 7.51, fitsEarth: false },
  { name: '200 bp — ribozyme', logBp: 2.3, origin: 7.17, fitsEarth: false },
  { name: '1,000 bp — single gene', logBp: 3, origin: 6.37, fitsEarth: false },
  { name: '10⁵ bp — parasitic minimum', logBp: 5, origin: 4.09, fitsEarth: true },
  { name: '3×10⁵ bp — free-living minimum', logBp: 5.5, origin: 3.55, fitsEarth: true },
  { name: '6×10⁵ bp — LUCA (low estimate)', logBp: 5.8, origin: 3.21, fitsEarth: true },
  { name: '10⁶ bp — LUCA (high estimate)', logBp: 6, origin: 2.95, fitsEarth: true },
]

export const INFO_DATA = [
  { name: '100 bp replicator', logProb: -60, color: '#D97706' },
  { name: '1,000 bp gene', logProb: -602, color: '#2563EB' },
  { name: '100,000 bp parasitic', logProb: -60_206, color: '#7C3AED' },
  { name: '300,000 bp free-living', logProb: -180_618, color: '#C4422B' },
  { name: '500,000 bp prokaryote', logProb: -301_030, color: '#BE185D' },
]

export const DATASET_COMPARISON = [
  { name: 'Sharov (2006)', points: 5, rSquared: 0.967, pValue: 0.003, origin: 9.8 },
  { name: 'Markov (2010)', points: 9, rSquared: 0.914, pValue: 0.0006, origin: 10.9 },
  { name: 'Extended (this study)', points: 14, rSquared: 0.713, pValue: 0.0001, origin: 11.2 },
]

export const MODEL_COMPARISON = [
  { name: 'Linear (Sharov)', rSquared: 0.967, origin: '9.8 Bya', params: 2, aic: -12.0, verdict: 'Pre-Earth' },
  { name: 'Logistic (S-curve)', rSquared: 0.969, origin: '20.5 Bya', params: 3, aic: -10.4, verdict: 'Much worse' },
  { name: 'Quadratic', rSquared: 0.981, origin: 'No root', params: 3, aic: null, verdict: 'Never reaches zero' },
  { name: 'Hyperexponential', rSquared: 0.979, origin: '>10 Bya', params: 3, aic: null, verdict: 'Worse' },
  { name: '3× faster early rate', rSquared: null, origin: '5.7 Bya', params: null, aic: null, verdict: 'Still pre-Earth' },
]

export function generateLinearCurve() {
  const data = []
  for (let t = -1; t <= 11; t += 0.1) {
    data.push({
      t: parseFloat(t.toFixed(1)),
      linear: parseFloat((LINEAR_MODEL.intercept - LINEAR_MODEL.slope * t).toFixed(3)),
    })
  }
  return data
}

export function generateLogisticCurve() {
  const data = []
  for (let t = -1; t <= 22; t += 0.1) {
    const val = LOGISTIC_MODEL.L / (1 + Math.exp(-LOGISTIC_MODEL.k * (-t - LOGISTIC_MODEL.t0)))
    data.push({
      t: parseFloat(t.toFixed(1)),
      logistic: parseFloat(Math.max(val, 0).toFixed(3)),
    })
  }
  return data
}

export function generateRegressionLine() {
  const data = []
  for (let t = 0; t <= 10.5; t += 0.2) {
    data.push({
      x: parseFloat(t.toFixed(1)),
      y: parseFloat((LINEAR_MODEL.intercept - LINEAR_MODEL.slope * t).toFixed(3)),
    })
  }
  return data
}
