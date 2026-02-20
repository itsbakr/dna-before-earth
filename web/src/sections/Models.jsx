import { useMemo } from 'react'
import {
  ComposedChart, Line, Scatter, XAxis, YAxis, CartesianGrid,
  ReferenceLine, ResponsiveContainer, Tooltip, Label, Legend,
} from 'recharts'
import { SHAROV_DATA, LINEAR_MODEL, LOGISTIC_MODEL, MODEL_COMPARISON } from '../data'
import { useInView } from '../hooks/useInView'

function ModelTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const t = payload[0]?.payload?.t
  if (t == null) return null
  return (
    <div className="bg-white border border-border rounded-lg px-4 py-3 shadow-lg">
      <p className="text-xs text-text-tertiary mb-1">{t.toFixed(1)} Billion Years Ago</p>
      {payload.map((p, i) => (
        p.value != null && (
          <p key={i} className="text-xs" style={{ color: p.color }}>
            <span className="font-semibold">{p.name}:</span> {p.value.toFixed(2)}
          </p>
        )
      ))}
    </div>
  )
}

function DataPointLabel({ cx, cy, index }) {
  const names = ['Prokaryotes', 'Eukaryotes', 'Worms', 'Fish', 'Mammals']
  const offsets = [
    { dx: 10, dy: 16 },
    { dx: 10, dy: 14 },
    { dx: 10, dy: -10 },
    { dx: 10, dy: 12 },
    { dx: -16, dy: -12 },
  ]
  const o = offsets[index] || { dx: 0, dy: -12 }
  return (
    <text x={cx + o.dx} y={cy + o.dy} textAnchor="start" fontSize={9} fontWeight={500} fill="#9C9B97">
      {names[index]}
    </text>
  )
}

function CustomLegend() {
  return (
    <div className="flex items-center justify-center gap-6 mt-4 text-xs text-text-secondary">
      <span className="flex items-center gap-2">
        <svg width="24" height="2"><line x1="0" y1="1" x2="24" y2="1" stroke="#C4422B" strokeWidth="2.5" /></svg>
        Linear (origin: 9.8 Bya)
      </span>
      <span className="flex items-center gap-2">
        <svg width="24" height="2"><line x1="0" y1="1" x2="24" y2="1" stroke="#059669" strokeWidth="2.5" strokeDasharray="5 3" /></svg>
        Logistic (origin: 20.5 Bya)
      </span>
      <span className="flex items-center gap-2">
        <svg width="10" height="10"><circle cx="5" cy="5" r="4" fill="#C4422B" stroke="white" strokeWidth="1.5" /></svg>
        Data points
      </span>
    </div>
  )
}

