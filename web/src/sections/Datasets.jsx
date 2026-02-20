import { DATASET_COMPARISON } from '../data'
import { useInView } from '../hooks/useInView'

export default function Datasets() {
  const [ref, visible] = useInView()

  return (
    <section id="datasets" ref={ref} className={`fade-section ${visible ? 'visible' : ''} bg-surface`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">06 — Expanded Data</p>
        <h2 className="section-title">More data makes it stronger</h2>
        <p className="section-subtitle mb-10">
          We expanded from 5 to 9 to 14 data points using independent sources and more conservative estimates.
          Each expansion moved the predicted origin <em>further</em> from Earth's age, not closer.
        </p>

        <div className="grid sm:grid-cols-3 gap-5 mb-10">
          {DATASET_COMPARISON.map((d, i) => (
            <div key={i} className="card relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-16 h-16 opacity-5">
                <span className="text-6xl font-bold text-accent">{d.points}</span>
              </div>
              <p className="text-xs font-medium text-text-tertiary uppercase tracking-wider mb-4">{d.name}</p>
              <div className="space-y-3">
                <div>
                  <p className="text-3xl font-mono font-bold text-accent">{d.origin} <span className="text-lg">Bya</span></p>
                  <p className="text-xs text-text-tertiary">Predicted origin</p>
                </div>
                <div className="flex gap-4">
                  <div>
                    <p className="text-sm font-mono font-semibold text-text-primary">{d.rSquared}</p>
                    <p className="text-2xs text-text-tertiary">R²</p>
                  </div>
                  <div>
                    <p className="text-sm font-mono font-semibold text-text-primary">{d.pValue}</p>
                    <p className="text-2xs text-text-tertiary">p-value</p>
                  </div>
                  <div>
                    <p className="text-sm font-mono font-semibold text-text-primary">{d.points}</p>
                    <p className="text-2xs text-text-tertiary">points</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="relative">
          <div className="flex items-center justify-between mb-4">
            {DATASET_COMPARISON.map((d, i) => (
              <div key={i} className="text-center flex-1">
                <p className="text-2xl font-mono font-bold text-accent">{d.origin}</p>
                <p className="text-xs text-text-tertiary">{d.points} points</p>
              </div>
            ))}
          </div>
          <div className="relative h-2 bg-cream rounded-full overflow-hidden">
            <div className="absolute inset-y-0 left-0 bg-accent/20 rounded-full" style={{ width: '100%' }} />
            {DATASET_COMPARISON.map((d, i) => (
              <div
                key={i}
                className="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-accent rounded-full border-2 border-white shadow-sm"
                style={{ left: `${((d.origin - 9) / 3) * 100}%` }}
              />
            ))}
          </div>
          <div className="flex justify-between mt-2 text-2xs text-text-tertiary font-mono">
            <span>9.0 Bya</span>
            <span>Earth (4.5 Bya) ←</span>
            <span>12.0 Bya</span>
          </div>
        </div>

        <div className="card mt-8">
          <p className="text-sm text-text-secondary leading-relaxed">
            Markov et al. (2010) independently expanded the dataset using <strong className="text-text-primary">more
            conservative</strong> estimates — free-living organisms only, not parasites — and obtained a
            stronger result. Our 14-point extended dataset adds 6 additional taxa from standard genomic
            databases. The progression is clear: more data strengthens the finding, not weakens it.
          </p>
        </div>
      </div>
    </section>
  )
}
