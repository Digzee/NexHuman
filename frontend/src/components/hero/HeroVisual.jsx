import {
  SiBitcoin,
  SiCardano,
  SiEthereum,
  SiSolana,
} from "react-icons/si";
import { LuBrainCircuit } from "react-icons/lu";
import FlowingWaves from "./FlowingWaves";

const cryptoAssets = [
  {
    name: "Bitcoin",
    Icon: SiBitcoin,
    position: "left-[3%] top-[27%]",
    colour:
      "border-orange-300/30 bg-orange-400/10 text-orange-300 shadow-orange-500/20",
  },
  {
    name: "Ethereum",
    Icon: SiEthereum,
    position: "right-[7%] top-[17%]",
    colour:
      "border-indigo-300/30 bg-indigo-400/10 text-indigo-200 shadow-indigo-500/20",
  },
  {
    name: "Solana",
    Icon: SiSolana,
    position: "bottom-[20%] right-[2%]",
    colour:
      "border-cyan-300/30 bg-cyan-400/10 text-cyan-200 shadow-cyan-500/20",
  },
  {
    name: "Cardano",
    Icon: SiCardano,
    position: "bottom-[14%] left-[11%]",
    colour:
      "border-blue-300/30 bg-blue-400/10 text-blue-200 shadow-blue-500/20",
  },
];

function CryptoIcon({ name, Icon, position, colour }) {
  return (
    <div
      aria-label={name}
      className={`absolute ${position} z-20 flex h-16 w-16 items-center
                  justify-center rounded-full border shadow-[0_0_35px]
                  backdrop-blur-md ${colour}`}
    >
      <Icon aria-hidden="true" className="text-3xl" />
    </div>
  );
}

function HeroVisual() {
  return (
    <div
      className="relative mx-auto flex min-h-[420px] w-full max-w-3xl
                 items-center justify-center lg:min-h-[520px]"
      aria-label="NexHuman investment intelligence visual"
    >
      <FlowingWaves />
      
      {/* Ambient lighting */}
      <div
        className="pointer-events-none absolute h-96 w-96 rounded-full
                   bg-violet-600/20 blur-3xl"
      />

      <div
        className="pointer-events-none absolute h-72 w-72 rounded-full
                   bg-blue-600/20 blur-3xl"
      />

      {/* Decorative orbit paths */}
      <div
        className="absolute h-[340px] w-[520px] rotate-[-8deg] rounded-[50%]
                   border border-violet-300/10"
      />

      <div
        className="absolute h-[260px] w-[440px] rotate-[13deg] rounded-[50%]
                   border border-blue-300/10"
      />

      {/* Brain glow */}
      <div
        className="absolute h-72 w-80 rounded-[45%]
                   bg-gradient-to-br from-violet-500/25
                   via-blue-500/15 to-cyan-400/5 blur-2xl"
      />

      {/* Static brain */}
      <div
        className="relative z-10 flex h-64 w-72 items-center justify-center
                   rounded-[44%] border border-violet-300/20
                   bg-gradient-to-br from-violet-500/10
                   via-blue-500/5 to-transparent
                   shadow-[0_0_90px_rgba(99,102,241,0.32)]
                   backdrop-blur-sm"
      >
        <div
          className="absolute inset-4 rounded-[44%]
                     border border-blue-300/10"
        />

        <LuBrainCircuit
          aria-hidden="true"
          className="relative text-[11rem] text-violet-200
                     drop-shadow-[0_0_30px_rgba(167,139,250,0.7)]"
        />
      </div>

      {/* Vertical light beneath brain */}
      <div
        className="absolute bottom-24 h-36 w-36
                   bg-gradient-to-b from-violet-400/20 to-transparent
                   blur-2xl"
      />

      {/* Holographic platform */}
      <div
        className="absolute bottom-16 h-12 w-80 rounded-[100%]
                   border border-violet-300/25 bg-violet-500/10
                   shadow-[0_0_75px_rgba(124,58,237,0.5)]"
      />

      <div
        className="absolute bottom-[4.6rem] h-5 w-64 rounded-[100%]
                   border border-blue-300/20 bg-blue-400/10 blur-[1px]"
      />

      {cryptoAssets.map((asset) => (
        <CryptoIcon key={asset.name} {...asset} />
      ))}

      {/* Small data particles */}
      <div className="absolute left-[28%] top-[15%] h-1.5 w-1.5 rounded-full bg-violet-300 shadow-[0_0_12px_rgba(196,181,253,0.9)]" />
      <div className="absolute right-[29%] top-[29%] h-1 w-1 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(103,232,249,0.9)]" />
      <div className="absolute bottom-[28%] left-[33%] h-1 w-1 rounded-full bg-blue-300 shadow-[0_0_10px_rgba(147,197,253,0.9)]" />
    </div>
  );
}

export default HeroVisual;