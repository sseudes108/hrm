// brmap.vert
varying vec3 vNormal;

void main() {
    // Passamos a normal para o fragment shader
    vNormal = normalize(normal); 
    
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mvPosition;
}