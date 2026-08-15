import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Sparkles } from "@react-three/drei";
import * as THREE from "three";

function BrainCore() {
  const groupRef = useRef();

  useFrame((state) => {
    if (!groupRef.current) return;

    const targetX = state.pointer.y * 0.12;
    const targetY = state.pointer.x * 0.18;

    groupRef.current.rotation.x = THREE.MathUtils.lerp(
      groupRef.current.rotation.x,
      targetX,
      0.04,
    );

    groupRef.current.rotation.y = THREE.MathUtils.lerp(
      groupRef.current.rotation.y,
      targetY,
      0.04,
    );
  });

  return (
    <group ref={groupRef} rotation={[0.08, -0.15, 0]}>
      <Float
        speed={1}
        rotationIntensity={0.08}
        floatIntensity={0.22}
        floatingRange={[-0.08, 0.08]}
      >
        <mesh position={[-0.72, 0, 0]} scale={[1, 1.15, 0.9]}>
          <icosahedronGeometry args={[1.05, 4]} />

          <meshStandardMaterial
            color="#8b5cf6"
            emissive="#5b21b6"
            emissiveIntensity={0.65}
            roughness={0.32}
            metalness={0.15}
            wireframe
          />
        </mesh>

        <mesh position={[0.72, 0, 0]} scale={[1, 1.15, 0.9]}>
          <icosahedronGeometry args={[1.05, 4]} />

          <meshStandardMaterial
            color="#6366f1"
            emissive="#4338ca"
            emissiveIntensity={0.65}
            roughness={0.32}
            metalness={0.15}
            wireframe
          />
        </mesh>

        <mesh
          position={[-0.68, 0, 0]}
          scale={[0.92, 1.06, 0.82]}
        >
          <icosahedronGeometry args={[1, 3]} />

          <meshPhysicalMaterial
            color="#7c3aed"
            emissive="#4c1d95"
            emissiveIntensity={0.22}
            transparent
            opacity={0.16}
            roughness={0.18}
            transmission={0.15}
          />
        </mesh>

        <mesh
          position={[0.68, 0, 0]}
          scale={[0.92, 1.06, 0.82]}
        >
          <icosahedronGeometry args={[1, 3]} />

          <meshPhysicalMaterial
            color="#2563eb"
            emissive="#1e40af"
            emissiveIntensity={0.22}
            transparent
            opacity={0.16}
            roughness={0.18}
            transmission={0.15}
          />
        </mesh>
      </Float>
    </group>
  );
}

function BrainScene() {
  return (
    <div
      className="relative z-10 h-72 w-80 sm:h-80 sm:w-96"
      aria-label="Interactive three-dimensional neural brain visual"
    >
      <Canvas
        camera={{
          position: [0, 0, 5],
          fov: 42,
        }}
        dpr={[1, 1.5]}
        gl={{
          alpha: true,
          antialias: true,
          powerPreference: "high-performance",
        }}
      >
        <ambientLight intensity={0.7} />

        <pointLight
          position={[3, 3, 4]}
          intensity={20}
          color="#a78bfa"
        />

        <pointLight
          position={[-3, -1, 3]}
          intensity={14}
          color="#2563eb"
        />

        <pointLight
          position={[0, -3, 2]}
          intensity={8}
          color="#22d3ee"
        />

        <BrainCore />

        <Sparkles
          count={35}
          scale={[4, 3, 2]}
          size={1.5}
          speed={0.15}
          opacity={0.35}
          color="#c4b5fd"
        />
      </Canvas>
    </div>
  );
}

export default BrainScene;