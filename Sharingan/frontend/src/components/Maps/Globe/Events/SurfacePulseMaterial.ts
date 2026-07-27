import * as THREE from 'three';
import fragmentShader from './Shader/surfacePulse.frag';
import vertexShader from './Shader/surfacePulse.vert';
import type { BurstShape } from './BurstMaterial';

// Controles manuais exclusivos da emissão horizontal no solo.
export const SURFACE_PULSE_CONTROLS = {
  speed: 0.62,
  minRadius: 0.5,
  maxRadius: 4.2,
  ringWidth: 0.032,
  glowStrength: 2.8,
  opacity: 0.92,
  phaseSpacing: 0.16,
  surfaceOffset: 0.1,
} as const;

const SHAPE_INDEX: Record<BurstShape, number> = { TRIANGLE: 0, SQUARE: 1, DIAMOND: 2, HEXAGON: 3 };

export function createSurfacePulseMaterial(color: THREE.ColorRepresentation, shape: BurstShape) {
  return new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uTime: { value: 0 }, uColor: { value: new THREE.Color(color) }, uShape: { value: SHAPE_INDEX[shape] },
      uSpeed: { value: SURFACE_PULSE_CONTROLS.speed }, uMinRadius: { value: SURFACE_PULSE_CONTROLS.minRadius },
      uMaxRadius: { value: SURFACE_PULSE_CONTROLS.maxRadius }, uRingWidth: { value: SURFACE_PULSE_CONTROLS.ringWidth },
      uGlowStrength: { value: SURFACE_PULSE_CONTROLS.glowStrength }, uOpacity: { value: SURFACE_PULSE_CONTROLS.opacity },
    },
    transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide,
  });
}
