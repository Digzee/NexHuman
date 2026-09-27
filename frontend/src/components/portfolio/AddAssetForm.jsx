function AddAssetForm({
  symbol,
  quantity,
  purchasePrice,
  supportedAssets,
  heldSymbols,
  onSymbolChange,
  onQuantityChange,
  onPurchasePriceChange,
  onSubmit,
  onCancel,
  error,
  isSubmitting,
}) {
  return (
    <form
      onSubmit={onSubmit}
      className="border-b border-white/10 p-6"
    >
      <h3 className="text-base font-semibold text-white">
        Add holding
      </h3>

      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <div>
          <label
            htmlFor="asset-symbol"
            className="text-sm font-medium text-slate-300"
          >
            Asset
          </label>

          <select
            id="asset-symbol"
            value={symbol}
            onChange={(event) =>
              onSymbolChange(event.target.value)
            }
            className="mt-2 w-full rounded-xl border border-white/10 bg-[#050816] px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400/60"
          >
            <option value="">
              Select an asset
            </option>

            {supportedAssets.map((asset) => {
              const isHeld = heldSymbols.includes(
                asset.symbol
              );

              return (
                <option
                  key={asset.id}
                  value={asset.symbol}
                  disabled={isHeld}
                >
                  {asset.name} ({asset.symbol})
                  {isHeld ? " — already added" : ""}
                </option>
              );
            })}
          </select>
        </div>

        <div>
          <label
            htmlFor="asset-quantity"
            className="text-sm font-medium text-slate-300"
          >
            Quantity
          </label>

          <input
            id="asset-quantity"
            type="number"
            min="0"
            step="any"
            value={quantity}
            onChange={(event) =>
              onQuantityChange(event.target.value)
            }
            placeholder="0.25"
            className="mt-2 w-full rounded-xl border border-white/10 bg-[#050816] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400/60"
          />
        </div>

        <div>
          <label
            htmlFor="asset-purchase-price"
            className="text-sm font-medium text-slate-300"
          >
            Average purchase price
          </label>

          <input
            id="asset-purchase-price"
            type="number"
            min="0"
            step="any"
            value={purchasePrice}
            onChange={(event) =>
              onPurchasePriceChange(event.target.value)
            }
            placeholder="65000"
            className="mt-2 w-full rounded-xl border border-white/10 bg-[#050816] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400/60"
          />
        </div>
      </div>

      {error && (
        <p
          role="alert"
          className="mt-4 text-sm text-red-300"
        >
          {error}
        </p>
      )}

      <div className="mt-5 flex flex-wrap gap-3">
        <button
          type="submit"
          disabled={isSubmitting || !symbol}
          className="rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-[#050816] transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? "Adding..." : "Add asset"}
        </button>

        <button
          type="button"
          onClick={onCancel}
          className="rounded-xl border border-white/10 px-4 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-white/5 hover:text-white"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}


export default AddAssetForm;