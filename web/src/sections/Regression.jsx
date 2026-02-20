import { useMemo } from 'react'
import {
  ComposedChart, Line, Scatter, XAxis, YAxis, CartesianGrid,
  ReferenceLine, ReferenceArea, ResponsiveContainer, Tooltip, Label,
} from 'recharts'
import { SHAROV_DATA, LINEAR_MODEL, generateRegressionLine } from '../data'
import { useInView } from '../hooks/useInView'

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0]?.payload
  if (!d?.name) return null
  return (
    <div className="bg-white border border-border rounded-lg px-4 py-3 shadow-lg">
      <p className="text-sm font-semibold text-text-primary">{d.name}</p>
      <div className="flex gap-4 mt-1">
        <p className="text-xs text-text-secondary"><span className="text-text-tertiary">Time:</span> {d.x} Bya</p>
        <p className="text-xs text-text-secondary"><span className="text-text-tertiary">log₁₀:</span> {d.y.toFixed(2)}</p>
      </div>
    </div>
  )
}

function PointLabel({ cx, cy, value, index }) {
  const names = ['Prokaryotes', 'Eukaryotes', 'Worms', 'Fish', 'Mammals']
  const offsets = [
    { dx: 0, dy: 18 },
    { dx: -10, dy: -14 },
    { dx: 0, dy: -14 },
    { dx: 0, dy: 14 },
    { dx: -20, dy: -14 },
  ]
  const o = offsets[index] || { dx: 0, dy: -14 }
  return (
    <text x={cx + o.dx} y={cy + o.dy} textAnchor="middle" fontSize={10} fontWeight={500} fill="#71706C">
      {names[index]}
    </text>
  )
}

export default function Regression() {
  const [ref, visible] = useInView()
  const regLine = useMemo(() => generateRegressionLine(), [])
  const scatterData = SHAROV_DATA.map(d => ({ x: d.time, y: d.logGenome, name: d.name }))

  return (
    <section id="regression" ref={ref} className={`fade-section ${visible ? 'visible' : ''}`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">01 — The Trend</p>
        <h2 className="section-title">The exponential trend is real</h2>
        <p className="section-subtitle mb-10">
          Plotting maximum genome complexity against geological time reveals a remarkably clean exponential
          relationship spanning 3.5 billion years. The regression is statistically significant with only 5 data points.
        </p>

        <div className="chart-container mb-6">
          <div className="flex items-center justify-between mb-4 px-2">
            <h3 className="text-xs font-semibold text-text-primary uppercase tracking-wider">Genome Complexity vs Time</h3>
            <span className="text-xs font-mono text-text-tertiary">R² = {LINEAR_MODEL.rSquared}</span>
          </div>
          <ResponsiveContainer width="100%" height={420}>
            <ComposedChart margin={{ top: 10, right: 40, bottom: 45, left: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EDECE8" />
              <ReferenceArea x1={0} x2={4.5} fill="#2563EB" fillOpacity={0.03} />
              <XAxis
                dataKey="x" type="number" domain={[0, 10.5]} reversed allowDataOverflow
                tick={{ fill: '#9C9B97', fontSize: 11, fontFamily: 'JetBrains Mono, monospace' }}
                stroke="#E8E6E1" tickLine={{ stroke: '#E8E6E1' }}
              >
                <Label value="Billions of Years Ago" position="bottom" offset={25} style={{ fill: '#71706C', fontSize: 12 }} />
              </XAxis>
              <YAxis
                domain={[0, 10]} allowDataOverflow
                tick={{ fill: '#9C9B97', fontSize: 11, fontFamily: 'JetBrains Mono, monospace' }}
                stroke="#E8E6E1" tickLine={{ stroke: '#E8E6E1' }}
              >
                <Label value="log₁₀(genome size, bp)" angle={-90} position="insideLeft" offset={-5} style={{ fill: '#71706C', fontSize: 12 }} />
              </YAxis>
              <ReferenceLine
                x={4.5} stroke="#2563EB" strokeDasharray="8 5" strokeWidth={1.5}
                label={{ value: 'Earth forms (4.5 Bya)', fill: '#2563EB', fontSize: 11, fontWeight: 500, position: 'insideTopRight', offset: 8 }}
              />
              <ReferenceLine
                x={9.8} stroke="#C4422B" strokeDasharray="4 4" strokeWidth={1} strokeOpacity={0.4}
                label={{ value: 'DNA Origin (9.8 Bya)', fill: '#C4422B', fontSize: 9, position: 'insideBottomRight', offset: 4 }}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ stroke: '#E8E6E1', strokeWidth: 1 }} />
              <Line data={regLine} dataKey="y" stroke="#C4422B" strokeWidth={2.5} dot={false} opacity={0.6} />
              <Scatter
                data={scatterData} dataKey="y" fill="#C4422B"
                shape={({ cx, cy }) => (
                  <circle cx={cx} cy={cy} r={6} fill="#C4422B" stroke="#fff" strokeWidth={2.5} />
                )}
                label={<PointLabel />}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        <div className="font-mono text-xs text-text-secondary bg-cream border border-border rounded-lg px-5 py-3 mb-8 flex flex-wrap gap-x-6 gap-y-1">
          <span>log₁₀(genome) = {LINEAR_MODEL.intercept} − {LINEAR_MODEL.slope} × t</span>
          <span className="text-text-tertiary">|</span>
          <span>R² = {LINEAR_MODEL.rSquared}</span>
          <span className="text-text-tertiary">|</span>
          <span>p = {LINEAR_MODEL.pValue}</span>
          <span className="text-text-tertiary">|</span>
          <span>Origin = 9.8 Bya</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <StatCard value="0.967" label="R-squared" sublabel="Goodness of fit" color="accent" />
          <StatCard value="343 Myr" label="Doubling time" sublabel="Per order of magnitude" color="blue" />
          <StatCard value="7.5×" label="Fold per Byr" sublabel="Growth rate" color="green" />
          <StatCard value="9.8 Bya" label="Extrapolated origin" sublabel="Before Earth formed" color="accent" />
        </div>

        <div className="card mt-8">
          <p className="text-sm text-text-secondary leading-relaxed">
            We replicated Sharov's (2006) regression exactly. The fit is remarkably strong for only 5 data points
            spanning 3.5 billion years. The p-value of 0.0026 indicates this trend is statistically significant.
            Extrapolating backward, genome complexity reaches zero at <strong className="text-text-primary">9.8 billion
            years ago</strong> — more than twice the age of Earth.
          </p>
        </div>
      </div>
    </section>
  )
}

function StatCard({ value, label, sublabel, color }) {
  const colors = {
    accent: 'text-accent',
    blue: 'text-blue',
    green: 'text-green',
    gold: 'text-gold',
    purple: 'text-purple',
  }

  return (
    <div className="card text-center">
      <p className={`stat-value ${colors[color] || 'text-accent'}`}>{value}</p>
      <p className="stat-label">{label}</p>
      {sublabel && <p className="text-2xs text-text-tertiary mt-0.5">{sublabel}</p>}
    </div>
  )
}
