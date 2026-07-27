uniform vec3 uColor;
uniform float uBaseOpacity;
uniform float uIntensityOpacity;
uniform float uFalloff;
uniform float uCoreFalloff;

varying vec2 vUv;
varying float vIntensity;

void main() {
  vec2 point = vUv - 0.5;
  float distanceFromCenter = length(point) * 2.0;
  float heat = exp(-distanceFromCenter * distanceFromCenter * uFalloff);
  float core = exp(-distanceFromCenter * distanceFromCenter * uCoreFalloff);
  float alpha = heat * (uBaseOpacity + vIntensity * uIntensityOpacity);

  if (alpha < 0.012) discard;

  gl_FragColor = vec4(uColor * (0.55 + core * 1.15), alpha);
}
