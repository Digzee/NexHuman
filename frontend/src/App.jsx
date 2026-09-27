import { Route, Routes } from "react-router-dom";

import HomePage from "./pages/HomePage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import DashboardPage from "./pages/DashboardPage";
import ForgotPasswordPage from "./pages/ForgotPasswordPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import DashboardLayout from "./components/dashboard/DashboardLayout";
import PortfolioPage from "./pages/PortfolioPage";
import InvestorProfilePage from "./pages/InvestorProfilePage";
import OptimizePage from "./pages/OptimizePage";
import AdvisorPage from "./pages/AdvisorPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />

      <Route
        path="/forgot-password"
        element={<ForgotPasswordPage />}
      />

      <Route
        path="/reset-password/:uid/:token"
        element={<ResetPasswordPage />}
      />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="portfolio" element={<PortfolioPage />} />
          <Route
            path="profile"
            element={<InvestorProfilePage />}
          />
          <Route
            path="optimise"
            element={<OptimizePage />}
          />
          <Route
            path="advisor"
            element={<AdvisorPage />}
          />
        </Route>
      </Route>
    </Routes>
  );
}


export default App;