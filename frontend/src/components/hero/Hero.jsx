import Button from "../ui/Button";
import Container from "../layout/Container";
import HeroVisual from "./HeroVisual";

function Hero() {
  return (
    <main className="relative overflow-hidden">
      {/* Background lighting */}
      <div
        className="pointer-events-none absolute inset-0
                   bg-[radial-gradient(circle_at_20%_20%,rgba(124,58,237,0.16),transparent_34%),radial-gradient(circle_at_78%_25%,rgba(37,99,235,0.14),transparent_30%)]"
      />

      <Container
        className="relative grid min-h-[calc(100vh-5rem)] items-center
                   gap-10 py-14 lg:grid-cols-[0.9fr_1.1fr] lg:py-20"
      >
        <section className="text-center lg:text-left">
          <p
            className="mb-5 text-sm font-semibold uppercase
                       tracking-[0.25em] text-violet-300"
          >
            Human-first investment intelligence
          </p>

          <h1
            className="text-5xl font-semibold tracking-tight text-white
                       sm:text-6xl lg:text-7xl"
          >
            Smarter
            <span
              className="mt-1 block bg-gradient-to-r from-violet-300
                         via-purple-400 to-blue-400 bg-clip-text
                         text-transparent"
            >
              Crypto Investing.
            </span>
          </h1>

          <h2
            className="mt-6 text-2xl font-medium text-slate-200
                       sm:text-3xl"
          >
            Powered by your personal AI advisor.
          </h2>

          <p
            className="mx-auto mt-6 max-w-xl text-base leading-8
                       text-slate-400 sm:text-lg lg:mx-0"
          >
            Build, optimize and understand your cryptocurrency portfolio using
            evolutionary algorithms, transparent recommendations and
            intelligent market analysis.
          </p>

          <div
            className="mt-9 flex flex-col items-center justify-center gap-4
                       sm:flex-row lg:justify-start"
          >
            <Button className="min-w-40">
              Start now
            </Button>

            <Button variant="secondary" className="min-w-40">
              Learn more
            </Button>
          </div>

          <div
            className="mt-8 flex flex-wrap justify-center gap-x-6 gap-y-3
                       text-sm text-slate-400 lg:justify-start"
          >
            <span>✓ Evolutionary AI</span>
            <span>✓ Explainable recommendations</span>
            <span>✓ Market intelligence</span>
          </div>

          <p className="mt-5 text-xs leading-5 text-slate-600">
            Educational portfolio guidance. Not regulated financial advice.
          </p>
        </section>

        <HeroVisual />
      </Container>
    </main>
  );
}

export default Hero;