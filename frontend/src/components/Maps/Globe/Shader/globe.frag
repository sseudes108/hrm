uniform vec3 uColor;
uniform sampler2D uHeightMap;
varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
    float h = texture2D(uHeightMap, vUv).r;

    if (h < 0.05) discard;

    // Fresnel para suavizar a borda (evita o corte seco)
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(vViewPosition);
    float fresnel = pow(1.0 - clamp(dot(normal, viewDir), 0.0, 1.0), 3.0);

    // Definição das camadas
    float continente = smoothstep(0.1, 0.2, h) * 0.15; 
    float linhas = smoothstep(0.1, 0.9, h);

    // Se Bloom for False, uColor * 5.0 apenas fará a linha ser muito clara.
    // O AdditiveBlending cuidará de deixá-la sólida.
    vec3 corFinal = mix(uColor * 0.5, uColor * 2.0, linhas);
    
    // Alpha Final: O segredo para não ter contorno cinza é o (1.0 - fresnel)
    float alphaFinal = max(continente, linhas) * (1.0 - fresnel);

    // Multiplicação obrigatória para AdditiveBlending não gerar halos
    vec3 rgbSaida = corFinal * alphaFinal;

    gl_FragColor = vec4(rgbSaida, alphaFinal);
}