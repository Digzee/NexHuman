import Button from "../ui/Button";
import Container from "../layout/Container";
import HeroVisual from "./HeroVisual";

function Hero() {
  return (
    <main className="relative overflow-hidden">
      <div
        className="pointer-events-none absolute inset-0
                   bg-[radial-gradient(circle_at_18%_20%,rgba(124,58,237,0.17),transparent_36%),radial-gradient(circle_at_78%_25%,rgba(37,99,235,0.15),transparent_32%)]"
      />

      <Container
        className="relative grid min-h-[calc(100vh-5rem)] items-center
                   gap-12 py-16 lg:grid-cols-[minmax(0,1fr)_minmax(520px,1.2fr)]
                   lg:gap-16 lg:py-20 xl:gap-24"
      >
        <section className="max-w-2xl text-center lg:text-left">
          <p
            className="mb-6 text-xs font-semibold uppercase
                       tracking-[0.3em] text-violet-300 sm:text-sm"
          >
            AI-powered portfolio optimisation
          </p>

          <h1
            className="text-5xl font-semibold tracking-tight text-white
                       sm:text-6xl lg:text-7xl"
          >
            Smarter
            <span
              className="mt-1 block pb-2 leading-[1.08] bg-gradient-to-r
                         from-violet-300 via-purple-400 to-blue-400
                         bg-clip-text text-transparent"
            >
              Crypto Investing.
            </span>
          </h1>

          <h2
            className="mt-6 text-2xl font-medium leading-tight text-slate-200
                       sm:text-3xl"
          >
            Powered by your personal AI advisor.
          </h2>

          <p
            className="mx-auto mt-6 max-w-xl text-base leading-8
                       text-slate-400 sm:text-lg lg:mx-0"
          >
            Build smarter cryptocurrency portfolios using evolutionary AI,
            transparent recommendations and intelligent market insights.
          </p>

          <div
            className="mt-9 flex flex-col items-center justify-center gap-4
                       sm:flex-row lg:justify-start"
          >
            <Button className="min-w-40" showArrow>
              Start now
            </Button>

            <Button
              variant="secondary"
              className="min-w-40"
              showArrow
            >
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