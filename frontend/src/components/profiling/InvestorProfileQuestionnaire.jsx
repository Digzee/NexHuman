const QUESTIONS = [
  {
    field: "investment_horizon",
    title: "Investment horizon",
    description:
      "How long do you expect to keep this money invested?",
    low: "Short term",
    high: "Long term",
  },
  {
    field: "loss_tolerance",
    title: "Loss tolerance",
    description:
      "How comfortable are you with temporary investment losses?",
    low: "Very uncomfortable",
    high: "Very comfortable",
  },
  {
    field: "volatility_comfort",
    title: "Market volatility",
    description:
      "How comfortable are you with significant changes in portfolio value?",
    low: "Prefer stability",
    high: "Comfortable with volatility",
  },
  {
    field: "investment_experience",
    title: "Investment experience",
    description:
      "How experienced are you with investing and financial markets?",
    low: "Very limited",
    high: "Very experienced",
  },
  {
    field: "growth_preference",
    title: "Growth preference",
    description:
      "How strongly do you prioritise long-term growth over capital stability?",
    low: "Prefer stability",
    high: "Prioritise growth",
  },
];


function InvestorProfileQuestionnaire({
  answers,
  onAnswerChange,
  onSubmit,
  isSubmitting,
  error,
}) {
  return (
    <form
      onSubmit={onSubmit}
      className="mt-8 space-y-5"
    >
      {QUESTIONS.map((question) => (
        <fieldset
          key={question.field}
          className="rounded-2xl border border-white/10 bg-[#0B1020] p-5"
        >
          <legend className="px-1 text-base font-semibold text-white">
            {question.title}
          </legend>

          <p className="mt-1 text-sm leading-6 text-slate-400">
            {question.description}
          </p>

          <div className="mt-5 flex items-center justify-between gap-2">
            {[1, 2, 3, 4, 5].map((value) => {
              const selected =
                answers[question.field] === value;

              return (
                <label
                  key={value}
                  className={`flex h-11 w-11 cursor-pointer items-center justify-center rounded-xl border text-sm font-semibold transition ${
                    selected
                      ? "border-cyan-400 bg-cyan-400/10 text-cyan-300"
                      : "border-white/10 text-slate-300 hover:bg-white/5"
                  }`}
                >
                  <input
                    type="radio"
                    name={question.field}
                    value={value}
                    checked={selected}
                    onChange={() =>
                      onAnswerChange(
                        question.field,
                        value
                      )
                    }
                    className="sr-only"
                  />

                  {value}
                </label>
              );
            })}
          </div>

          <div className="mt-3 flex justify-between gap-4 text-xs text-slate-500">
            <span>{question.low}</span>
            <span className="text-right">
              {question.high}
            </span>
          </div>
        </fieldset>
      ))}

      {error && (
        <p
          role="alert"
          className="text-sm text-red-300"
        >
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-flex w-full items-center justify-center rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
      >
        {isSubmitting
          ? "Calculating profile..."
          : "Calculate my risk profile"}
      </button>
    </form>
  );
}


export default InvestorProfileQuestionnaire;