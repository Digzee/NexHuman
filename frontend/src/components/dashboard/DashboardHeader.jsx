import { FaBars } from "react-icons/fa6";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";


function DashboardHeader({ onMenuClick }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    navigate("/login");
  }

  return (
    <header className="flex h-20 items-center justify-between border-b border-white/10 bg-[#050816]/80 px-6 backdrop-blur lg:px-8">
      <div className="flex items-center gap-4">
        <button
          type="button"
          onClick={onMenuClick}
          aria-label="Open navigation"
          className="flex h-10 w-10 items-center justify-center rounded-lg text-slate-400 transition hover:bg-white/5 hover:text-white lg:hidden"
        >
          <FaBars aria-hidden="true" />
        </button>

        <div>
          <p className="hidden text-sm text-slate-500 sm:block">
            Portfolio intelligence
          </p>

          <p className="text-lg font-semibold tracking-tight text-white lg:hidden">
            NexHuman
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 sm:gap-4">
        <div className="hidden text-right md:block">
          <p className="text-sm font-medium text-white">
            {user.first_name} {user.last_name}
          </p>

          <p className="text-xs text-slate-500">
            {user.email}
          </p>
        </div>

        <div
          aria-hidden="true"
          className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-violet-600 to-blue-600 text-sm font-semibold text-white"
        >
          {user.first_name?.charAt(0)}
          {user.last_name?.charAt(0)}
        </div>

        <button
          type="button"
          onClick={handleLogout}
          className="hidden text-sm font-medium text-slate-400 transition hover:text-white sm:block"
        >
          Logout
        </button>
      </div>
    </header>
  );
}


export default DashboardHeader;