import Container from "../layout/Container";
import Button from "../ui/Button";

function Navbar() {
  return (
    <header className="relative z-20 border-b border-white/5 bg-[#050816]/80 backdrop-blur-md">
      <Container className="flex h-20 items-center justify-between">
        <a
          href="/"
          className="text-xl font-semibold tracking-tight text-white"
        >
          NexHuman
        </a>

        <nav
          aria-label="Primary navigation"
          className="hidden items-center gap-8 text-sm text-slate-300 md:flex"
        >
          <a className="transition hover:text-white" href="#features">
            Features
          </a>

          <a className="transition hover:text-white" href="#how-it-works">
            How it works
          </a>

          <a className="transition hover:text-white" href="#about">
            About
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <button className="hidden px-4 py-2 text-sm font-medium text-slate-300 transition hover:text-white sm:block">
            Login
          </button>

          <Button className="px-5 py-2.5">
            Register
          </Button>
        </div>
      </Container>
    </header>
  );
}

export default Navbar;