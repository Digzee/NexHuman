import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";


const PERIODS = [
  {
    label: "1M",
    days: 30,
  },
  {
    label: "3M",
    days: 90,
  },
  {
    label: "6M",
    days: 180,
  },
  {
    label: "1Y",
    days: 365,
  },
];


function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value));
}


function formatCompactCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(Number(value));
}


function formatPercentage(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  return `${Number(value).toFixed(2)}%`;
}


function formatSignedPercentage(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  const numericValue = Number(value);

  return `${
    numericValue > 0 ? "+" : ""
  }${numericValue.toFixed(2)}%`;
}


function getReturnClass(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "text-slate-300";
  }

  const numericValue = Number(value);

  if (numericValue > 0) {
    return "text-emerald-400";
  }

  if (numericValue < 0) {
    return "text-red-400";
  }

  return "text-slate-200";
}


function formatDate(date) {
  return new Intl.DateTimeFormat(
    "en-US",
    {
      month: "short",
      day: "numeric",
    }
  ).format(
    new Date(`${date}T00:00:00`)
  );
}


function PerformanceTooltip({
  active,
  payload,
  label,
}) {
  if (!active || !payload?.length) {
    return null;
  }

  return (
    <div className="rounded-xl border border-white/10 bg-[#0B1020] px-4 py-3 shadow-xl">
      <p className="text-xs text-slate-400">
        {formatDate(label)}
      </p>

      <p className="mt-1 font-semibold text-white">
        {formatCurrency(payload[0].value)}
      </p>
    </div>
  );
}


