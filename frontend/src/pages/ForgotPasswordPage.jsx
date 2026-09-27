import { API_BASE_URL } from "../config/api";
import { useState } from "react";
import { Link } from "react-router-dom";


function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setIsSuccess(false);
    setIsSubmitting(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/password-reset/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        }
      );

      if (!response.ok) {
        setError("Unable to process the password reset request.");
        return;
      }

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
            Password recovery
          </p>

          <h1 className="text-4xl font-semibold tracking-tight">
            Reset your password.
          </h1>

          <p className="mt-4 text-sm leading-6 text-slate-400">
            Enter your email address and we'll send you instructions
            to reset your NexHuman password.
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
              value={email}
              onChange={(event) => {
                setEmail(event.target.value);
                setError("");
              }}
              className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 outline-none transition focus:border-cyan-400/60"
            />
          </div>

          {error && (
            <p role="alert" className="text-sm text-red-400">
              {error}
            </p>
          )}

          {isSuccess && (
            <p role="status" className="text-sm text-green-400">
              If an account exists for this email address, password
              reset instructions have been sent.
            </p>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 px-5 py-3 font-medium transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting
              ? "Sending instructions..."
              : "Send reset instructions"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Remember your password?{" "}
          <Link
            to="/login"
            className="font-medium text-cyan-400 hover:text-cyan-300"
          >
            Log in
          </Link>
        </p>
      </div>
    </main>
  );
}


export default ForgotPasswordPage;