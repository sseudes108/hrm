uniform sampler2D uMap;
uniform vec3 uColor;
uniform float uTime;
// ----------------------------------------
varying vec2 vUv;

void main() {
  vec2 shiftedUv = vec2(
    fract(vUv.x + 0.196), 
    fract(vUv.y + 0.023)
  );
  
  vec4 tex = texture2D(uMap, shiftedUv);
  float val = tex.r;

  // 1. MÁSCARAS
  float maskTerra = smoothstep(0.01, 0.1, val);
  float maskLinhas = smoothstep(0.5, 0.8, val);

  // 2. EFEITO NEON (Pulso)
  float pulse = sin(uTime * 2.5) * 0.15 + 0.85;
  
  vec3 corPreenchimento = uColor * 0.2;
  vec3 corNeon = uColor * 2.5 * pulse;

  vec3 finalColor = mix(corPreenchimento, corNeon, maskLinhas);

  // 3. TRANSPARÊNCIA AJUSTÁVEL
  float opacidadeContinente = 0.81; // Tente 0.5 para ver a geometria de baixo
  float opacidadeLinhas = 1.0;

  // O Mix do Alpha: Linhas sólidas, continente translúcido
  float alphaFinal = mix(opacidadeContinente, opacidadeLinhas, maskLinhas);

  // Aplica a máscara de terra para o oceano continuar transparente
  float alphaComCorte = alphaFinal * maskTerra;

  if (alphaComCorte < 0.01) discard;

  gl_FragColor = vec4(finalColor, alphaComCorte);
}