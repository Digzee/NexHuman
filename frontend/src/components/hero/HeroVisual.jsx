import { useState } from "react";
import { motion, useReducedMotion } from "framer-motion";

import {
  SiBitcoin,
  SiCardano,
  SiEthereum,
  SiSolana,
} from "react-icons/si";

import BrainScene from "./BrainScene";
import FlowingWaves from "./FlowingWaves";

const cryptoAssets = [
  {
    name: "Bitcoin",
    Icon: SiBitcoin,
    position: "left-[3%] top-[27%]",
    delay: "0s",
    colour:
      "border-orange-300/30 bg-orange-400/10 text-orange-300 shadow-orange-500/20",
  },
  {
    name: "Ethereum",
    Icon: SiEthereum,
    position: "right-[7%] top-[17%]",
    delay: "-1.5s",
    colour:
      "border-indigo-300/30 bg-indigo-400/10 text-indigo-200 shadow-indigo-500/20",
  },
  {
    name: "Solana",
    Icon: SiSolana,
    position: "bottom-[20%] right-[2%]",
    delay: "-3s",
    colour:
      "border-cyan-300/30 bg-cyan-400/10 text-cyan-200 shadow-cyan-500/20",
  },
  {
    name: "Cardano",
    Icon: SiCardano,
    position: "bottom-[14%] left-[11%]",
    delay: "-4.5s",
    colour:
      "border-blue-300/30 bg-blue-400/10 text-blue-200 shadow-blue-500/20",
  },
];

function CryptoIcon({ name, Icon, position, colour, delay = "0s" }) {
  const [isSpinning, setIsSpinning] = useState(false);

  function handleSpin() {
    if (isSpinning) return;

    setIsSpinning(true);

    window.setTimeout(() => {
      setIsSpinning(false);
    }, 700);
  }

  return (
    <motion.button
      type="button"
      aria-label={`Spin ${name} icon`}
      onClick={handleSpin}
      style={{ "--float-delay": delay }}

      initial={{
        opacity: 0,
        scale: 0.7,
        y: 12,
      }}
      animate={{
        opacity: 1,
        scale: 1,
        y: 0,
      }}
      transition={{
        duration: 0.7,
        delay: 2.2,
        ease: [0.22, 1, 0.36, 1],
      }}
      
      className={`crypto-icon absolute ${position} z-20 flex h-16 w-16
                  cursor-pointer items-center justify-center rounded-full
                  border shadow-[0_0_35px] backdrop-blur-md
                  transition-transform duration-300
                  hover:scale-110 focus:outline-none focus:ring-2
                  focus:ring-violet-400 focus:ring-offset-2
                  focus:ring-offset-[#050816]
                  ${isSpinning ? "crypto-icon-spin" : ""}
                  ${colour}`}
    >
      <Icon aria-hidden="true" className="text-3xl" />
    </motion.button>
  );
}

function HeroVisual() {
  const shouldReduceMotion = useReducedMotion();
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

      <motion.div
        initial={shouldReduceMotion ? false : { opacity: 0, scale: 0.94 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{
          duration: 1,
          delay: shouldReduceMotion ? 0 : 1.3,
          ease: [0.22, 1, 0.36, 1],
        }}
        className="relative z-10"
      >
        <BrainScene />
      </motion.div>

      {/* Vertical light beneath brain */}
      <div
        className="absolute bottom-24 h-36 w-36
                   bg-gradient-to-b from-violet-400/20 to-transparent
                   blur-2xl"
      />
      
      <motion.div
        initial={shouldReduceMotion ? false : { opacity: 0, scaleX: 0.65 }}
        animate={{ opacity: 1, scaleX: 1 }}
        transition={{
          duration: 0.8,
          delay: shouldReduceMotion ? 0 : 1.6,
          ease: [0.22, 1, 0.36, 1],
        }}
        className="pointer-events-none absolute inset-0 origin-center"
      >
        {/* Holographic platform */}
        <div
          className="absolute bottom-16 left-1/2 h-12 w-80
                    -translate-x-1/2 rounded-[100%]
                    border border-violet-300/25 bg-violet-500/10
                    shadow-[0_0_75px_rgba(124,58,237,0.5)]"
        />

        <div
          className="absolute bottom-[4.6rem] left-1/2 h-5 w-64
                    -translate-x-1/2 rounded-[100%]
                    border border-blue-300/20 bg-blue-400/10 blur-[1px]"
        />
      </motion.div>



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