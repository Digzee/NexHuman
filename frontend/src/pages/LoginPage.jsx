import { useState } from "react";
import { Link } from "react-router-dom";


const initialFormData = {
  email: "",
  password: "",
};


function LoginPage() {
  const [formData, setFormData] = useState(initialFormData);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));

    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setIsSuccess(false);
    setIsSubmitting(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/auth/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.detail || "Unable to log in with the provided credentials."
        );
        return;
      }

      /*
       * Token storage will be handled by the authentication
       * state/session layer in the next milestone.
       */
      //console.log("Login successful", data);

      setIsSuccess(true);
    } catch {
      setError("Unable to connect to NexHuman. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#050816] text-[#F8FAFC]">
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col justify-center px-6 py-12">
        <Link
          to="/"
          className="mb-10 text-xl font-semibold tracking-tight"
        >
          NexHuman
        </Link>

        <div>
          <p className="mb-3 text-sm font-medium text-cyan-400">
            Welcome back
          </p>

          <h1 className="text-4xl font-semibold tracking-tight">
            Log in to NexHuman.
          </h1>

          <p className="mt-4 text-sm leading-6 text-slate-400">
            Access your portfolios, optimisation results and intelligent
            investment insights.
          </p>
        </div>

        <form
          className="mt-8 space-y-5"
          onSubmit={handleSubmit}
          noValidate
        >
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-sm text-slate-300"
            >
              Email
            </label>

            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={formData.email}
              onChange={handleChange}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 outline-none transition focus:border-cyan-400/60"
            />
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between">
              <label
                htmlFor="password"
                className="text-sm text-slate-300"
              >
                Password
              </label>

              <span className="text-sm text-slate-500">
                Forgot password?
              </span>
            </div>

            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={formData.password}
              onChange={handleChange}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 outline-none transition focus:border-cyan-400/60"
            />
          </div>

          {error && (
            <p
              role="alert"
              className="text-sm text-red-400"
            >
              {error}
            </p>
          )}

          {isSuccess && (
            <p
              role="status"
              className="text-sm text-green-400"
            >
              Login successful.
            </p>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 px-5 py-3 font-medium transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Logging in..." : "Log in"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Don't have an account?{" "}
          <Link
            to="/register"
            className="font-medium text-cyan-400 hover:text-cyan-300"
          >
            Create one
          </Link>
        </p>
      </div>
    </main>
  );
}


export default LoginPage;