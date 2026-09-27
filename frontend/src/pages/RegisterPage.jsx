import { API_BASE_URL } from "../config/api";
import { useState } from "react";
import { Link } from "react-router-dom";


const initialFormData = {
  first_name: "",
  last_name: "",
  email: "",
  password: "",
};


function RegisterPage() {
  const [formData, setFormData] = useState(initialFormData);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));

    setErrors((current) => ({
      ...current,
      [name]: undefined,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setErrors({});
    setIsSubmitting(true);
    setIsSuccess(false);

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/register/`,
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
        setErrors(data);
        return;
      }

      setIsSuccess(true);
      setFormData(initialFormData);
    } catch {
      setErrors({
        general:
          "Unable to connect to NexHuman. Please try again.",
      });
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
            Create your account
          </p>

          <h1 className="text-4xl font-semibold tracking-tight">
            Start investing smarter.
          </h1>

          <p className="mt-4 text-sm leading-6 text-slate-400">
            Create your NexHuman account to build intelligent cryptocurrency
            portfolios powered by evolutionary optimisation.
          </p>
        </div>

        <form
          className="mt-8 space-y-5"
          onSubmit={handleSubmit}
          noValidate
        >
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <FormField
              label="First name"
              name="first_name"
              type="text"
              autoComplete="given-name"
              value={formData.first_name}
              error={errors.first_name}
              onChange={handleChange}
            />

            <FormField
              label="Last name"
              name="last_name"
              type="text"
              autoComplete="family-name"
              value={formData.last_name}
              error={errors.last_name}
              onChange={handleChange}
            />
          </div>

          <FormField
            label="Email"
            name="email"
            type="email"
            autoComplete="email"
            value={formData.email}
            error={errors.email}
            onChange={handleChange}
          />

          <FormField
            label="Password"
            name="password"
            type="password"
            autoComplete="new-password"
            value={formData.password}
            error={errors.password}
            onChange={handleChange}
          />

          {errors.general && (
            <p
              role="alert"
              className="text-sm text-red-400"
            >
              {errors.general}
            </p>
          )}

          {isSuccess && (
            <p
              role="status"
              className="text-sm text-green-400"
            >
              Account created successfully. You can now log in.
            </p>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 px-5 py-3 font-medium transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmitting ? "Creating account..." : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Already have an account?{" "}
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


function FormField({
  label,
  name,
  type,
  autoComplete,
  value,
  error,
  onChange,
}) {
  const errorMessage = Array.isArray(error) ? error[0] : error;
  const errorId = `${name}-error`;

  return (
    <div>
      <label
        htmlFor={name}
        className="mb-2 block text-sm text-slate-300"
      >
        {label}
      </label>

      <input
        id={name}
        name={name}
        type={type}
        autoComplete={autoComplete}
        value={value}
        onChange={onChange}
        aria-invalid={Boolean(errorMessage)}
        aria-describedby={errorMessage ? errorId : undefined}
        className={`w-full rounded-xl border bg-white/5 px-4 py-3 outline-none transition ${
          errorMessage
            ? "border-red-400/70 focus:border-red-400"
            : "border-white/10 focus:border-cyan-400/60"
        }`}
      />

      {errorMessage && (
        <p
          id={errorId}
          role="alert"
          className="mt-2 text-sm text-red-400"
        >
          {errorMessage}
        </p>
      )}
    </div>
  );
}


export default RegisterPage;