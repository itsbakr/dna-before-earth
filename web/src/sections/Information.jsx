import { INFO_DATA } from '../data'
import { useInView } from '../hooks/useInView'

export default function Information() {
  const [ref, visible] = useInView()

  const maxLog = 301_030

  return (
    <section id="information" ref={ref} className={`fade-section ${visible ? 'visible' : ''}`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-20 sm:py-28">
        <p className="section-label">05 — Information Theory</p>
        <h2 className="section-title">The probability gap</h2>
        <p className="section-subtitle mb-10">
          How likely is it that a functional genome of a given size could assemble randomly?
          The numbers reveal a gap so vast it transcends any meaningful physical comparison.
        </p>

        <div className="grid sm:grid-cols-3 gap-4 mb-10">
          <div className="card text-center">
            <p className="text-xs font-medium text-text-tertiary uppercase tracking-wider mb-1">Atoms in universe</p>
            <p className="text-3xl font-mono font-bold text-blue">10<sup>80</sup></p>
          </div>
          <div className="card text-center">
            <p className="text-xs font-medium text-text-tertiary uppercase tracking-wider mb-1">Minimal genome assembly</p>
            <p className="text-3xl font-mono font-bold text-accent">10<sup>-180,618</sup></p>
          </div>
          <div className="card text-center">
            <p className="text-xs font-medium text-text-tertiary uppercase tracking-wider mb-1">Gap</p>
            <p className="text-3xl font-mono font-bold text-gold">180,698</p>
            <p className="text-xs text-text-tertiary">orders of magnitude</p>
          </div>
        </div>

        <div className="card mb-8">
          <h3 className="text-xs font-semibold text-text-primary uppercase tracking-wider mb-5">Probability of random assembly</h3>
          <div className="space-y-4">
            {INFO_DATA.map((d, i) => (
              <div key={i}>
                <div className="flex items-baseline justify-between mb-1.5">
                  <span className="text-xs font-medium text-text-primary">{d.name}</span>
                  <span className="text-xs font-mono font-bold" style={{ color: d.color }}>
                    10<sup>{d.logProb.toLocaleString()}</sup>
                  </span>
                </div>
                <div className="relative h-3 bg-cream rounded-full overflow-hidden">
                  <div
                    className="absolute inset-y-0 left-0 rounded-full transition-all duration-1000"
                    style={{
                      width: `${Math.max(1.5, (Math.abs(d.logProb) / maxLog) * 100)}%`,
                      backgroundColor: d.color,
                      opacity: 0.35,
                    }}
                  />
                  <div
                    className="absolute inset-y-0 left-0 rounded-full"
                    style={{
                      width: `${Math.max(1.5, (Math.abs(d.logProb) / maxLog) * 100)}%`,
                      background: `linear-gradient(90deg, ${d.color}50, ${d.color}20)`,
                    }}
                  />
                </div>
              </div>
            ))}
            <div className="pt-3 border-t border-border">
              <div className="flex items-baseline justify-between mb-1.5">
                <span className="text-xs font-medium text-green">Atoms in observable universe</span>
                <span className="text-xs font-mono font-bold text-green">10<sup>80</sup></span>
              </div>
              <div className="relative h-3 bg-cream rounded-full overflow-hidden">
                <div
                  className="absolute inset-y-0 left-0 rounded-full bg-green"
                  style={{ width: '0.03%', minWidth: '3px', opacity: 0.5 }}
                />
              </div>
              <p className="text-2xs text-text-tertiary mt-1 italic">
                Barely visible at this scale — that's the point
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <p className="text-sm text-text-secondary leading-relaxed">
            Even a minimal self-replicating system of 100 base pairs contains 200 bits of specified
            information with a random assembly probability of 10<sup>-60</sup>. For a minimal free-living genome
            (300,000 bp), the probability is 10<sup>-180,618</sup>. Even if every atom in the observable universe
            were a separate experiment running every Planck time since the Big Bang, you would only
            get ~10<sup>150</sup> trials — leaving a gap of over <strong className="text-text-primary">180,000 orders
            of magnitude</strong>.
          </p>
        </div>
      </div>
    </section>
  )
}
