import * as THREE from 'three';

export function createSmoothWallGeometry(shapes: THREE.Shape[], depth: number) {
  const vertices: number[] = [];
  const indices: number[] = [];
  let offset = 0;

  shapes.forEach(shape => {
    const points = shape.getPoints();
    for (let i = 0; i < points.length - 1; i++) {
      const p1 = points[i];
      const p2 = points[i + 1];

      // 4 Vértices por segmento (Parede vertical)
      vertices.push(p1.x, p1.y, 0);      // 0: Base 1
      vertices.push(p2.x, p2.y, 0);      // 1: Base 2
      vertices.push(p1.x, p1.y, depth);  // 2: Topo 1
      vertices.push(p2.x, p2.y, depth);  // 3: Topo 2

      // Triângulo 1
      indices.push(offset + 0, offset + 1, offset + 2);
      // Triângulo 2
      indices.push(offset + 2, offset + 1, offset + 3);

      offset += 4;
    }
  });

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}