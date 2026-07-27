uniform sampler2D uMap;
uniform vec3 uColor;
uniform vec2 uTextureOffset;
uniform float uFillStrength;
uniform float uLineStrength;
uniform float uFillOpacity;
uniform float uLineOpacity;

varying vec2 vUv;

void main() {
  float textureValue = texture2D(uMap, fract(vUv + uTextureOffset)).r;
  float landMask = smoothstep(0.01, 0.1, textureValue);
  float lineMask = smoothstep(0.5, 0.8, textureValue);
  float opacity = mix(uFillOpacity, uLineOpacity, lineMask) * landMask;
  vec3 color = uColor * mix(uFillStrength, uLineStrength, lineMask);

  if (opacity < 0.01) discard;
  gl_FragColor = vec4(color, opacity);
}
