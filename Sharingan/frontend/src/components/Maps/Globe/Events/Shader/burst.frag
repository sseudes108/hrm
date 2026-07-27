uniform vec3 uColor;
uniform float uShape;

varying vec2 vUv;
varying float vProgress;
varying float vIntensity;

float sdPolygon(vec2 point, float sides, float rotation) {
  float angle = atan(point.y, point.x) + rotation;
  float sector = 6.283185 / sides;
  float boundary = cos(3.141593 / sides) / cos(mod(angle + sector * 0.5, sector) - sector * 0.5);
  return length(point) - 0.34 * boundary;
}

float shapeDistance(vec2 point) {
  if (uShape < 0.5) return sdPolygon(point, 3.0, 1.570796);
  if (uShape < 1.5) return sdPolygon(point, 4.0, 0.785398);
  if (uShape < 2.5) return sdPolygon(point, 4.0, 0.0);
  return sdPolygon(point, 6.0, 0.0);
}

void main() {
  float distanceToEdge = abs(shapeDistance(vUv - 0.5));
  float outline = 1.0 - smoothstep(0.008, 0.028, distanceToEdge);
  float glow = 1.0 - smoothstep(0.015, 0.09, distanceToEdge);
  float fadeIn = smoothstep(0.0, 0.06, vProgress);
  float fadeOut = 1.0 - smoothstep(0.46, 0.64, vProgress);
  float alpha = (outline + glow * 0.22) * fadeIn * fadeOut * vIntensity;

  gl_FragColor = vec4(uColor * (0.9 + glow * 0.7), alpha);
}
