export function Ocean() {
  return (
    <mesh renderOrder={1}>
      <sphereGeometry args={[99, 128, 128]} />
      <meshPhongMaterial 
        color="#001330"            // Azul quase preto para profundidade total
        emissive="#000d20"         // Uma leve luminescência azul interna
        specular="#444444"         // Intensidade do reflexo (cinza para não estourar muito)
        shininess={80}             // Quão polida é a superfície (0 a 100)
        transparent={true}
        opacity={1} 
      />
    </mesh>
  );
}