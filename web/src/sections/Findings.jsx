import { useInView } from '../hooks/useInView'

const findings = [
  {
    n: '01',
    title: 'The exponential trend is real and robust',
    body: 'R² = 0.967, p = 0.003. Monte Carlo (100% pre-Earth across 10,000 simulations) and bootstrap analysis both confirm this is not an artifact of small sample size or data uncertainty.',
    color: 'accent',
  },
  {
    n: '02',
    title: 'Alternative models do not resolve the problem',
    body: 'The logistic model pushes the origin to 20.5 Bya. The quadratic model has no valid root. The hyperexponential model gives >10 Bya. Every alternative makes the finding stronger or is indeterminate.',
    color: 'blue',
  },
  {
    n: '03',
    title: 'Only a discontinuous threshold resolves terrestrial origin',
    body: 'To place life\'s origin within Earth\'s history, one must assume life started at ~100,000+ bp — a massive jump from non-life to organized complexity with no intermediate stages.',
    color: 'green',
  },
  {
    n: '04',
    title: 'The probability of such a threshold is astronomically low',
    body: 'Random assembly of 300,000 bp has probability 10⁻¹⁸⁰,⁶¹⁸. This exceeds the universal probability bound by over 180,000 orders of magnitude.',
    color: 'gold',
  },
  {
    n: '05',
    title: 'Every pathway leads to an open question',
    body: 'Whether panspermia, an undiscovered rapid-assembly mechanism, or something beyond current frameworks — the data reveals a genuine gap in our understanding that has been insufficiently acknowledged for two decades.',
    color: 'purple',
  },
]

const colorMap = {
  accent: { border: 'border-l-accent', text: 'text-accent', bg: 'bg-accent-light' },
  blue: { border: 'border-l-blue', text: 'text-blue', bg: 'bg-blue-light' },
  green: { border: 'border-l-green', text: 'text-green', bg: 'bg-green-light' },
  gold: { border: 'border-l-gold', text: 'text-gold', bg: 'bg-gold-light' },
  purple: { border: 'border-l-purple', text: 'text-purple', bg: 'bg-purple-light' },
}

export default function Findings() {
  const [ref, visible] = useInView()

  return (
    <section id="findings" ref={ref} className={`fade-section ${visible ? 'visible' : ''}`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">07 — Findings</p>
        <h2 className="section-title">What the data shows</h2>
        <p className="section-subtitle mb-10">
          Five consolidated findings from our systematic replication and stress-testing of the genome complexity clock.
        </p>

        <div className="space-y-4 mb-10">
          {findings.map((f, i) => {
            const c = colorMap[f.color]
            return (
              <div key={i} className={`card border-l-4 ${c.border} flex gap-5`}>
                <div className={`text-2xl font-mono font-bold ${c.text} shrink-0 w-8`}>{f.n}</div>
                <div>
                  <h3 className="text-sm font-semibold text-text-primary mb-1.5">{f.title}</h3>
                  <p className="text-sm text-text-secondary leading-relaxed">{f.body}</p>
                </div>
              </div>
            )
          })}
        </div>

        <div className="card bg-cream">
          <h3 className="text-sm font-semibold text-text-primary mb-3">Methodological note</h3>
          <p className="text-sm text-text-secondary leading-relaxed">
            This analysis deliberately tested assumptions favorable to a terrestrial origin — slower early rates,
            logistic growth, minimum thresholds. In every case except the threshold hypothesis, the data resisted
            a purely Earth-bound explanation. The data comes from the same databases every evolutionary biologist
            uses daily. The fossil dates are standard paleontological consensus. The methods are standard
            quantitative biology.
          </p>
        </div>
      </div>
    </section>
  )
}