function PortfolioPerformance({
  performance,
  selectedDays,
  onPeriodChange,
  isLoading,
  error,
}) {
  const hasData =
    performance?.data_points?.length > 0;

  const totalReturn = hasData
    ? performance.total_return_percentage
    : null;

  const annualisedReturn = hasData
    ? performance.annualised_return_percentage
    : null;

  const annualisedVolatility = hasData
    ? performance.annualised_volatility_percentage
    : null;

  const maximumDrawdown = hasData
    ? performance.maximum_drawdown_percentage
    : null;

  const chartData = hasData
    ? performance.data_points.map(
        (point) => ({
          date: point.date,
          value: Number(point.value),
        })
      )
    : [];

  return (
    <section
      aria-labelledby="portfolio-performance-heading"
      className="mt-8 rounded-2xl border border-white/10 bg-[#11172A] p-6"
    >
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h3
            id="portfolio-performance-heading"
            className="text-base font-semibold text-white"
          >
            Historical performance
          </h3>

          <p className="mt-1 max-w-2xl text-sm text-slate-400">
            Historical analysis of how your current
            holdings would have performed over the
            selected period.
          </p>
        </div>

        <div
          className="flex rounded-xl border border-white/10 bg-[#0B1020] p-1"
          aria-label="Performance period"
        >
          {PERIODS.map((period) => {
            const isSelected =
              selectedDays === period.days;

            return (
              <button
                key={period.days}
                type="button"
                onClick={() =>
                  onPeriodChange(period.days)
                }
                aria-pressed={isSelected}
                className={`rounded-lg px-3 py-2 text-xs font-medium transition ${
                  isSelected
                    ? "bg-violet-600 text-white"
                    : "text-slate-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                {period.label}
              </button>
            );
          })}
        </div>
      </div>

      {isLoading && (
        <div
          className="flex h-80 items-center justify-center text-sm text-slate-400"
          role="status"
        >
          Loading historical performance...
        </div>
      )}

      {!isLoading && error && (
        <div
          className="mt-6 rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-4 text-sm text-red-300"
          role="alert"
        >
          {error}
        </div>
      )}

      {!isLoading && !error && !hasData && (
        <div className="flex h-64 items-center justify-center text-center">
          <div>
            <p className="text-sm font-medium text-slate-300">
              Historical performance is not available.
            </p>

            <p className="mt-2 max-w-md text-sm text-slate-500">
              Complete historical market data is
              required for every holding in the
              portfolio.
            </p>
          </div>
        </div>
      )}

      {!isLoading && !error && hasData && (
        <>
          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-[#0B1020] p-4">
              <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
                Starting value
              </p>

              <p className="mt-2 text-lg font-semibold text-white">
                {formatCurrency(
                  performance.starting_value
                )}
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-[#0B1020] p-4">
              <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
                Ending value
              </p>

              <p className="mt-2 text-lg font-semibold text-white">
                {formatCurrency(
                  performance.ending_value
                )}
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-[#0B1020] p-4">
              <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
                Period return
              </p>

              <p
                className={`mt-2 text-lg font-semibold ${getReturnClass(
                  totalReturn
                )}`}
              >
                {formatSignedPercentage(
                  totalReturn
                )}
              </p>
            </div>
          </div>

          <div
            className="mt-8 h-80 w-full"
            aria-label="Historical portfolio value chart"
          >
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <LineChart
                data={chartData}
                margin={{
                  top: 10,
                  right: 10,
                  left: 0,
                  bottom: 0,
                }}
              >
                <CartesianGrid
                  stroke="rgba(148, 163, 184, 0.08)"
                  vertical={false}
                />

                <XAxis
                  dataKey="date"
                  tickFormatter={formatDate}
                  stroke="#64748B"
                  tickLine={false}
                  axisLine={false}
                  minTickGap={32}
                  fontSize={12}
                />

                <YAxis
                  tickFormatter={
                    formatCompactCurrency
                  }
                  stroke="#64748B"
                  tickLine={false}
                  axisLine={false}
                  width={70}
                  fontSize={12}
                />

                <Tooltip
                  content={
                    <PerformanceTooltip />
                  }
                />

                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#22D3EE"
                  strokeWidth={2.5}
                  dot={false}
                  activeDot={{
                    r: 5,
                    fill: "#7C3AED",
                    stroke: "#F8FAFC",
                    strokeWidth: 2,
                  }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-8">
            <div>
              <h4 className="text-sm font-semibold text-white">
                Performance metrics
              </h4>

              <p className="mt-1 text-sm text-slate-400">
                Return and risk statistics calculated
                from the historical portfolio series.
              </p>
            </div>

            <div className="mt-4 grid gap-4 sm:grid-cols-3">
              <div className="rounded-xl border border-white/10 bg-[#0B1020] p-4">
                <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
                  Annualised return
                </p>

                <p
                  className={`mt-2 text-lg font-semibold ${getReturnClass(
                    annualisedReturn
                  )}`}
                >
                  {formatSignedPercentage(
                    annualisedReturn
                  )}
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-500">
                  Selected-period return expressed as
                  an annual equivalent.
                </p>
              </div>

              <div className="rounded-xl border border-white/10 bg-[#0B1020] p-4">
                <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
                  Annualised volatility
                </p>

                <p className="mt-2 text-lg font-semibold text-white">
                  {formatPercentage(
                    annualisedVolatility
                  )}
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-500">
                  Variability of daily portfolio
                  returns, annualised over 365 days.
                </p>
              </div>

              <div className="rounded-xl border border-white/10 bg-[#0B1020] p-4">
                <p className="text-xs uppercase tracking-[0.12em] text-slate-500">
                  Maximum drawdown
                </p>

                <p
                  className={`mt-2 text-lg font-semibold ${getReturnClass(
                    maximumDrawdown
                  )}`}
                >
                  {formatSignedPercentage(
                    maximumDrawdown
                  )}
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-500">
                  Largest peak-to-trough decline
                  during the selected period.
                </p>
              </div>
            </div>
          </div>

          <p className="mt-6 text-xs leading-5 text-slate-500">
            This analysis applies your current holding
            quantities to historical market prices.
            It does not represent your actual
            transaction history or past account
            balance.
          </p>
        </>
      )}
    </section>
  );
}


export default PortfolioPerformance;