import { Bloom, Noise, Vignette, EffectComposer } from '@react-three/postprocessing';
import * as THREE from 'three';

// Método separado para o Bloom
export function BloomEffect() {
  return (
    <Bloom 
      intensity={0.05}         // Menos agressivo que 2.5
      luminanceThreshold={0.1} // Começa a brilhar mais cedo
      luminanceSmoothing={0.9}
      mipmapBlur
      radius={0.4}            // <--- Aumente para o brilho espalhar
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