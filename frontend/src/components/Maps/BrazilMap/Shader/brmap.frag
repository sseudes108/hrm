// brmap.frag
varying vec3 vNormal;

// ESSENCIAL: Declarar as uniforms que vêm do React
uniform vec3 uOuterColor; 
uniform float uTime; // Caso queira usar o tempo para animações

void main() {
    // 1. Remove o teto e o fundo (descarta faces horizontais)
    // No Extrude deitado, o topo/fundo tem normal Z forte
    if (abs(vNormal.z) > 0.5) {
        discard;
    }

    // 2. Torna a parte interna invisível
    if (!gl_FrontFacing) {
        discard;
    }

    // 3. Lado de fora: 
    // vec4 precisa de (r, g, b, a). uOuterColor já é (r, g, b)
    gl_FragColor = vec4(uOuterColor, 0.7);
}