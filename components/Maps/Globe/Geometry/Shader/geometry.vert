// vertexShader
varying vec3 vNormal;
varying float vDepth;
const float PI = 3.14159265359;

void main() {
  float lon = (position.x / 180.0) * PI; 
  float lat = (-position.z / 90.0) * (PI / 2.0); 

  // 2. Altura
  vDepth = position.y; 
  float radius = 101.0 + position.y; 

  vec3 spherePos;
  spherePos.x = radius * cos(lat) * sin(lon);
  spherePos.y = radius * sin(lat);
  spherePos.z = radius * cos(lat) * cos(lon);

  vNormal = normalize(spherePos);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(spherePos, 1.0);
}