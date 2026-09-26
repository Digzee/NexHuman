import Hero from "../components/hero/Hero";
import Navbar from "../components/navigation/Navbar";

function App() {
  return (
    <div className="min-h-screen bg-[#050816] text-slate-100">
      <Navbar />
      <Hero />
    </div>
  );
}

export default App;