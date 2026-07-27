import * as THREE from 'three';
import fragmentShader from './Shader/heatmap.frag';
import vertexShader from './Shader/heatmap.vert';

// Controles manuais exclusivos das manchas planas do Heatmap.
export const HEATMAP_CONTROLS = {
  minRadius: 4.2,
  riskRadiusFactor: 0.09,
  baseOpacity: 0.5,
  intensityOpacity: 0.4,
  falloff: 5.2,
  coreFalloff: 2.0,
  rhythmSpeed: 2.2,
  rhythmAmplitude: 0.1,
  surfaceOffset: -0.9,
} as const;

export function createHeatmapMaterial(color: THREE.ColorRepresentation) {
  return new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uTime: { value: 0 },
      uColor: { value: new THREE.Color(color) },
      uBaseOpacity: { value: HEATMAP_CONTROLS.baseOpacity },
      uIntensityOpacity: { value: HEATMAP_CONTROLS.intensityOpacity },
      uFalloff: { value: HEATMAP_CONTROLS.falloff },
      uCoreFalloff: { value: HEATMAP_CONTROLS.coreFalloff },
      uRhythmSpeed: { value: HEATMAP_CONTROLS.rhythmSpeed },
      uRhythmAmplitude: { value: HEATMAP_CONTROLS.rhythmAmplitude },
    },
    transparent: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
}