export default function Models() {
  const [ref, visible] = useInView()

  const curveData = useMemo(() => {
    const data = []
    for (let t = -1; t <= 22; t += 0.15) {
      const lin = LINEAR_MODEL.intercept - LINEAR_MODEL.slope * t
      const log = LOGISTIC_MODEL.L / (1 + Math.exp(-LOGISTIC_MODEL.k * (-t - LOGISTIC_MODEL.t0)))
      data.push({
        t: parseFloat(t.toFixed(2)),
        linear: parseFloat(Math.max(lin, -1).toFixed(3)),
        logistic: parseFloat(Math.max(log, 0).toFixed(3)),
      })
    }
    return data
  }, [])

  const scatterData = SHAROV_DATA.map(d => ({ t: d.time, linear: d.logGenome }))

  return (
    <section id="models" ref={ref} className={`fade-section ${visible ? 'visible' : ''}`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">03 — Alternative Models</p>
        <h2 className="section-title">Does the curve shape matter?</h2>
        <p className="section-subtitle mb-10">
          Critics assumed a more "realistic" growth model would resolve the pre-Earth problem.
          We tested every alternative they suggested. The opposite happened.
        </p>

        <div className="chart-container mb-8">
          <div className="flex items-center justify-between mb-4 px-2">
            <h3 className="text-xs font-semibold text-text-primary uppercase tracking-wider">Linear vs Logistic Growth</h3>
            <span className="text-xs text-accent font-medium">Logistic makes it worse</span>
          </div>
          <ResponsiveContainer width="100%" height={420}>
            <ComposedChart data={curveData} margin={{ top: 10, right: 40, bottom: 45, left: 25 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#EDECE8" />
              <XAxis
                dataKey="t" type="number" domain={[0, 22]} reversed allowDataOverflow
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
                label={{ value: 'Earth', fill: '#2563EB', fontSize: 11, fontWeight: 500, position: 'insideTopRight', offset: 8 }}
              />
              <ReferenceLine
                x={13.8} stroke="#7C3AED" strokeDasharray="8 5" strokeWidth={1.5}
                label={{ value: 'Big Bang', fill: '#7C3AED', fontSize: 11, fontWeight: 500, position: 'insideTopRight', offset: 8 }}
              />
              <ReferenceLine y={0} stroke="#E8E6E1" strokeWidth={1} />
              <Tooltip content={<ModelTooltip />} cursor={{ stroke: '#E8E6E1', strokeWidth: 1 }} />
              <Line dataKey="linear" stroke="#C4422B" strokeWidth={2.5} dot={false} name="Linear" />
              <Line dataKey="logistic" stroke="#059669" strokeWidth={2.5} dot={false} name="Logistic" strokeDasharray="6 4" />
              <Scatter data={scatterData} dataKey="linear" fill="#C4422B"
                shape={({ cx, cy }) => <circle cx={cx} cy={cy} r={5.5} fill="#C4422B" stroke="#fff" strokeWidth={2.5} />}
                label={<DataPointLabel />}
              />
            </ComposedChart>
          </ResponsiveContainer>
          <CustomLegend />
        </div>

        <div className="grid sm:grid-cols-2 gap-4 mb-8">
          <div className="card border-l-4 border-l-accent">
            <h3 className="text-sm font-semibold text-accent mb-2">Linear (Exponential)</h3>
            <p className="font-mono text-xs text-text-tertiary mb-2">
              R² = 0.967 · AIC = −12.0 · 2 parameters
            </p>
            <p className="text-sm text-text-secondary leading-relaxed">
              Origin: <strong className="text-text-primary">9.8 Bya</strong>.
              Sharov's original model — clean, simple, fits the data well.
            </p>
          </div>
          <div className="card border-l-4 border-l-green">
            <h3 className="text-sm font-semibold text-green mb-2">Logistic (S-curve)</h3>
            <p className="font-mono text-xs text-text-tertiary mb-2">
              R² = 0.969 · AIC = −10.4 · 3 parameters
            </p>
            <p className="text-sm text-text-secondary leading-relaxed">
              Origin: <strong className="text-text-primary">20.5 Bya</strong>.
              Expected to help — actually pushes the origin <em>past the Big Bang</em>.
            </p>
          </div>
        </div>

        <div className="card overflow-x-auto">
          <h3 className="text-sm font-semibold text-text-primary mb-4">All models tested</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-border">
                <th className="text-left py-2 pr-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Model</th>
                <th className="text-right py-2 px-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">R²</th>
                <th className="text-right py-2 px-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Origin</th>
                <th className="text-right py-2 pl-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Verdict</th>
              </tr>
            </thead>
            <tbody>
              {MODEL_COMPARISON.map((m, i) => (
                <tr key={i} className="border-b border-border/50">
                  <td className="py-3 pr-4 text-text-primary font-medium">{m.name}</td>
                  <td className="py-3 px-4 text-right font-mono text-text-secondary">
                    {m.rSquared ?? '—'}
                  </td>
                  <td className="py-3 px-4 text-right font-mono font-semibold text-accent">{m.origin}</td>
                  <td className="py-3 pl-4 text-right text-text-secondary">{m.verdict}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  )
}
