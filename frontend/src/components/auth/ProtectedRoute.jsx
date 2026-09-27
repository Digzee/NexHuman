import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";


function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#050816] text-[#F8FAFC]">
        <p className="text-sm text-slate-400">
          Loading NexHuman...
        </p>
      </main>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}


export default ProtectedRoute;