function formatCurrency(value) {
  const number = Number(value);

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(number);
}


function formatPercentage(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return `${Number(value).toFixed(2)}%`;
}


function PortfolioOverview({
  valuation,
  isLoading,
  error,
}) {
  if (isLoading) {
    return (
      <div className="mt-6 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
        <p className="text-sm text-slate-400">
          Loading portfolio valuation...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-6 rounded-2xl border border-red-500/20 bg-red-500/5 p-6">
        <p className="text-sm text-red-300">
          {error}
        </p>
      </div>
    );
  }

  if (!valuation) {
    return null;
  }

  const profitLoss = Number(
    valuation.profit_loss
  );

  const profitLossClass =
    profitLoss > 0
      ? "text-green-400"
      : profitLoss < 0
        ? "text-red-400"
        : "text-slate-200";

  const cards = [
    {
      label: "Portfolio value",
      value: formatCurrency(
        valuation.total_value
      ),
    },
    {
      label: "Profit / loss",
      value: formatCurrency(
        valuation.profit_loss
      ),
      valueClass: profitLossClass,
    },
    {
      label: "Return",
      value: formatPercentage(
        valuation.return_percentage
      ),
      valueClass: profitLossClass,
    },
    {
      label: "Cost basis coverage",
      value: formatPercentage(
        valuation.cost_basis_coverage_percentage
      ),
    },
  ];

  return (
    <section
      aria-labelledby="portfolio-overview-heading"
      className="mt-6"
    >
      <div className="mb-4">
        <h3
          id="portfolio-overview-heading"
          className="text-base font-semibold text-white"
        >
          Portfolio overview
        </h3>

        <p className="mt-1 text-sm text-slate-400">
          Current valuation based on the latest
          available market prices.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => (
          <div
            key={card.label}
            className="rounded-2xl border border-white/10 bg-[#11172A] p-5"
          >
            <p className="text-xs font-medium uppercase tracking-[0.14em] text-slate-500">
              {card.label}
            </p>

            <p
              className={`mt-3 text-2xl font-semibold tracking-tight ${
                card.valueClass || "text-white"
              }`}
            >
              {card.value}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}


export default PortfolioOverview;