import { useAuth } from "../context/AuthContext";


function DashboardPage() {
  const { user } = useAuth();

  return (
    <section>
      <p className="text-sm font-medium text-cyan-400">
        Overview
      </p>

      <h1 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">
        Welcome back, {user.first_name}.
      </h1>

      <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
        Your portfolio overview, performance and investment
        insights will appear here.
      </p>
    </section>
  );
}


export default DashboardPage;