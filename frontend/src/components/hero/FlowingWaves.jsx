function FlowingWaves() {
  return (
    <div
      className="pointer-events-none absolute inset-0 z-0 overflow-hidden"
      aria-hidden="true"
    >
      <svg
        className="h-full w-full"
        viewBox="0 0 800 520"
        preserveAspectRatio="xMidYMid meet"
      >
        <defs>
          <linearGradient id="waveGradientA" x1="0%" y1="50%" x2="100%" y2="50%">
            <stop offset="0%" stopColor="#7c3aed" stopOpacity="0" />
            <stop offset="35%" stopColor="#8b5cf6" stopOpacity="0.7" />
            <stop offset="70%" stopColor="#3b82f6" stopOpacity="0.65" />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0" />
          </linearGradient>

          <linearGradient id="waveGradientB" x1="0%" y1="50%" x2="100%" y2="50%">
            <stop offset="0%" stopColor="#2563eb" stopOpacity="0" />
            <stop offset="45%" stopColor="#60a5fa" stopOpacity="0.45" />
            <stop offset="75%" stopColor="#a78bfa" stopOpacity="0.55" />
            <stop offset="100%" stopColor="#7c3aed" stopOpacity="0" />
          </linearGradient>

          <filter id="waveGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <g className="wave-group wave-group-a" filter="url(#waveGlow)">
          <path
            className="energy-wave energy-wave-a"
            d="M -100 355
               C 40 290, 140 420, 280 345
               S 500 250, 650 330
               S 820 410, 950 300"
            fill="none"
            stroke="url(#waveGradientA)"
            strokeWidth="3"
            strokeLinecap="round"
          />

          <path
            className="energy-wave energy-wave-a-secondary"
            d="M -120 390
               C 20 330, 160 440, 300 375
               S 510 290, 670 365
               S 830 430, 960 335"
            fill="none"
            stroke="url(#waveGradientA)"
            strokeWidth="1.5"
            strokeLinecap="round"
            opacity="0.55"
          />
        </g>

        <g className="wave-group wave-group-b" filter="url(#waveGlow)">
          <path
            className="energy-wave energy-wave-b"
            d="M -100 305
               C 80 240, 165 360, 320 300
               S 540 205, 690 275
               S 835 350, 960 250"
            fill="none"
            stroke="url(#waveGradientB)"
            strokeWidth="2"
            strokeLinecap="round"
            opacity="0.75"
          />
        </g>
      </svg>
    </div>
  );
}

export default FlowingWaves;