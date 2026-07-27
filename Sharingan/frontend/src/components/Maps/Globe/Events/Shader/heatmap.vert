attribute float aIntensity;
attribute float aPhase;

uniform float uTime;
uniform float uRhythmSpeed;
uniform float uRhythmAmplitude;

varying vec2 vUv;
varying float vIntensity;

void main() {
  vUv = uv;
  vIntensity = aIntensity;

  float rhythm = 1.0 + sin(uTime * uRhythmSpeed + aPhase) * uRhythmAmplitude;
  vec3 transformed = position;
  transformed.xz *= rhythm;
  vec4 worldPosition = instanceMatrix * vec4(transformed, 1.0);
  gl_Position = projectionMatrix * modelViewMatrix * worldPosition;
}
