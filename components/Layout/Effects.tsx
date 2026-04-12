import { Bloom, Noise, Vignette, EffectComposer } from '@react-three/postprocessing';
import * as THREE from 'three';

// Método separado para o Bloom
export function BloomEffect() {
  return (
    <Bloom 
      intensity={1.5}
      luminanceThreshold={0.2}
      luminanceSmoothing={0.9}
      mipmapBlur
      radius={0.7}
    />
  );
}

// Método separado para o Noise
export function NoiseEffect() {
  return <Noise opacity={0.03} />;
}

// Método separado para o Vignette
export function VignetteEffect() {
  return <Vignette eskil={false} offset={0.1} darkness={1.1} />;
}

interface EffectsProps {
  bloom?: boolean;
  noise?: boolean;
  vignette?: boolean;
}

export function Effects({ bloom=false, noise=false, vignette=true }: EffectsProps) {
  return (
    <EffectComposer 
      multisampling={8} 
      frameBufferType={THREE.HalfFloatType}
    >
      {bloom ? <BloomEffect /> : <></>}
      {noise ? <NoiseEffect /> : <></>}
      {vignette ? <VignetteEffect /> : <></>}
    </EffectComposer>
  );
}