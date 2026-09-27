import {
  FaChartPie,
  FaGear,
  FaRobot,
  FaSliders,
  FaWallet,
  FaXmark,
} from "react-icons/fa6";
import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";


const navigation = [
  {
    name: "Overview",
    to: "/dashboard",
    icon: FaChartPie,
    end: true,
  },
  {
    name: "Portfolio",
    to: "/dashboard/portfolio",
    icon: FaWallet,
  },
  {
    name: "Optimise",
    to: "/dashboard/optimise",
    icon: FaSliders,
  },
  {
    name: "AI Advisor",
    to: "/dashboard/advisor",
    icon: FaRobot,
  },
];


function DashboardSidebar({
  isOpen = false,
  onClose = () => {},
}) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
    await logout();
    onClose();
    navigate("/login");
  }

  function renderNavigation() {
    return (
      <nav
        aria-label="Dashboard navigation"
        className="flex flex-1 flex-col px-4 py-6"
      >
        <div className="space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.to}
                end={item.end}
                onClick={onClose}
                className={({ isActive }) =>
                  [
                    "flex items-center gap-3 rounded-xl px-3 py-2.5",
                    "text-sm font-medium transition",
                    isActive
                      ? "bg-white/10 text-white"
                      : "text-slate-400 hover:bg-white/5 hover:text-white",
                  ].join(" ")
                }
              >
                <Icon aria-hidden="true" className="text-base" />
                {item.name}
              </NavLink>
            );
          })}
        </div>

        <div className="mt-auto space-y-1 border-t border-white/10 pt-4">
          <NavLink
            to="/dashboard/settings"
            onClick={onClose}
            className={({ isActive }) =>
              [
                "flex items-center gap-3 rounded-xl px-3 py-2.5",
                "text-sm font-medium transition",
                isActive
                  ? "bg-white/10 text-white"
                  : "text-slate-400 hover:bg-white/5 hover:text-white",
              ].join(" ")
            }
          >
            <FaGear aria-hidden="true" />
            Settings
          </NavLink>

          <button
            type="button"
            onClick={handleLogout}
            className="flex w-full items-center rounded-xl px-3 py-2.5 text-left text-sm font-medium text-slate-400 transition hover:bg-white/5 hover:text-white lg:hidden"
          >
            Logout
          </button>
        </div>
      </nav>
    );
  }

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 border-r border-white/10 bg-[#080C19] lg:flex lg:flex-col">
        <div className="flex h-20 items-center border-b border-white/10 px-6">
          <NavLink
            to="/dashboard"
            className="text-xl font-semibold tracking-tight text-white"
          >
            NexHuman
          </NavLink>
        </div>

        {renderNavigation()}
      </aside>

      {/* Mobile backdrop */}
      {isOpen && (
        <button
          type="button"
          aria-label="Close navigation"
          onClick={onClose}
          className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm lg:hidden"
        />
      )}

      {/* Mobile sidebar */}
      <aside
        className={[
          "fixed inset-y-0 left-0 z-50 flex w-72 flex-col",
          "border-r border-white/10 bg-[#080C19]",
          "transition-transform duration-300 lg:hidden",
          isOpen ? "translate-x-0" : "-translate-x-full",
        ].join(" ")}
      >
        <div className="flex h-20 items-center justify-between border-b border-white/10 px-6">
          <NavLink
            to="/dashboard"
            onClick={onClose}
            className="text-xl font-semibold tracking-tight text-white"
          >
            NexHuman
          </NavLink>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close navigation"
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-white/5 hover:text-white"
          >
            <FaXmark aria-hidden="true" />
          </button>
        </div>

        {renderNavigation()}
      </aside>
    </>
  );
}


export default DashboardSidebar;