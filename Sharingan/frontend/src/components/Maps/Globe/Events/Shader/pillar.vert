attribute float aPhase;
attribute float aIntensity;

uniform float uTime;

varying float vHeight;
varying float vPulse;
varying float vIntensity;

void main() {
  float pulse = 0.5 + 0.5 * sin(uTime * 2.1 + aPhase);
  vec3 transformed = position;

  // Mantém a base estável e concentra a variação de altura no topo do pilar.
  transformed.y = mix(-0.5, position.y, 0.88 + pulse * 0.22);
  transformed.xz *= 0.92 + pulse * 0.16;

  vHeight = position.y + 0.5;
  vPulse = pulse;
  vIntensity = aIntensity;

  vec4 worldPosition = instanceMatrix * vec4(transformed, 1.0);
  gl_Position = projectionMatrix * modelViewMatrix * worldPosition;
}
