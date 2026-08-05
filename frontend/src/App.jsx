import Navbar from "./components/navigation/Navbar";

function App() {
  return (
    <div className="min-h-screen bg-[#050816] text-slate-100">
      <Navbar />

      <main className="flex min-h-[calc(100vh-5rem)] items-center justify-center">
        <p className="text-slate-500">
          Landing page content coming next
        </p>
      </main>
    </div>
  );
}

export default App;