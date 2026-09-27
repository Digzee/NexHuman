import {
  FaPen,
  FaTrash,
} from "react-icons/fa6";


function HoldingsTable({
  assets,
  editingAssetId,
  editQuantity,
  editPurchasePrice,
  onEditQuantityChange,
  onEditPurchasePriceChange,
  onStartEditing,
  onCancelEditing,
  onUpdateAsset,
  onDeleteAsset,
  error,
  isSubmitting,
}) {
  if (assets.length === 0) {
    return (
      <div className="py-8 text-center">
        <h3 className="text-base font-semibold text-white">
          No holdings yet
        </h3>

        <p className="mt-2 text-sm text-slate-400">
          Add a cryptocurrency to start building this
          portfolio.
        </p>
      </div>
    );
  }

  return (
    <>
      {error && (
        <p
          role="alert"
          className="mb-4 text-sm text-red-300"
        >
          {error}
        </p>
      )}

      <div className="overflow-x-auto">
        <table className="w-full min-w-[600px] text-left">
          <thead>
            <tr className="border-b border-white/10">
              <th className="pb-3 text-xs font-medium uppercase tracking-wider text-slate-500">
                Asset
              </th>

              <th className="pb-3 text-xs font-medium uppercase tracking-wider text-slate-500">
                Quantity
              </th>

              <th className="pb-3 text-xs font-medium uppercase tracking-wider text-slate-500">
                Avg. purchase price
              </th>

              <th className="pb-3 text-right text-xs font-medium uppercase tracking-wider text-slate-500">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
            {assets.map((asset) => {
              const isEditing =
                editingAssetId === asset.id;

              return (
                <tr
                  key={asset.id}
                  className="border-b border-white/5 last:border-0"
                >
                  <td className="py-4 font-semibold text-white">
                    {asset.symbol}
                  </td>

                  <td className="py-4 pr-4 text-sm text-slate-300">
                    {isEditing ? (
                      <input
                        type="number"
                        min="0"
                        step="any"
                        aria-label={`${asset.symbol} quantity`}
                        value={editQuantity}
                        onChange={(event) =>
                          onEditQuantityChange(
                            event.target.value
                          )
                        }
                        className="w-32 rounded-lg border border-white/10 bg-[#050816] px-3 py-2 text-sm text-white outline-none focus:border-cyan-400/60"
                      />
                    ) : (
                      Number(
                        asset.quantity
                      ).toLocaleString()
                    )}
                  </td>

                  <td className="py-4 pr-4 text-sm text-slate-300">
                    {isEditing ? (
                      <input
                        type="number"
                        min="0"
                        step="any"
                        aria-label={`${asset.symbol} average purchase price`}
                        value={editPurchasePrice}
                        onChange={(event) =>
                          onEditPurchasePriceChange(
                            event.target.value
                          )
                        }
                        className="w-36 rounded-lg border border-white/10 bg-[#050816] px-3 py-2 text-sm text-white outline-none focus:border-cyan-400/60"
                      />
                    ) : asset.average_purchase_price ? (
                      `$${Number(
                        asset.average_purchase_price
                      ).toLocaleString()}`
                    ) : (
                      "—"
                    )}
                  </td>

                  <td className="py-4">
                    <div className="flex justify-end gap-2">
                      {isEditing ? (
                        <>
                          <button
                            type="button"
                            disabled={isSubmitting}
                            onClick={() =>
                              onUpdateAsset(asset.id)
                            }
                            className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-[#050816] transition hover:bg-slate-200 disabled:opacity-60"
                          >
                            Save
                          </button>

                          <button
                            type="button"
                            disabled={isSubmitting}
                            onClick={onCancelEditing}
                            className="rounded-lg border border-white/10 px-3 py-2 text-xs font-medium text-slate-300 transition hover:bg-white/5"
                          >
                            Cancel
                          </button>
                        </>
                      ) : (
                        <>
                          <button
                            type="button"
                            onClick={() =>
                              onStartEditing(asset)
                            }
                            aria-label={`Edit ${asset.symbol}`}
                            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-white/5 hover:text-white"
                          >
                            <FaPen aria-hidden="true" />
                          </button>

                          <button
                            type="button"
                            onClick={() =>
                              onDeleteAsset(asset)
                            }
                            aria-label={`Remove ${asset.symbol}`}
                            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-500/10 hover:text-red-300"
                          >
                            <FaTrash aria-hidden="true" />
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}


export default HoldingsTable;