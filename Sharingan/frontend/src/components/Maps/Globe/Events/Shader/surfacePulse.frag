uniform vec3 uColor;
uniform float uShape;
uniform float uRingWidth;
uniform float uGlowStrength;
uniform float uOpacity;
varying vec2 vUv;
varying float vProgress;
varying float vIntensity;
float sdPolygon(vec2 point, float sides, float rotation) { float angle = atan(point.y, point.x) + rotation; float sector = 6.283185 / sides; float boundary = cos(3.141593 / sides) / cos(mod(angle + sector * 0.5, sector) - sector * 0.5); return length(point) - 0.34 * boundary; }
float shapeDistance(vec2 point) { if (uShape < 0.5) return sdPolygon(point, 3.0, 1.570796); if (uShape < 1.5) return sdPolygon(point, 4.0, 0.785398); if (uShape < 2.5) return sdPolygon(point, 4.0, 0.0); return sdPolygon(point, 6.0, 0.0); }
void main() {
  float edge = abs(shapeDistance(vUv - 0.5));
  float ring = 1.0 - smoothstep(uRingWidth, uRingWidth * 2.7, edge);
  float glow = 1.0 - smoothstep(uRingWidth * 1.2, 0.12, edge);
  float fade = smoothstep(0.0, 0.05, vProgress) * (1.0 - smoothstep(0.58, 0.92, vProgress));
  float alpha = (ring + glow * 0.22) * fade * vIntensity * uOpacity;
  if (alpha < 0.01) discard;
  gl_FragColor = vec4(uColor * (1.0 + glow * uGlowStrength), alpha);
}
