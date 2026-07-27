import { useFrame } from '@react-three/fiber';
import type { RefObject } from 'react';
import * as THREE from 'three';

function updateShaderTime(material: THREE.ShaderMaterial, elapsedTime: number) {
  const timeUniform = material.uniforms.uTime;
  if (timeUniform) {
    timeUniform.value = elapsedTime;
  }
}

export function useShaderTime(material: THREE.ShaderMaterial) {
  useFrame((state) => {
    updateShaderTime(material, state.clock.getElapsedTime());
  });
}

export function useSharedGlobeRotation(
  globeRef: RefObject<THREE.Object3D | null>,
  isLocked: boolean,
) {
  useFrame((_, delta) => {
    if (globeRef.current) {
      const speed = isLocked ? 0 : 0.01;
      globeRef.current.rotation.y += speed * delta;
    }
  });
}

/** @deprecated Use useShaderTime and useSharedGlobeRotation separately. */
export function useGlobalRotation(
  meshRef: RefObject<THREE.Object3D | null>,
  material: THREE.ShaderMaterial,
  isLocked: boolean,
) {
  useFrame((state, delta) => {
    if (meshRef.current && material) {
      const speed = isLocked ? 0 : 0.01;
      
      // Compatibilidade temporária para componentes externos legados.
      meshRef.current.rotation.y += speed * delta;
      updateShaderTime(material, state.clock.getElapsedTime());
    }
  });
}
