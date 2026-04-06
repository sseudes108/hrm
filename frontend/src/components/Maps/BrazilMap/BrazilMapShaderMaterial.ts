import * as THREE from 'three';

export const BrazilMapShader = {
  uniforms: {
    // Definimos as duas cores como Uniforms
    uOuterColor: { value: new THREE.Color("#ff0000") }, // Vermelho para Fora
    uInnerColor: { value: new THREE.Color("#0000ff") }, // Azul para Dentro
  },
  
  // O Vertex Shader apenas passa as normais para o Fragment
  vertexShader: `
    varying vec3 vNormal;
    varying vec2 vUv;
    
    void main() {
      vNormal = normal;
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  
  // O Fragment Shader faz a mágica da cor
  fragmentShader: `
    // brmap.frag
    varying vec3 vNormal;
    varying vec3 vLocalPos;

    uniform vec3 uColor; // Uma única cor sólida

    void main() {
        // 1. Remove o teto e o fundo (mesma lógica)
        if (abs(vNormal.z) > 0.5) {
            discard;
        }

        // Saída sólida e limpa, sem depender do gl_FrontFacing
        gl_FragColor = vec4(uColor, 1.0);
    }
  `,
};