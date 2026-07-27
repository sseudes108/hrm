import * as THREE from 'three';
import vertexShader from './Shader/overlay.vert';
import fragmentShader from './Shader/overlay.frag';

// Controles manuais exclusivos da placa de vidro continental.
export const OVERLAY_CONTROLS = {
  textureOffsetX: 0.196,
  textureOffsetY: 0.023,
  fillStrength: 0.16,
  lineStrength: 1.75,
  fillOpacity: 0.9,
  lineOpacity: 0.78,
  sphereRadius: 102.3,
} as const;

export function createOverlayMaterial(texture: THREE.Texture, color: THREE.ColorRepresentation) {
  return new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      uMap: { value: texture },
      uColor: { value: new THREE.Color(color) },
      uTextureOffset: { value: new THREE.Vector2(OVERLAY_CONTROLS.textureOffsetX, OVERLAY_CONTROLS.textureOffsetY) },
      uFillStrength: { value: OVERLAY_CONTROLS.fillStrength },
      uLineStrength: { value: OVERLAY_CONTROLS.lineStrength },
      uFillOpacity: { value: OVERLAY_CONTROLS.fillOpacity },
      uLineOpacity: { value: OVERLAY_CONTROLS.lineOpacity },
    },
    transparent: true,
    side: THREE.FrontSide,
    depthWrite: false,
    depthTest: true,
  });
}
