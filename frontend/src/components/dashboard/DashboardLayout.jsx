import { useState } from "react";
import { Outlet } from "react-router-dom";

import DashboardHeader from "./DashboardHeader";
import DashboardSidebar from "./DashboardSidebar";


function DashboardLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  function openSidebar() {
    setIsSidebarOpen(true);
  }

  function closeSidebar() {
    setIsSidebarOpen(false);
  }

  return (
    <div className="min-h-screen bg-[#050816] text-[#F8FAFC]">
      <DashboardSidebar
        isOpen={isSidebarOpen}
        onClose={closeSidebar}
      />

      <div className="lg:pl-64">
        <DashboardHeader onMenuClick={openSidebar} />

        <main className="px-6 py-8 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}


export default DashboardLayout;