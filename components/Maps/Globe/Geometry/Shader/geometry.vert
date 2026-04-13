// vertexShader
varying vec3 vNormal;
varying float vDepth;
varying vec2 vUv;
varying float vAltitude; // <--- 1. DECLARAR ESTA VARIÁVEL

const float PI = 3.14159265359;

void main() {
  vUv = uv;
  
  // Capturamos a altitude original do plano (position.y no seu caso)
  // Base (mar) é o valor mais baixo de Y. Topo é o valor mais alto de Y.
  vAltitude = position.y; 
  vDepth = position.y;

  // 1. Projeção Esférica (Mantida)
  float lon = (position.x / 180.0) * PI; 
  float lat = (-position.z / 90.0) * (PI / 2.0); 

  float radius = 101.0 + position.y; 

  vec3 spherePos;
  spherePos.x = radius * cos(lat) * sin(lon);
  spherePos.y = radius * sin(lat);
  spherePos.z = radius * cos(lat) * cos(lon);

  vNormal = normalize(spherePos);
  
  // 2. Posicionamento Final (Mantido)
  gl_Position = projectionMatrix * modelViewMatrix * vec4(spherePos, 1.0);
}