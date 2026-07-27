// fragmentShader
uniform vec3 uColor;
varying float vAltitude; 

void main() {
    // 1. AJUSTE DO DEGRADÊ (Mais agressivo para não lavar a cor)
    // Se vAltitude for a altura, queremos que o brilho suma rápido
    float glowFade = 1.3 - smoothstep(-5.0, 5.0, vAltitude);
    
    // Forçamos o fade a ser mais "curvo" (exponencial) 
    // Isso evita que o topo do continente fique claro demais
    glowFade = pow(glowFade, 4.0); 

    // 2. CORES
    // Cor de fundo: Vermelho profundo e escuro (contraste)
    vec3 baseColor = uColor * 0.8; 
    
    // Cor do Neon: Vermelho puro e "estourado" para o Bloom
    vec3 ledColor = uColor * 20.0; 

    // 3. MIX
    vec3 finalColor = mix(baseColor, ledColor, glowFade);

    // 4. SAÍDA (Removi o multiplicador global 1.5 que estava deixando tudo pálido)
    gl_FragColor = vec4(finalColor, 0.9);
}