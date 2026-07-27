uniform vec3 uColor;

varying float vHeight;
varying float vPulse;
varying float vIntensity;

void main() {
  float verticalFade = smoothstep(0.0, 0.2, vHeight) * (0.45 + vHeight * 0.55);
  float emission = (0.22 + vPulse * 0.48) * vIntensity;
  float alpha = verticalFade * emission;

  gl_FragColor = vec4(uColor * (0.7 + vPulse * 0.7), alpha);
}
