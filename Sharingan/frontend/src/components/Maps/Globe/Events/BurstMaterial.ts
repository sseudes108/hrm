import * as THREE from 'three';
import fragmentShader from './Shader/burst.frag';
import vertexShader from './Shader/burst.vert';

// Ajuste estes valores para controlar a emissão sem tocar nos shaders.
export const BURST_EMISSION = {
  cycleSpeed: 0.9, // Aumente para diminuir o tempo entre um disparo e outro.
  ringInterval: 0.01, // Diminua para aproximar os contornos na sequência do disparo.
  emissionDistance: 0.45, // Diminua para encurtar a distância vertical entre emissões.
  minRadius: 0.1,
  maxRadius: 3.0,
  expansion: 1, // 0 = anel mantém o tamanho; 1 = expande até maxRadius.
  verticalTravel: 3,
  ringsPerEvent: 27,
  testEventLimit: 20,
  surfaceOffset: 0.1,
} as const;

export type BurstShape = 'TRIANGLE' | 'SQUARE' | 'DIAMOND' | 'HEXAGON';

const SHAPE_INDEX: Record<BurstShape, number> = {
  TRIANGLE: 0,
  SQUARE: 1,
  DIAMOND: 2,
  HEXAGON: 3,
};

export function createBurstMaterial(
  color: THREE.ColorRepresentation,
  shape: BurstShape,
  emission = BURST_EMISSION,
) {
  return new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uTime: { value: 0 },
      uColor: { value: new THREE.Color(color) },
      uCycleSpeed: { value: emission.cycleSpeed },
      uMinRadius: { value: emission.minRadius },
      uMaxRadius: { value: emission.maxRadius },
      uExpansion: { value: emission.expansion },
      uVerticalTravel: { value: emission.verticalTravel },
      uEmissionDistance: { value: emission.emissionDistance },
      uShape: { value: SHAPE_INDEX[shape] },
    },
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
}
