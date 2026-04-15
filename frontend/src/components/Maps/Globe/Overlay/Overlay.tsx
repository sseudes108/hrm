import { useRef, useMemo } from 'react';
import { useLoader } from '@react-three/fiber';
import * as THREE from 'three';
import { OverlayShader } from './OverlayMaterial';
import { useGlobalRotation } from '../Control/Controller';

interface GlobeOverlayProps {
  textureUrl: string;
  activeTheme: any;
  isLocked: boolean;
}

export function Overlay({ textureUrl, activeTheme, isLocked }: GlobeOverlayProps) {
  const linesTexture = useLoader(THREE.TextureLoader, textureUrl);
  const overlayMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader: OverlayShader.vertexShader,
      fragmentShader: OverlayShader.fragmentShader,
      uniforms: {
        uMap: { value: linesTexture },
        uColor: { value: new THREE.Color(activeTheme.primary) },
        uTime: { value: 0 },
      },
      transparent: true,
      side: THREE.FrontSide,
      depthWrite: false,
      depthTest: true,
    });
  }, [activeTheme.primary, linesTexture]);

  const meshRef = useRef<THREE.Mesh>(null!);
  useGlobalRotation(meshRef, overlayMaterial, isLocked)

  return (
    <mesh ref={meshRef} renderOrder={10}>
      <sphereGeometry args={[102.3, 128, 128]} />
      <primitive object={overlayMaterial} attach="material" />
    </mesh>
  );
}