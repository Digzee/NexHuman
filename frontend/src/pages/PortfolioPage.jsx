import { useEffect, useState } from "react";
import { FaPlus } from "react-icons/fa6";

import AddAssetForm from "../components/portfolio/AddAssetForm";
import AllocationChart from "../components/portfolio/AllocationChart";
import AssetAllocation from "../components/portfolio/AssetAllocation";
import CreatePortfolioForm from "../components/portfolio/CreatePortfolioForm";
import HoldingsTable from "../components/portfolio/HoldingsTable";
import PortfolioOverview from "../components/portfolio/PortfolioOverview";
import PortfolioPerformance from "../components/portfolio/PortfolioPerformance";
import PortfolioRiskSummary from "../components/portfolio/PortfolioRiskSummary";
import PortfolioSelector from "../components/portfolio/PortfolioSelector";
import { API_BASE_URL } from "../config/api";
import { useAuth } from "../context/AuthContext";


function PortfolioPage() {
  const { authenticatedFetch } = useAuth();

  const [portfolios, setPortfolios] = useState([]);
  const [selectedPortfolio, setSelectedPortfolio] = useState(null);
  const [supportedAssets, setSupportedAssets] = useState([]);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const [isCreating, setIsCreating] = useState(false);
  const [newPortfolioName, setNewPortfolioName] = useState("");
  const [createError, setCreateError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [isAddingAsset, setIsAddingAsset] = useState(false);
  const [assetSymbol, setAssetSymbol] = useState("");
  const [assetQuantity, setAssetQuantity] = useState("");
  const [assetPurchasePrice, setAssetPurchasePrice] = useState("");
  const [assetError, setAssetError] = useState("");
  const [isAddingAssetSubmitting, setIsAddingAssetSubmitting] =
    useState(false);

  const [editingAssetId, setEditingAssetId] = useState(null);
  const [editQuantity, setEditQuantity] = useState("");
  const [editPurchasePrice, setEditPurchasePrice] = useState("");
  const [assetActionError, setAssetActionError] = useState("");
  const [isAssetActionSubmitting, setIsAssetActionSubmitting] =
    useState(false);

  const [valuation, setValuation] = useState(null);
  const [isValuationLoading, setIsValuationLoading] =
    useState(false);
  const [valuationError, setValuationError] = useState("");

  const [performance, setPerformance] = useState(null);
  const [selectedPerformanceDays, setSelectedPerformanceDays] =
    useState(30);
  const [isPerformanceLoading, setIsPerformanceLoading] =
    useState(false);
  const [performanceError, setPerformanceError] = useState("");

  const [risk, setRisk] = useState(null);
  const [isRiskLoading, setIsRiskLoading] = useState(false);
  const [riskError, setRiskError] = useState("");


  async function fetchValuation(portfolioId) {
    setIsValuationLoading(true);
    setValuationError("");

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/${portfolioId}/valuation/`
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load portfolio valuation."
        );
      }

      const data = await response.json();

      setValuation(data);
    } catch {
      setValuation(null);
      setValuationError(
        "We couldn't load the current portfolio valuation."
      );
    } finally {
      setIsValuationLoading(false);
    }
  }


  async function fetchPerformance(
    portfolioId,
    days = selectedPerformanceDays
  ) {
    setIsPerformanceLoading(true);
    setPerformanceError("");

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/${portfolioId}/performance/?days=${days}`
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load historical performance."
        );
      }

      const data = await response.json();

      setPerformance(data);
    } catch {
      setPerformance(null);
      setPerformanceError(
        "We couldn't load the historical portfolio performance."
      );
    } finally {
      setIsPerformanceLoading(false);
    }
  }


  async function fetchRisk(
    portfolioId,
    days = selectedPerformanceDays
  ) {
    setIsRiskLoading(true);
    setRiskError("");

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/${portfolioId}/risk/?days=${days}`
      );

      if (!response.ok) {
        throw new Error(
          "Unable to load portfolio risk."
        );
      }

      const data = await response.json();

      setRisk(data);
    } catch {
      setRisk(null);
      setRiskError(
        "We couldn't load the portfolio risk analysis."
      );
    } finally {
      setIsRiskLoading(false);
    }
  }


  useEffect(() => {
    async function fetchPortfolios() {
      try {
        const response = await authenticatedFetch(
          `${API_BASE_URL}/portfolios/`
        );

        if (!response.ok) {
          throw new Error(
            "Unable to load portfolios."
          );
        }

        const data = await response.json();

        setPortfolios(data);

        if (data.length > 0) {
          setSelectedPortfolio(data[0]);
        }
      } catch {
        setError(
          "We couldn't load your portfolios. Please try again."
        );
      } finally {
        setIsLoading(false);
      }
    }


    async function fetchSupportedAssets() {
      try {
        const response = await authenticatedFetch(
          `${API_BASE_URL}/market-data/cryptocurrencies/`
        );

        if (!response.ok) {
          throw new Error(
            "Unable to load supported cryptocurrencies."
          );
        }

        const data = await response.json();

        setSupportedAssets(data);
      } catch {
        setError(
          "We couldn't load the supported cryptocurrencies. Please try again."
        );
      }
    }


    fetchPortfolios();
    fetchSupportedAssets();

    // authenticatedFetch is provided by AuthContext.
    // These requests should run once when the page mounts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  useEffect(() => {
    if (!selectedPortfolio) {
      setValuation(null);
      return;
    }

    fetchValuation(selectedPortfolio.id);

    // authenticatedFetch is provided by AuthContext.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPortfolio?.id]);


  useEffect(() => {
    if (!selectedPortfolio) {
      setPerformance(null);
      setRisk(null);
      return;
    }

    fetchPerformance(
      selectedPortfolio.id,
      selectedPerformanceDays
    );

    fetchRisk(
      selectedPortfolio.id,
      selectedPerformanceDays
    );

    // authenticatedFetch is provided by AuthContext.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    selectedPortfolio?.id,
    selectedPerformanceDays,
  ]);


  async function handleCreatePortfolio(event) {
    event.preventDefault();

    const name = newPortfolioName.trim();

    if (!name) {
      setCreateError("Enter a portfolio name.");
      return;
    }

    setCreateError("");
    setIsSubmitting(true);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Unable to create portfolio."
        );
      }

      const createdPortfolio = await response.json();

      setPortfolios((currentPortfolios) => [
        createdPortfolio,
        ...currentPortfolios,
      ]);

      setSelectedPortfolio(createdPortfolio);
      setSelectedPerformanceDays(30);
      setNewPortfolioName("");
      setIsCreating(false);
    } catch {
      setCreateError(
        "We couldn't create the portfolio. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  }


  async function handleAddAsset(event) {
    event.preventDefault();

    if (!selectedPortfolio) {
      return;
    }

    const symbol = assetSymbol.trim();
    const quantity = assetQuantity.trim();
    const averagePurchasePrice =
      assetPurchasePrice.trim();

    if (!symbol || !quantity) {
      setAssetError(
        "Select an asset and enter a quantity."
      );
      return;
    }

    setAssetError("");
    setIsAddingAssetSubmitting(true);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/${selectedPortfolio.id}/assets/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            symbol,
            quantity,
            average_purchase_price:
              averagePurchasePrice || null,
          }),
        }
      );

      if (!response.ok) {
        const data = await response.json();

        const symbolError = data.symbol?.[0];

        throw new Error(
          symbolError ||
            "Unable to add this asset."
        );
      }

      const createdAsset = await response.json();

      const updatedPortfolio = {
        ...selectedPortfolio,
        assets: [
          ...selectedPortfolio.assets,
          createdAsset,
        ],
      };

      setSelectedPortfolio(updatedPortfolio);

      setPortfolios((currentPortfolios) =>
        currentPortfolios.map((portfolio) =>
          portfolio.id === updatedPortfolio.id
            ? updatedPortfolio
            : portfolio
        )
      );

      await Promise.all([
        fetchValuation(selectedPortfolio.id),
        fetchPerformance(
          selectedPortfolio.id,
          selectedPerformanceDays
        ),
        fetchRisk(
          selectedPortfolio.id,
          selectedPerformanceDays
        ),
      ]);

      setAssetSymbol("");
      setAssetQuantity("");
      setAssetPurchasePrice("");
      setIsAddingAsset(false);
    } catch (error) {
      setAssetError(
        error.message ||
          "We couldn't add the asset. Please try again."
      );
    } finally {
      setIsAddingAssetSubmitting(false);
    }
  }


  function handleStartEditing(asset) {
    setEditingAssetId(asset.id);
    setEditQuantity(asset.quantity);
    setEditPurchasePrice(
      asset.average_purchase_price || ""
    );
    setAssetActionError("");
  }


  function handleCancelEditing() {
    setEditingAssetId(null);
    setEditQuantity("");
    setEditPurchasePrice("");
    setAssetActionError("");
  }


  async function handleUpdateAsset(assetId) {
    if (!selectedPortfolio) {
      return;
    }

    if (!editQuantity.trim()) {
      setAssetActionError(
        "Enter a quantity."
      );
      return;
    }

    setAssetActionError("");
    setIsAssetActionSubmitting(true);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/${selectedPortfolio.id}/assets/${assetId}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            quantity: editQuantity,
            average_purchase_price:
              editPurchasePrice.trim() || null,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Unable to update this asset."
        );
      }

      const updatedAsset = await response.json();

      const updatedPortfolio = {
        ...selectedPortfolio,
        assets: selectedPortfolio.assets.map(
          (asset) =>
            asset.id === updatedAsset.id
              ? updatedAsset
              : asset
        ),
      };

      setSelectedPortfolio(updatedPortfolio);

      setPortfolios((currentPortfolios) =>
        currentPortfolios.map((portfolio) =>
          portfolio.id === updatedPortfolio.id
            ? updatedPortfolio
            : portfolio
        )
      );

      await Promise.all([
        fetchValuation(selectedPortfolio.id),
        fetchPerformance(
          selectedPortfolio.id,
          selectedPerformanceDays
        ),
        fetchRisk(
          selectedPortfolio.id,
          selectedPerformanceDays
        ),
      ]);

      handleCancelEditing();
    } catch {
      setAssetActionError(
        "We couldn't update the asset. Please try again."
      );
    } finally {
      setIsAssetActionSubmitting(false);
    }
  }


  async function handleDeleteAsset(asset) {
    if (!selectedPortfolio) {
      return;
    }

    const shouldDelete = window.confirm(
      `Remove ${asset.symbol} from ${selectedPortfolio.name}?`
    );

    if (!shouldDelete) {
      return;
    }

    setAssetActionError("");
    setIsAssetActionSubmitting(true);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/portfolios/${selectedPortfolio.id}/assets/${asset.id}/`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Unable to remove this asset."
        );
      }

      const updatedPortfolio = {
        ...selectedPortfolio,
        assets: selectedPortfolio.assets.filter(
          (currentAsset) =>
            currentAsset.id !== asset.id
        ),
      };

      setSelectedPortfolio(updatedPortfolio);

      setPortfolios((currentPortfolios) =>
        currentPortfolios.map((portfolio) =>
          portfolio.id === updatedPortfolio.id
            ? updatedPortfolio
            : portfolio
        )
      );

      await Promise.all([
        fetchValuation(selectedPortfolio.id),
        fetchPerformance(
          selectedPortfolio.id,
          selectedPerformanceDays
        ),
        fetchRisk(
          selectedPortfolio.id,
          selectedPerformanceDays
        ),
      ]);

      if (editingAssetId === asset.id) {
        handleCancelEditing();
      }
    } catch {
      setAssetActionError(
        "We couldn't remove the asset. Please try again."
      );
    } finally {
      setIsAssetActionSubmitting(false);
    }
  }


  return (
    <section>
      <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-cyan-400">
            Portfolio
          </p>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">
            Your portfolio
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
            Manage your cryptocurrency holdings and track how
            your portfolio changes over time.
          </p>
        </div>

        <button
          type="button"
          onClick={() => {
            setIsCreating(true);
            setCreateError("");
          }}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:opacity-90"
        >
          <FaPlus aria-hidden="true" />
          New portfolio
        </button>
      </div>


      {isCreating && (
        <CreatePortfolioForm
          name={newPortfolioName}
          onNameChange={setNewPortfolioName}
          onSubmit={handleCreatePortfolio}
          onCancel={() => {
            setIsCreating(false);
            setNewPortfolioName("");
            setCreateError("");
          }}
          error={createError}
          isSubmitting={isSubmitting}
        />
      )}


      <div className="mt-8">
        {isLoading && (
          <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
            <p className="text-sm text-slate-400">
              Loading portfolios...
            </p>
          </div>
        )}


        {!isLoading && error && (
          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-6">
            <p className="text-sm text-red-300">
              {error}
            </p>
          </div>
        )}


        {!isLoading &&
          !error &&
          portfolios.length === 0 && (
            <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-6">
              <h2 className="text-lg font-semibold text-white">
                No portfolios yet
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Create your first portfolio to begin tracking
                your cryptocurrency investments.
              </p>
            </div>
          )}


        {!isLoading &&
          !error &&
          portfolios.length > 0 && (
            <>
              <PortfolioSelector
                portfolios={portfolios}
                selectedPortfolio={selectedPortfolio}
                onSelect={(portfolio) => {
                  setSelectedPortfolio(portfolio);
                  setSelectedPerformanceDays(30);
                  setEditingAssetId(null);
                  setAssetActionError("");
                  setIsAddingAsset(false);
                  setAssetSymbol("");
                  setAssetQuantity("");
                  setAssetPurchasePrice("");
                  setAssetError("");
                }}
              />


              {selectedPortfolio && (
                <div className="mt-8 rounded-2xl border border-white/10 bg-[#0B1020]">
                  <div className="flex flex-col gap-4 border-b border-white/10 p-6 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-400">
                        Selected portfolio
                      </p>

                      <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white">
                        {selectedPortfolio.name}
                      </h2>

                      <p className="mt-2 text-sm text-slate-400">
                        {selectedPortfolio.assets.length}{" "}
                        {selectedPortfolio.assets.length === 1
                          ? "holding"
                          : "holdings"}
                      </p>
                    </div>

                    <button
                      type="button"
                      onClick={() => {
                        setIsAddingAsset(true);
                        setAssetError("");
                      }}
                      className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-white/5"
                    >
                      <FaPlus aria-hidden="true" />
                      Add asset
                    </button>
                  </div>


                  {isAddingAsset && (
                    <AddAssetForm
                      symbol={assetSymbol}
                      quantity={assetQuantity}
                      purchasePrice={assetPurchasePrice}
                      supportedAssets={supportedAssets}
                      heldSymbols={selectedPortfolio.assets.map(
                        (asset) => asset.symbol
                      )}
                      onSymbolChange={setAssetSymbol}
                      onQuantityChange={setAssetQuantity}
                      onPurchasePriceChange={
                        setAssetPurchasePrice
                      }
                      onSubmit={handleAddAsset}
                      onCancel={() => {
                        setIsAddingAsset(false);
                        setAssetSymbol("");
                        setAssetQuantity("");
                        setAssetPurchasePrice("");
                        setAssetError("");
                      }}
                      error={assetError}
                      isSubmitting={
                        isAddingAssetSubmitting
                      }
                    />
                  )}


                  <div className="p-6">
                    <PortfolioOverview
                      valuation={valuation}
                      isLoading={isValuationLoading}
                      error={valuationError}
                    />

                    <PortfolioPerformance
                      performance={performance}
                      selectedDays={
                        selectedPerformanceDays
                      }
                      onPeriodChange={
                        setSelectedPerformanceDays
                      }
                      isLoading={
                        isPerformanceLoading
                      }
                      error={performanceError}
                    />

                    <div className="mt-8">
                      <PortfolioRiskSummary
                        risk={risk}
                        isLoading={isRiskLoading}
                        error={riskError}
                      />
                    </div>

                    <AllocationChart
                      valuation={valuation}
                    />

                    <AssetAllocation
                      valuation={valuation}
                    />

                    <div className="mt-8">
                      <HoldingsTable
                        assets={
                          selectedPortfolio.assets
                        }
                        editingAssetId={
                          editingAssetId
                        }
                        editQuantity={
                          editQuantity
                        }
                        editPurchasePrice={
                          editPurchasePrice
                        }
                        onEditQuantityChange={
                          setEditQuantity
                        }
                        onEditPurchasePriceChange={
                          setEditPurchasePrice
                        }
                        onStartEditing={
                          handleStartEditing
                        }
                        onCancelEditing={
                          handleCancelEditing
                        }
                        onUpdateAsset={
                          handleUpdateAsset
                        }
                        onDeleteAsset={
                          handleDeleteAsset
                        }
                        error={
                          assetActionError
                        }
                        isSubmitting={
                          isAssetActionSubmitting
                        }
                      />
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
      </div>
    </section>
  );
}


export default PortfolioPage;