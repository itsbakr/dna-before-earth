import { THRESHOLDS } from '../data'
import { useInView } from '../hooks/useInView'

export default function Thresholds() {
  const [ref, visible] = useInView()

  return (
    <section id="thresholds" ref={ref} className={`fade-section ${visible ? 'visible' : ''} bg-surface`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">04 — Thresholds</p>
        <h2 className="section-title">What if life didn't start from zero?</h2>
        <p className="section-subtitle mb-10">
          Instead of extrapolating to 1 base pair, what if life requires a minimum complexity to begin?
          We tested every plausible threshold. Most still predate Earth.
        </p>

        <div className="card overflow-x-auto mb-8">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-border">
                <th className="text-left py-3 pr-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Starting complexity</th>
                <th className="text-right py-3 px-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Size (log₁₀ bp)</th>
                <th className="text-right py-3 px-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Predicted origin</th>
                <th className="text-center py-3 pl-4 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Fits Earth?</th>
              </tr>
            </thead>
            <tbody>
              {THRESHOLDS.map((t, i) => (
                <tr key={i} className={`border-b border-border/50 ${t.fitsEarth ? 'bg-green-light/50' : ''}`}>
                  <td className="py-3.5 pr-4 text-text-primary">{t.name}</td>
                  <td className="py-3.5 px-4 text-right font-mono text-text-secondary">{t.logBp}</td>
                  <td className={`py-3.5 px-4 text-right font-mono font-semibold ${t.fitsEarth ? 'text-green' : 'text-accent'}`}>
                    {t.origin.toFixed(1)} Bya
                  </td>
                  <td className="py-3.5 pl-4 text-center">
                    <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                      t.fitsEarth
                        ? 'bg-green-light text-green'
                        : 'bg-accent-light text-accent'
                    }`}>
                      {t.fitsEarth ? 'Yes' : 'No'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card border-l-4 border-l-accent">
          <h3 className="text-sm font-semibold text-text-primary mb-3">The threshold dilemma</h3>
          <p className="text-sm text-text-secondary leading-relaxed">
            To place the origin within Earth's history, life must have started at a minimum
            of ~100,000 base pairs — roughly 100 genes functioning together. Anything simpler,
            even a minimal self-replicating RNA molecule, still predates Earth. This creates a dilemma:
            either life began elsewhere and arrived already complex, or a massive jump in organized
            complexity occurred spontaneously — with probability approximately <strong className="text-accent font-mono">10⁻⁶⁰,⁰⁰⁰</strong>.
          </p>
        </div>
      </div>
    </section>
  )
}
