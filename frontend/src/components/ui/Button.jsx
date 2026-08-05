import { FaArrowRight } from "react-icons/fa6";

const variants = {
  primary:
    "bg-gradient-to-r from-violet-600 to-blue-600 text-white shadow-lg shadow-violet-950/40 hover:-translate-y-0.5 hover:shadow-violet-800/40",
  secondary:
    "border border-white/15 bg-white/5 text-white hover:-translate-y-0.5 hover:border-white/30 hover:bg-white/10",
};

function Button({
  children,
  variant = "primary",
  className = "",
  type = "button",
  showArrow = false,
}) {
  return (
    <button
      type={type}
      className={`group inline-flex items-center justify-center gap-3 rounded-full px-6 py-2.5 text-sm font-semibold transition duration-200 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:ring-offset-[#050816] ${variants[variant]} ${className}`}
    >
      <span>{children}</span>

      {showArrow && (
        <FaArrowRight
          aria-hidden="true"
          className="text-xs transition-transform duration-200 group-hover:translate-x-1"
        />
      )}
    </button>
  );
}

export default Button;