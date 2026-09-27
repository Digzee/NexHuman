function PortfolioSelector({
  portfolios,
  selectedPortfolio,
  onSelect,
}) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {portfolios.map((portfolio) => {
        const isSelected =
          selectedPortfolio?.id === portfolio.id;

        return (
          <button
            key={portfolio.id}
            type="button"
            onClick={() => onSelect(portfolio)}
            aria-pressed={isSelected}
            className={[
              "rounded-2xl border p-6 text-left transition",
              isSelected
                ? "border-cyan-400/50 bg-cyan-400/5"
                : "border-white/10 bg-[#0B1020] hover:border-white/20",
            ].join(" ")}
          >
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
              Portfolio
            </p>

            <h2 className="mt-2 text-lg font-semibold text-white">
              {portfolio.name}
            </h2>

            <p className="mt-3 text-sm text-slate-400">
              {portfolio.assets.length}{" "}
              {portfolio.assets.length === 1
                ? "asset"
                : "assets"}
            </p>

            {isSelected && (
              <p className="mt-4 text-xs font-medium text-cyan-400">
                Selected
              </p>
            )}
          </button>
        );
      })}
    </div>
  );
}

export default PortfolioSelector;