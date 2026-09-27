import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";


const CHART_COLOURS = [
  "#7C3AED",
  "#2563EB",
  "#22D3EE",
  "#8B5CF6",
  "#06B6D4",
];


function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value));
}


function AllocationTooltip({
  active,
  payload,
}) {
  if (!active || !payload?.length) {
    return null;
  }

  const asset = payload[0].payload;

  return (
    <div className="rounded-xl border border-white/10 bg-[#0B1020] px-4 py-3 shadow-xl">
      <p className="font-semibold text-white">
        {asset.symbol}
      </p>

      <p className="mt-1 text-sm text-slate-300">
        {formatCurrency(asset.currentValue)}
      </p>

      <p className="mt-1 text-sm text-cyan-400">
        {asset.allocation.toFixed(2)}%
      </p>
    </div>
  );
}


function AllocationChart({ valuation }) {
  if (!valuation || valuation.assets.length === 0) {
    return null;
  }

  const chartData = valuation.assets
    .map((asset) => ({
      symbol: asset.symbol,
      allocation: Number(
        asset.allocation_percentage
      ),
      currentValue: Number(
        asset.current_value
      ),
    }))
    .sort(
      (firstAsset, secondAsset) =>
        secondAsset.allocation -
        firstAsset.allocation
    );

  return (
    <section
      aria-labelledby="allocation-chart-heading"
      className="mt-8 rounded-2xl border border-white/10 bg-[#11172A] p-6"
    >
      <div>
        <h3
          id="allocation-chart-heading"
          className="text-base font-semibold text-white"
        >
          Portfolio composition
        </h3>

        <p className="mt-1 text-sm text-slate-400">
          Visual breakdown of your current portfolio
          by market value.
        </p>
      </div>

      <div className="mt-6 grid items-center gap-8 lg:grid-cols-[minmax(0,1fr)_220px]">
        <div
          className="h-72 w-full"
          aria-label="Portfolio allocation chart"
        >
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <PieChart>
              <Pie
                data={chartData}
                dataKey="allocation"
                nameKey="symbol"
                cx="50%"
                cy="50%"
                innerRadius={75}
                outerRadius={110}
                paddingAngle={3}
                stroke="none"
              >
                {chartData.map((asset, index) => (
                  <Cell
                    key={asset.symbol}
                    fill={
                      CHART_COLOURS[
                        index %
                          CHART_COLOURS.length
                      ]
                    }
                  />
                ))}
              </Pie>

              <Tooltip
                content={<AllocationTooltip />}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-3">
          {chartData.map((asset, index) => (
            <div
              key={asset.symbol}
              className="flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-3">
                <span
                  className="h-2.5 w-2.5 rounded-full"
                  style={{
                    backgroundColor:
                      CHART_COLOURS[
                        index %
                          CHART_COLOURS.length
                      ],
                  }}
                  aria-hidden="true"
                />

                <span className="text-sm font-medium text-slate-200">
                  {asset.symbol}
                </span>
              </div>

              <span className="text-sm text-slate-400">
                {asset.allocation.toFixed(2)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}


export default AllocationChart;