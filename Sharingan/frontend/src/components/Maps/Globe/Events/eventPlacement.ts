import * as THREE from 'three';

export const GLOBE_RADIUS = 103;
export const WORLD_UP = new THREE.Vector3(0, 1, 0);

// Compensação da translação aplicada à textura em Overlay/Shader/overlay.frag.
// Mantenha estes valores sincronizados com `shiftedUv` para que eventos e mapa
// usem a mesma referência geográfica.
export const MAP_TEXTURE_OFFSET = {
  longitude: -0.698 * 360,
  latitude: -0.023 * 180,
} as const;

export function eventHeight(riskScore: number) {
  return 5 + riskScore * 0.07;
}

export function eventSurfaceNormal(latitude: number, longitude: number) {
  const adjustedLatitude = latitude + MAP_TEXTURE_OFFSET.latitude;
  const adjustedLongitude = longitude + MAP_TEXTURE_OFFSET.longitude;
  const phi = THREE.MathUtils.degToRad(90 - adjustedLatitude);
  const theta = THREE.MathUtils.degToRad(adjustedLongitude + 180);

  // SphereGeometry usa o eixo Z invertido em relação à fórmula esférica usual.
  return new THREE.Vector3(
    Math.sin(phi) * Math.cos(theta),
    Math.cos(phi),
    -Math.sin(phi) * Math.sin(theta),
  );
}

export function phaseFromId(id: string) {
  return Array.from(id).reduce((phase, character) => phase + character.charCodeAt(0), 0) * 0.173;
}
