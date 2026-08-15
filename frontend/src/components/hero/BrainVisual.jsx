import {
  motion,
  useMotionValue,
  useReducedMotion,
  useSpring,
} from "framer-motion";

import { useRef } from "react";

import { LuBrainCircuit } from "react-icons/lu";

function BrainVisual() {
  const shouldReduceMotion = useReducedMotion();
  const containerRef = useRef(null);

  const rotateX = useMotionValue(0);
  const rotateY = useMotionValue(0);

  const smoothRotateX = useSpring(rotateX, {
    stiffness: 80,
    damping: 20,
    mass: 0.8,
  });

  const smoothRotateY = useSpring(rotateY, {
    stiffness: 80,
    damping: 20,
    mass: 0.8,
  });

  function handleMouseMove(event) {
    if (shouldReduceMotion) return;

    const bounds = containerRef.current?.getBoundingClientRect();

    if (!bounds) return;

    const x = event.clientX - bounds.left;
    const y = event.clientY - bounds.top;

    const xPercent = x / bounds.width - 0.5;
    const yPercent = y / bounds.height - 0.5;

    rotateY.set(xPercent * 6);
    rotateX.set(yPercent * -6);
  }

  function handleMouseLeave() {
    rotateX.set(0);
    rotateY.set(0);
  }

  return (
    <motion.div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        rotateX: smoothRotateX,
        rotateY: smoothRotateY,
        transformPerspective: 900,
      }}
      className="relative z-10 flex h-64 w-72 items-center justify-center"
    >
      <motion.div
        animate={
            shouldReduceMotion
                ? undefined
                : {
                    scale: [1, 1.025, 1],
                    opacity: [0.95, 1, 0.95],
                  }
        }
        transition={{
          duration: 4.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute h-72 w-80 rounded-[45%]
                   bg-gradient-to-br from-violet-500/25
                   via-blue-500/15 to-cyan-400/5 blur-2xl"
      />

      <motion.div
        animate={
            shouldReduceMotion
                ? undefined
                : {
                    boxShadow: [
                        "0 0 55px rgba(99,102,241,0.22)",
                        "0 0 95px rgba(124,58,237,0.38)",
                        "0 0 55px rgba(99,102,241,0.22)",
                    ],
                }
        }
        transition={{
          duration: 4.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="relative flex h-64 w-72 items-center justify-center
                   rounded-[44%] border border-violet-300/20
                   bg-gradient-to-br from-violet-500/10
                   via-blue-500/5 to-transparent
                   backdrop-blur-sm"
      >
        <div
          className="absolute inset-4 rounded-[44%]
                     border border-blue-300/10"
        />

        <motion.div
          animate={
            shouldReduceMotion
                ? undefined
                : {
                    scale: [1, 1.02, 1],
                }
            }
          transition={{
            duration: 4.5,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <LuBrainCircuit
            aria-hidden="true"
            className="relative text-[11rem] text-violet-200
                       drop-shadow-[0_0_30px_rgba(167,139,250,0.7)]"
          />
        </motion.div>
      </motion.div>
    </motion.div>
  );
}

export default BrainVisual;