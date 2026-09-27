import { useEffect, useState } from "react";

import { API_BASE_URL } from "../config/api";
import { useAuth } from "../context/AuthContext";


function formatPercentage(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return `${(Number(value) * 100).toFixed(2)}%`;
}


function formatWeight(value) {
  const percentage = Number(value) * 100;

  if (percentage < 0.01) {
    return "0.00%";
  }

  return `${percentage.toFixed(2)}%`;
}


function formatNumber(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return Number(value).toFixed(3);
}


function OptimizePage() {
  const { authenticatedFetch } = useAuth();

  const [portfolios, setPortfolios] = useState([]);
  const [selectedPortfolioId, setSelectedPortfolioId] =
    useState("");

  const [profile, setProfile] = useState(null);
  const [result, setResult] = useState(null);

  const [isLoading, setIsLoading] = useState(true);
  const [isOptimizing, setIsOptimizing] =
    useState(false);

  const [error, setError] = useState("");


  useEffect(() => {
    async function loadPage() {
      try {
        const [
          portfolioResponse,
          profileResponse,
        ] = await Promise.all([
          authenticatedFetch(
            `${API_BASE_URL}/portfolios/`
          ),
          authenticatedFetch(
            `${API_BASE_URL}/profiling/`
          ),
        ]);

        if (!portfolioResponse.ok) {
          throw new Error(
            "Unable to load portfolios."
          );
        }

        const portfolioData =
          await portfolioResponse.json();

        setPortfolios(portfolioData);

        if (portfolioData.length > 0) {
          setSelectedPortfolioId(
            String(portfolioData[0].id)
          );
        }

        if (profileResponse.ok) {
          const profileData =
            await profileResponse.json();

          setProfile(profileData);
        }
      } catch {
        setError(
          "We couldn't load the optimisation workspace."
        );
      } finally {
        setIsLoading(false);
      }
    }

    loadPage();

    // authenticatedFetch is provided by AuthContext.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  async function handleOptimize() {
    if (!selectedPortfolioId) {
      setError(
        "Please select a portfolio."
      );
      return;
    }

    if (!profile) {
      setError(
        "Complete your investor profile before optimising a portfolio."
      );
      return;
    }

    setError("");
    setIsOptimizing(true);
    setResult(null);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/optimizer/portfolio/${selectedPortfolioId}/`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Portfolio optimisation failed."
        );
      }

      setResult(data);
    } catch (requestError) {
      setError(
        requestError.message ||
          "Portfolio optimisation failed."
      );
    } finally {
      setIsOptimizing(false);
    }
  }


  if (isLoading) {
    return (
      <p className="text-sm text-slate-400">
        Loading optimisation workspace...
      </p>
    );
  }


  return (
    <section className="pb-12">
      <p className="text-sm font-medium text-cyan-400">
        Portfolio Optimiser
      </p>

      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
        Optimise your portfolio
      </h1>

      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">
        NexHuman uses a genetic algorithm to search for
        portfolio allocations with improved historical
        risk-adjusted performance while respecting your
        investor profile.
      </p>


      <div className="mt-8 grid gap-5 lg:grid-cols-3">
        <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6 lg:col-span-2">
          <label
            htmlFor="portfolio"
            className="text-sm font-medium text-slate-200"
          >
            Portfolio
          </label>

          <select
            id="portfolio"
            value={selectedPortfolioId}
            onChange={(event) => {
              setSelectedPortfolioId(
                event.target.value
              );
              setResult(null);
            }}
            className="mt-3 w-full rounded-xl border border-white/10 bg-[#11172A] px-4 py-3 text-sm text-white outline-none focus:border-cyan-400"
          >
            {portfolios.length === 0 && (
              <option value="">
                No portfolios available
              </option>
            )}

            {portfolios.map((portfolio) => (
              <option
                key={portfolio.id}
                value={portfolio.id}
              >
                {portfolio.name}
              </option>
            ))}
          </select>

          <button
            type="button"
            onClick={handleOptimize}
            disabled={
              isOptimizing ||
              !selectedPortfolioId ||
              !profile
            }
            className="mt-5 inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isOptimizing
              ? "Running genetic algorithm..."
              : "Optimise Portfolio"}
          </button>

          {isOptimizing && (
            <p className="mt-3 text-xs leading-5 text-slate-500">
              Analysing historical market data and
              evolving candidate portfolio allocations.
            </p>
          )}

          {error && (
            <p
              role="alert"
              className="mt-4 text-sm text-red-300"
            >
              {error}
            </p>
          )}
        </div>


        <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
            Investor profile
          </p>

          {profile ? (
            <>
              <p className="mt-4 text-2xl font-semibold text-white">
                {profile.risk_label_display}
              </p>

              <p className="mt-1 text-sm text-slate-400">
                {profile.risk_score}/25 profile score
              </p>

              <p className="mt-5 text-xs leading-5 text-slate-500">
                Your investor profile influences the
                portfolio concentration constraint used
                during optimisation.
              </p>
            </>
          ) : (
            <p className="mt-4 text-sm leading-6 text-slate-400">
              Complete your investor profile before
              running the optimiser.
            </p>
          )}
        </div>
      </div>


      {result && (
        <>
          <div className="mt-8">
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-400">
              Recommended allocation
            </p>

            <h2 className="mt-2 text-2xl font-semibold text-white">
              Genetic algorithm result
            </h2>

            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
              The allocation below represents the
              highest-fitness portfolio identified by
              this optimisation run under the selected
              constraints.
            </p>
          </div>


          <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
            {result.allocations.map(
              (allocation) => (
                <div
                  key={allocation.symbol}
                  className="rounded-2xl border border-white/10 bg-[#0B1020] p-5"
                >
                  <p className="text-sm font-medium text-slate-400">
                    {allocation.symbol}
                  </p>

                  <p className="mt-2 text-2xl font-semibold text-white">
                    {formatWeight(
                      allocation.weight
                    )}
                  </p>

                  <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-white/5">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-violet-500 to-cyan-400"
                      style={{
                        width: `${Math.max(
                          0,
                          Math.min(
                            Number(
                              allocation.weight
                            ) * 100,
                            100
                          )
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              )
            )}
          </div>


          <div className="mt-8 grid gap-5 lg:grid-cols-2">
            <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
              <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-400">
                GA portfolio
              </p>

              <div className="mt-5 space-y-4">
                <MetricRow
                  label="Annualised return"
                  value={formatPercentage(
                    result.expected_return
                  )}
                />

                <MetricRow
                  label="Annualised volatility"
                  value={formatPercentage(
                    result.volatility
                  )}
                />

                <MetricRow
                  label="Sharpe ratio"
                  value={formatNumber(
                    result.sharpe_ratio
                  )}
                />
              </div>
            </div>


            <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
              <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
                Equal-weight baseline
              </p>

              <div className="mt-5 space-y-4">
                <MetricRow
                  label="Annualised return"
                  value={formatPercentage(
                    result.baseline_return
                  )}
                />

                <MetricRow
                  label="Annualised volatility"
                  value={formatPercentage(
                    result.baseline_volatility
                  )}
                />

                <MetricRow
                  label="Sharpe ratio"
                  value={formatNumber(
                    result.baseline_sharpe_ratio
                  )}
                />
              </div>
            </div>
          </div>


          <div className="mt-5 rounded-2xl border border-cyan-400/20 bg-cyan-400/[0.03] p-6">
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-400">
              NexHuman Explanation
            </p>

            <h3 className="mt-2 text-lg font-semibold text-white">
              Understanding this recommendation
            </h3>

            <div className="mt-5 space-y-4 text-sm leading-6 text-slate-400">
              <p>
                {result.explanation.summary}
              </p>

              <p>
                {result.explanation.comparison}
              </p>

              <p>
                {result.explanation.risk_context}
              </p>

              <p>
                {result.explanation.return_context}
              </p>
            </div>
          </div>


          <div className="mt-5 rounded-2xl border border-white/10 bg-[#0B1020] p-6">
            <h3 className="text-lg font-semibold text-white">
              How this recommendation was produced
            </h3>

            <p className="mt-3 max-w-4xl text-sm leading-6 text-slate-400">
              NexHuman analysed {result.historical_days}{" "}
              days of historical cryptocurrency market
              data. Candidate allocations were evolved
              using tournament selection, blend
              crossover, mutation and elitism. Fitness
              was evaluated using historical
              risk-adjusted return.
            </p>

            <div className="mt-5 grid gap-4 sm:grid-cols-3">
              <MethodItem
                label="Population"
                value={result.population_size}
              />

              <MethodItem
                label="Generations"
                value={result.generations}
              />

              <MethodItem
                label="Risk profile"
                value={
                  result.risk_profile
                    .charAt(0)
                    .toUpperCase() +
                  result.risk_profile.slice(1)
                }
              />
            </div>

            <p className="mt-5 border-t border-white/10 pt-4 text-xs leading-5 text-slate-500">
              Historical optimisation does not predict
              future performance. Results are provided
              for educational purposes and should not
              be interpreted as financial advice.
            </p>
          </div>
        </>
      )}
    </section>
  );
}


function MetricRow({
  label,
  value,
}) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-white/5 pb-3 last:border-0 last:pb-0">
      <span className="text-sm text-slate-400">
        {label}
      </span>

      <span className="text-sm font-semibold text-white">
        {value}
      </span>
    </div>
  );
}


function MethodItem({
  label,
  value,
}) {
  return (
    <div className="rounded-xl bg-white/[0.03] p-4">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-slate-200">
        {value}
      </p>
    </div>
  );
}


export default OptimizePage;