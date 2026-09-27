import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";


function DashboardPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <main className="min-h-screen bg-[#050816] px-6 py-12 text-[#F8FAFC]">
      <div className="mx-auto max-w-6xl">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-cyan-400">
            NexHuman Dashboard
          </p>

          <button
            type="button"
            onClick={handleLogout}
            className="text-sm font-medium text-slate-300 transition hover:text-white"
          >
            Logout
          </button>
        </div>

        <h1 className="mt-3 text-4xl font-semibold tracking-tight">
          Welcome, {user.first_name}.
        </h1>

        <p className="mt-4 text-slate-400">
          Your portfolio dashboard will be built here in Phase 3.
        </p>
      </div>
    </main>
  );
}


export default DashboardPage;