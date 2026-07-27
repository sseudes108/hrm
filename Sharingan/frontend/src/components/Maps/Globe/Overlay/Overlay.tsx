import { useMemo } from 'react';
import { useLoader } from '@react-three/fiber';
import * as THREE from 'three';
import { createOverlayMaterial, OVERLAY_CONTROLS } from './OverlayMaterial';
import { useTheme } from '../../../../context/useTheme';

interface GlobeOverlayProps { textureUrl: string }

// Camada base: somente a placa translúcida que acompanha o contorno dos continentes.
export function Overlay({ textureUrl }: GlobeOverlayProps) {
  const { theme } = useTheme();
  const linesTexture = useLoader(THREE.TextureLoader, textureUrl);
  const material = useMemo(() => createOverlayMaterial(linesTexture, theme.primary), [linesTexture, theme.primary]);

  return <mesh renderOrder={10}><sphereGeometry args={[OVERLAY_CONTROLS.sphereRadius, 128, 128]} /><primitive object={material} attach="material" /></mesh>;
}
