import { Link } from "react-router-dom";

import Container from "../layout/Container";
import Button from "../ui/Button";


function Navbar() {
  return (
    <header className="relative z-20 border-b border-white/5 bg-[#050816]/80 backdrop-blur-md">
      <Container className="flex h-20 items-center justify-between">
        <Link
          to="/"
          className="text-xl font-semibold tracking-tight text-white"
        >
          NexHuman
        </Link>

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
          <Link
            to="/login"
            className="hidden px-4 py-2 text-sm font-medium text-slate-300 transition hover:text-white sm:block"
          >
            Login
          </Link>

          <Button to="/register" className="px-5 py-2.5">
            Register
          </Button>
        </div>
      </Container>
    </header>
  );
}


export default Navbar;