import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  ReferenceLine, ReferenceArea, ResponsiveContainer, Cell, Tooltip, Label,
} from 'recharts'
import { MC_HISTOGRAM, MC_STATS, BOOT_STATS } from '../data'
import { useInView } from '../hooks/useInView'

function HistogramTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0]?.payload
  return (
    <div className="bg-white border border-border rounded-lg px-4 py-3 shadow-lg">
      <p className="text-xs text-text-tertiary">Origin estimate</p>
      <p className="text-sm font-semibold text-text-primary">{d.mid.toFixed(1)} Billion Years Ago</p>
      <p className="text-xs text-text-secondary mt-1">{d.count.toLocaleString()} of 10,000 simulations</p>
    </div>
  )
}

export default function MonteCarlo() {
  const [ref, visible] = useInView()

  return (
    <section id="monte-carlo" ref={ref} className={`fade-section ${visible ? 'visible' : ''} bg-surface`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">02 — Uncertainty</p>
        <h2 className="section-title">10,000 simulations. 100% pre-Earth.</h2>
        <p className="section-subtitle mb-10">
          We randomly perturbed every data point within its measurement uncertainty 10,000 times
          and re-ran the regression. Not a single simulation placed the origin within Earth's history.
        </p>

        <div className="chart-container mb-8">
          <div className="flex items-center justify-between mb-4 px-2">
            <h3 className="text-xs font-semibold text-text-primary uppercase tracking-wider">Monte Carlo Distribution</h3>
            <span className="text-xs font-mono text-text-tertiary">n = 10,000</span>
          </div>
          <ResponsiveContainer width="100%" height={360}>
            <BarChart data={MC_HISTOGRAM} margin={{ top: 10, right: 20, bottom: 45, left: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EDECE8" vertical={false} />
              <XAxis
                dataKey="bin"
                tick={{ fill: '#9C9B97', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
                stroke="#E8E6E1" tickLine={{ stroke: '#E8E6E1' }}
                interval={1}
              >
                <Label value="Predicted Origin (Billion Years Ago)" position="bottom" offset={25} style={{ fill: '#71706C', fontSize: 12 }} />
              </XAxis>
              <YAxis
                tick={{ fill: '#9C9B97', fontSize: 10, fontFamily: 'JetBrains Mono, monospace' }}
                stroke="#E8E6E1" tickLine={{ stroke: '#E8E6E1' }}
              >
                <Label value="Simulations" angle={-90} position="insideLeft" offset={-5} style={{ fill: '#71706C', fontSize: 12 }} />
              </YAxis>
              <ReferenceLine
                x="4.5" stroke="#2563EB" strokeDasharray="8 5" strokeWidth={1.5}
                label={{ value: 'Earth (4.5 Bya)', fill: '#2563EB', fontSize: 10, fontWeight: 500, position: 'insideTopRight', offset: 4 }}
              />
              <Tooltip content={<HistogramTooltip />} cursor={{ fill: '#E8E6E1', fillOpacity: 0.3 }} />
              <Bar dataKey="count" radius={[3, 3, 0, 0]} maxBarSize={36}>
                {MC_HISTOGRAM.map((entry, i) => {
                  const peak = 1804
                  const intensity = 0.5 + (entry.count / peak) * 0.5
                  return (
                    <Cell
                      key={i}
                      fill={entry.mid > 13.8 ? '#7C3AED' : '#C4422B'}
                      fillOpacity={Math.max(0.35, intensity * 0.9)}
                    />
                  )
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="flex items-center justify-center gap-8 mt-4 text-xs text-text-tertiary">
            <span className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-sm bg-accent/80 inline-block" />
              Simulation results
            </span>
            <span className="flex items-center gap-2">
              <span className="w-px h-3 inline-block border-l-2 border-dashed border-blue" />
              Earth's age (4.5 Bya)
            </span>
            <span className="flex items-center gap-2">
              <span className="text-xs font-mono text-accent font-semibold">← gap →</span>
              No simulations in Earth range
            </span>
          </div>
        </div>

        <div className="bg-accent-light border border-accent/10 rounded-xl px-5 py-4 mb-8 flex items-start gap-3">
          <span className="text-accent text-lg leading-none mt-0.5">*</span>
          <p className="text-sm text-text-secondary leading-relaxed">
            The lowest estimate across all 10,000 simulations was <strong className="text-accent font-mono">7.7 Bya</strong> — still
            3.2 billion years before Earth formed. The entire distribution sits to the right of Earth's age.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <div className="card text-center">
            <p className="stat-value text-accent">100%</p>
            <p className="stat-label">Pre-Earth</p>
          </div>
          <div className="card text-center">
            <p className="stat-value text-blue">7.7–12.8</p>
            <p className="stat-label">95% CI (Bya)</p>
          </div>
          <div className="card text-center">
            <p className="stat-value text-green">{MC_STATS.median}</p>
            <p className="stat-label">Median (Bya)</p>
          </div>
          <div className="card text-center">
            <p className="stat-value text-gold">±{MC_STATS.std}</p>
            <p className="stat-label">Std deviation</p>
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <div className="card">
            <h3 className="text-sm font-semibold text-text-primary mb-2">Monte Carlo</h3>
            <p className="text-sm text-text-secondary leading-relaxed">
              Each data point has measurement uncertainty — prokaryote origins could be 3.2–3.8 Bya,
              genome size estimates involve judgment calls. We perturbed everything within these ranges.
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-semibold text-text-primary mb-2">Bootstrap confirms</h3>
            <p className="text-sm text-text-secondary leading-relaxed">
              A separate bootstrap resampling (10,000 iterations, sampling with replacement) yielded
              consistent results: mean origin {BOOT_STATS.mean} Bya, 95% CI [{BOOT_STATS.ciLow}, {BOOT_STATS.ciHigh}] Bya,
              with <strong className="text-text-primary">100% of samples predating Earth</strong>.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
