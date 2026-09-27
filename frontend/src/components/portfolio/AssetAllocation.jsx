function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value));
}


function AssetAllocation({ valuation }) {
  if (!valuation || valuation.assets.length === 0) {
    return null;
  }

  const assets = [...valuation.assets].sort(
    (firstAsset, secondAsset) =>
      Number(secondAsset.allocation_percentage) -
      Number(firstAsset.allocation_percentage)
  );

  return (
    <section
      aria-labelledby="asset-allocation-heading"
      className="mt-8"
    >
      <div className="mb-5">
        <h3
          id="asset-allocation-heading"
          className="text-base font-semibold text-white"
        >
          Asset allocation
        </h3>

        <p className="mt-1 text-sm text-slate-400">
          How your portfolio value is distributed across
          your cryptocurrency holdings.
        </p>
      </div>

      <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#11172A]">
        <div className="hidden grid-cols-[1fr_1fr_1fr] gap-4 border-b border-white/10 px-5 py-3 text-xs font-medium uppercase tracking-[0.14em] text-slate-500 sm:grid">
          <span>Asset</span>
          <span>Current value</span>
          <span>Allocation</span>
        </div>

        <div className="divide-y divide-white/10">
          {assets.map((asset) => {
            const allocation = Number(
              asset.allocation_percentage
            );

            return (
              <div
                key={asset.id}
                className="grid gap-4 px-5 py-4 sm:grid-cols-[1fr_1fr_1fr] sm:items-center"
              >
                <div>
                  <p className="font-semibold text-white">
                    {asset.symbol}
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-500 sm:hidden">
                    Current value
                  </p>

                  <p className="mt-1 text-sm text-slate-200 sm:mt-0">
                    {formatCurrency(
                      asset.current_value
                    )}
                  </p>
                </div>

                <div>
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-sm font-medium text-white">
                      {allocation.toFixed(2)}%
                    </span>
                  </div>

                  <div
                    className="mt-2 h-2 overflow-hidden rounded-full bg-white/5"
                    role="progressbar"
                    aria-label={`${asset.symbol} allocation`}
                    aria-valuemin="0"
                    aria-valuemax="100"
                    aria-valuenow={allocation}
                  >
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-violet-600 to-cyan-400"
                      style={{
                        width: `${Math.min(
                          allocation,
                          100
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}


export default AssetAllocation;