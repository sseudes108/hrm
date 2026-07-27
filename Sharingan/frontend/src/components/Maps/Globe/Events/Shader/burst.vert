attribute float aPhase;
attribute float aIntensity;
attribute float aHeight;

uniform float uTime;
uniform float uCycleSpeed;
uniform float uMinRadius;
uniform float uMaxRadius;
uniform float uExpansion;
uniform float uVerticalTravel;
uniform float uEmissionDistance;

varying vec2 vUv;
varying float vProgress;
varying float vIntensity;

void main() {
  float progress = fract(uTime * uCycleSpeed + aPhase);
  float travel = smoothstep(0.0, 0.58, progress);
  float expandedRadius = mix(uMinRadius, uMaxRadius, travel);
  float radius = mix(uMinRadius, expandedRadius, uExpansion);

  vec3 transformed = position;
  transformed.xz *= radius;
  transformed.y += travel * aHeight * uVerticalTravel * uEmissionDistance;

  vUv = uv;
  vProgress = progress;
  vIntensity = aIntensity;

  vec4 worldPosition = instanceMatrix * vec4(transformed, 1.0);
  gl_Position = projectionMatrix * modelViewMatrix * worldPosition;
}
