const formatPercentage = (value) => {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return `${Number(value).toFixed(1)}%`;
};

const formatConcentration = (value) => {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return Number(value).toFixed(3);
};

const getRiskDescription = (riskLabel) => {
  switch (riskLabel) {
    case "Low":
      return "Lower historical and concentration-based portfolio risk.";

    case "Moderate":
      return "Moderate historical and concentration-based portfolio risk.";

    case "High":
      return "Elevated historical and concentration-based portfolio risk.";

    case "Very High":
      return "Very high historical and concentration-based portfolio risk.";

    default:
      return "Risk analysis is not currently available.";
  }
};

function PortfolioRiskSummary({
  risk,
  isLoading,
  error,
}) {
  if (isLoading) {
    return (
      <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
        <p className="text-sm text-slate-400">
          Analysing portfolio risk...
        </p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="rounded-2xl border border-red-500/20 bg-[#0B1020] p-6">
        <p className="text-sm text-red-400">
          {error}
        </p>
      </section>
    );
  }

  if (!risk) {
    return null;
  }

  const riskAvailable =
    risk.risk_label !== "Unavailable";

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
      <div className="mb-6">
        <p className="text-sm font-medium text-cyan-400">
          Portfolio analysis
        </p>

        <h2 className="mt-1 text-xl font-semibold text-slate-100">
          Risk Summary
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
          Historical market risk and portfolio
          concentration based on your current
          holdings.
        </p>
      </div>

      {!riskAvailable ? (
        <div className="rounded-xl border border-white/10 bg-white/[0.02] p-5">
          <p className="text-sm text-slate-400">
            Add portfolio holdings and sufficient
            historical data to calculate risk.
          </p>
        </div>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-white/[0.02] p-5">
              <p className="text-sm text-slate-400">
                Overall risk
              </p>

              <p className="mt-2 text-2xl font-semibold text-slate-100">
                {risk.risk_label}
              </p>

              <p className="mt-2 text-xs leading-5 text-slate-500">
                {getRiskDescription(
                  risk.risk_label
                )}
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/[0.02] p-5">
              <p className="text-sm text-slate-400">
                Annualised volatility
              </p>

              <p className="mt-2 text-2xl font-semibold text-slate-100">
                {formatPercentage(
                  risk.annualised_volatility_percentage
                )}
              </p>

              <p className="mt-2 text-xs leading-5 text-slate-500">
                Historical variability of portfolio
                returns, annualised using a 365-day
                cryptocurrency convention.
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/[0.02] p-5">
              <p className="text-sm text-slate-400">
                Maximum drawdown
              </p>

              <p className="mt-2 text-2xl font-semibold text-slate-100">
                {formatPercentage(
                  risk.maximum_drawdown_percentage
                )}
              </p>

              <p className="mt-2 text-xs leading-5 text-slate-500">
                Largest historical peak-to-trough
                decline during the selected period.
              </p>
            </div>
          </div>

          <div className="mt-6 rounded-xl border border-white/10 bg-white/[0.02] p-5">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-sm text-slate-400">
                  Diversification
                </p>

                <p className="mt-1 text-xl font-semibold text-slate-100">
                  {risk.diversification_label}
                </p>
              </div>

              <div className="rounded-full border border-purple-400/20 bg-purple-500/10 px-3 py-1 text-xs font-medium text-purple-300">
                HHI{" "}
                {formatConcentration(
                  risk.concentration_index
                )}
              </div>
            </div>

            <div className="mt-5 grid gap-4 sm:grid-cols-3">
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">
                  Assets
                </p>

                <p className="mt-1 text-lg font-medium text-slate-200">
                  {risk.asset_count}
                </p>
              </div>

              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">
                  Largest holding
                </p>

                <p className="mt-1 text-lg font-medium text-slate-200">
                  {formatPercentage(
                    risk.largest_holding_percentage
                  )}
                </p>
              </div>

              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">
                  Concentration
                </p>

                <p className="mt-1 text-lg font-medium text-slate-200">
                  {formatConcentration(
                    risk.concentration_index
                  )}
                </p>
              </div>
            </div>

            <p className="mt-5 border-t border-white/10 pt-4 text-xs leading-5 text-slate-500">
              Diversification is estimated using a
              concentration index based on portfolio
              allocation weights. Lower values indicate
              a more evenly distributed portfolio.
            </p>
          </div>
        </>
      )}

      <p className="mt-5 text-xs leading-5 text-slate-500">
        Risk classifications are educational NexHuman
        indicators derived from historical volatility,
        drawdown and portfolio concentration. They are
        not a personal investor risk profile or
        investment advice.
      </p>
    </section>
  );
}

export default PortfolioRiskSummary;