function CreatePortfolioForm({
  name,
  onNameChange,
  onSubmit,
  onCancel,
  error,
  isSubmitting,
}) {
  return (
    <form
      onSubmit={onSubmit}
      className="mt-8 rounded-2xl border border-white/10 bg-[#0B1020] p-6"
    >
      <label
        htmlFor="portfolio-name"
        className="text-sm font-medium text-white"
      >
        Portfolio name
      </label>

      <input
        id="portfolio-name"
        type="text"
        maxLength={100}
        value={name}
        onChange={(event) =>
          onNameChange(event.target.value)
        }
        placeholder="e.g. Long-term portfolio"
        className="mt-3 w-full rounded-xl border border-white/10 bg-[#050816] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400/60"
      />

      {error && (
        <p role="alert" className="mt-3 text-sm text-red-300">
          {error}
        </p>
      )}

      <div className="mt-5 flex flex-wrap gap-3">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-[#050816] transition hover:bg-slate-200 disabled:opacity-60"
        >
          {isSubmitting ? "Creating..." : "Create portfolio"}
        </button>

        <button
          type="button"
          onClick={onCancel}
          className="rounded-xl border border-white/10 px-4 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-white/5"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

export default CreatePortfolioForm;