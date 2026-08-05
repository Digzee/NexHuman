function HeroVisual() {
  return (
    <div
      className="relative mx-auto flex min-h-[360px] w-full max-w-2xl
                 items-center justify-center lg:min-h-[480px]"
      aria-label="Future interactive brain and cryptocurrency animation"
    >
      {/* Background glow */}
      <div className="absolute h-80 w-80 rounded-full bg-violet-600/20 blur-3xl" />
      <div className="absolute h-64 w-64 rounded-full bg-blue-600/20 blur-3xl" />

      {/* Holographic platform */}
      <div
        className="absolute bottom-14 h-12 w-72 rounded-[100%]
                   border border-violet-400/30 bg-violet-500/10
                   shadow-[0_0_70px_rgba(124,58,237,0.4)]"
      />

      {/* Temporary brain placeholder */}
      <div
        className="relative flex h-60 w-72 items-center justify-center
                   rounded-[45%] border border-violet-300/30
                   bg-gradient-to-br from-violet-500/20
                   via-blue-500/10 to-transparent
                   shadow-[0_0_80px_rgba(99,102,241,0.28)]
                   backdrop-blur-sm"
      >
        <div className="absolute inset-5 rounded-[45%] border border-blue-300/20" />

        <div className="relative text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-violet-200">
            Interactive visual
          </p>

          <p className="mt-3 max-w-44 text-sm leading-6 text-slate-400">
            3D brain, flowing waves and orbiting cryptocurrency icons
          </p>
        </div>
      </div>

      {/* Temporary crypto markers */}
      <div
        className="absolute left-[8%] top-[20%] flex h-16 w-16
                   items-center justify-center rounded-full
                   border border-orange-300/30 bg-orange-400/10
                   text-2xl font-bold text-orange-300"
      >
        ₿
      </div>

      <div
        className="absolute right-[10%] top-[18%] flex h-16 w-16
                   items-center justify-center rounded-full
                   border border-violet-300/30 bg-violet-400/10
                   text-2xl text-violet-200"
      >
        Ξ
      </div>

      <div
        className="absolute bottom-[22%] right-[4%] flex h-14 w-14
                   items-center justify-center rounded-full
                   border border-cyan-300/30 bg-cyan-400/10
                   text-xs font-bold text-cyan-200"
      >
        SOL
      </div>
    </div>
  );
}

export default HeroVisual;