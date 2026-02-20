import { useState, useEffect } from 'react'
import Regression from './sections/Regression'
import MonteCarlo from './sections/MonteCarlo'
import Models from './sections/Models'
import Thresholds from './sections/Thresholds'
import Information from './sections/Information'
import Datasets from './sections/Datasets'
import Findings from './sections/Findings'

const NAV_ITEMS = [
  { id: 'regression', label: 'Trend' },
  { id: 'monte-carlo', label: 'Uncertainty' },
  { id: 'models', label: 'Models' },
  { id: 'thresholds', label: 'Thresholds' },
  { id: 'information', label: 'Information' },
  { id: 'datasets', label: 'Data' },
  { id: 'findings', label: 'Findings' },
]

function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [active, setActive] = useState('')

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 80)

      const sections = NAV_ITEMS.map(item => {
        const el = document.getElementById(item.id)
        if (!el) return { id: item.id, top: Infinity }
        return { id: item.id, top: el.getBoundingClientRect().top }
      })

      const current = sections.reduce((closest, section) => {
        if (section.top <= 200 && section.top > closest.top) return section
        return closest
      }, { id: '', top: -Infinity })

      setActive(current.id)
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      scrolled ? 'bg-cream/90 backdrop-blur-md border-b border-border shadow-sm' : 'bg-transparent'
    }`}>
      <div className="max-w-wide mx-auto px-5 sm:px-8 flex items-center justify-between h-14">
        <a href="#" className="text-sm font-semibold text-text-primary tracking-tight">
          Genome Clock
        </a>
        <div className="hidden sm:flex items-center gap-1">
          {NAV_ITEMS.map(item => (
            <a
              key={item.id}
              href={`#${item.id}`}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                active === item.id
                  ? 'text-accent bg-accent-light'
                  : 'text-text-secondary hover:text-text-primary hover:bg-surface'
              }`}
            >
              {item.label}
            </a>
          ))}
        </div>
        <a
          href="https://github.com/itsbakr/dna-before-earth"
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-text-tertiary hover:text-text-primary transition-colors"
        >
          GitHub
        </a>
      </div>
    </nav>
  )
}

function Hero() {
  return (
    <section className="pt-28 sm:pt-36 pb-16 sm:pb-24">
      <div className="max-w-wide mx-auto px-5 sm:px-8">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold tracking-[0.2em] uppercase text-accent mb-4">
            Research
          </p>
          <h1 className="text-4xl sm:text-5xl lg:text-[3.4rem] font-serif font-semibold text-text-primary tracking-tight leading-[1.1] mb-5">
            The Genome<br />Complexity Clock
          </h1>
          <p className="text-lg sm:text-xl text-text-secondary leading-relaxed mb-4 max-w-xl">
            A quantitative replication of a dismissed 2006 finding — tested with 10,000 simulations,
            5 alternative models, and 3 independent datasets.
          </p>
          <p className="text-sm text-text-tertiary leading-relaxed max-w-xl">
            In 2006, Alexei Sharov (NIH) showed genome complexity follows an exponential trend
            that extrapolates to an origin ~10 billion years ago — before Earth existed.
            A Caltech peer reviewer dismissed it. Nobody ever tested whether he was wrong. We did.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-12">
          <HeroStat value="9.8 Bya" label="Predicted origin" sublabel="More than 2× Earth's age" />
          <HeroStat value="100%" label="Pre-Earth" sublabel="10,000 Monte Carlo sims" />
          <HeroStat value="0.967" label="R-squared" sublabel="5 points, 3.5 Byr span" />
          <HeroStat value="5" label="Models tested" sublabel="All confirm or worsen" />
        </div>

        <div className="mt-12 pt-8 border-t border-border">
          <div className="flex flex-wrap gap-3">
            {['Monte Carlo', 'Bootstrap', 'Logistic Regression', 'Information Theory', 'Multi-dataset'].map(tag => (
              <span key={tag} className="text-xs font-medium text-text-tertiary bg-surface border border-border rounded-full px-3 py-1">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

function HeroStat({ value, label, sublabel }) {
  return (
    <div className="border border-border rounded-xl p-5 bg-surface">
      <p className="text-2xl sm:text-3xl font-mono font-bold text-text-primary tracking-tight">{value}</p>
      <p className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mt-1">{label}</p>
      {sublabel && <p className="text-2xs text-text-tertiary mt-0.5">{sublabel}</p>}
    </div>
  )
}

function Author() {
  return (
    <section className="border-t border-border bg-surface">
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-14 sm:py-20">
        <div className="flex flex-col sm:flex-row items-start gap-5">
          <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center text-accent font-semibold text-base shrink-0">
            AB
          </div>
          <div>
            <p className="text-xs font-semibold tracking-[0.15em] uppercase text-text-tertiary mb-1">Built by</p>
            <a
              href="https://github.com/itsbakr"
              target="_blank"
              rel="noopener noreferrer"
              className="text-lg font-semibold text-text-primary hover:text-accent transition-colors"
            >
              Ahmed Bakr
            </a>
            <p className="text-sm text-text-secondary leading-relaxed mt-2 max-w-lg">
              AI engineer with 8 years shipping products across 6 countries.
              Founder of{' '}
              <a href="https://getawn.ai" target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">Awn AI</a>
              {' '}(Arabic AI agent builder) and Awn Labs (Arabic AI training data).
            </p>
            <div className="flex gap-4 mt-3">
              <a href="https://github.com/itsbakr" target="_blank" rel="noopener noreferrer" className="text-xs text-text-tertiary hover:text-accent transition-colors">
                GitHub
              </a>
              <a href="https://github.com/itsbakr/dna-before-earth" target="_blank" rel="noopener noreferrer" className="text-xs text-text-tertiary hover:text-accent transition-colors">
                Source Code
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="border-t border-border bg-cream">
      <div className="max-w-wide mx-auto px-5 sm:px-8 py-12 sm:py-16">
        <div className="grid sm:grid-cols-3 gap-8 mb-10">
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">Primary Sources</h4>
            <div className="space-y-2 text-sm text-text-secondary">
              <p>Sharov, A.A. (2006). <em>Biology Direct</em>, 1:17</p>
              <p>Sharov & Gordon (2013). arXiv:1304.3381</p>
              <p>Markov et al. (2010). <em>Paleontological Journal</em>, 44:363</p>
            </div>
          </div>
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">Data Sources</h4>
            <div className="space-y-2 text-sm text-text-secondary">
              <p>NCBI GenBank</p>
              <p>Animal Genome Size Database</p>
              <p>Standard paleontological consensus</p>
            </div>
          </div>
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">Methodology</h4>
            <div className="space-y-2 text-sm text-text-secondary">
              <p>Monte Carlo uncertainty propagation</p>
              <p>Bootstrap resampling (10,000×)</p>
              <p>AIC/BIC model comparison</p>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-text-primary">The Genome Complexity Clock</p>
            <p className="text-xs text-text-tertiary mt-1">
              By{' '}
              <a href="https://github.com/itsbakr" target="_blank" rel="noopener noreferrer" className="text-text-secondary hover:text-accent transition-colors">
                Ahmed Bakr
              </a>
              {' '}· AI-assisted scientific replication · Every number is reproducible from public data
            </p>
          </div>
          <p className="text-xs text-text-tertiary">
            MIT License · Open Source ·{' '}
            <a href="https://github.com/itsbakr/dna-before-earth" target="_blank" rel="noopener noreferrer" className="text-text-secondary hover:text-accent transition-colors">
              View on GitHub
            </a>
          </p>
        </div>
      </div>
    </footer>
  )
}

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <Regression />
      <MonteCarlo />
      <Models />
      <Thresholds />
      <Information />
      <Datasets />
      <Findings />
      <Author />
      <Footer />
    </div>
  )
}
