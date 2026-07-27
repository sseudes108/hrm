attribute float aPhase;
attribute float aIntensity;
uniform float uTime;
uniform float uSpeed;
uniform float uMinRadius;
uniform float uMaxRadius;
varying vec2 vUv;
varying float vProgress;
varying float vIntensity;
void main() {
  float progress = fract(uTime * uSpeed + aPhase);
  float radius = mix(uMinRadius, uMaxRadius, smoothstep(0.0, 0.72, progress));
  vec3 transformed = position;
  transformed.xz *= radius;
  vUv = uv; vProgress = progress; vIntensity = aIntensity;
  gl_Position = projectionMatrix * modelViewMatrix * instanceMatrix * vec4(transformed, 1.0);
}
