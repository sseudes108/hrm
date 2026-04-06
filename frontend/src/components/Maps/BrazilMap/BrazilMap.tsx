import { useMemo, useEffect } from 'react';
import * as THREE from 'three';
import { SVGLoader, SVGResult } from 'three/examples/jsm/loaders/SVGLoader';
import { createSmoothWallGeometry } from './SmoothWallGeometry';

interface BrazilMapProps {
  svgData: string;
  activeTheme: any;
}

interface StateMeshData {
  geometry: THREE.BufferGeometry;
  id: string;
}

export function BrazilMap({ svgData, activeTheme }: BrazilMapProps) {
  
  // 1. Processamento da Geometria
  const stateMeshes = useMemo<StateMeshData[]>(() => {
    if (!svgData) return [];

    try {
      const loader = new SVGLoader();
      const svgParsed = loader.parse(svgData) as SVGResult;
      
      return svgParsed.paths.map((path, pIdx) => {
        const shapes = path.toShapes(true);
        const geometry = createSmoothWallGeometry(shapes, 15);
        geometry.computeVertexNormals();

        return {
          geometry: geometry,
          id: (path.userData as any)?.style?.id || `state-${pIdx}`,
        };
      });
    } catch (err) {
      console.error("Erro ao processar geometria:", err);
      return [];
    }
  }, [svgData]);

  // 2. Material Externo (COR DO TEMA)
  const outerMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      transparent: true,
      side: THREE.FrontSide,
      depthWrite: true,
      depthTest: true,
      // PolygonOffset empurra a face externa levemente para a frente da câmera
      polygonOffset: true,
      polygonOffsetFactor: -1, 
      polygonOffsetUnits: -1,
      uniforms: { uColor: { value: new THREE.Color(activeTheme.primary) } },
      vertexShader: `
        varying vec3 vNormal;
        void main() {
          vNormal = normalize(normalMatrix * normal);
          // Empurra o vértice 0.1 unidades na direção da normal (para fora)
          vec3 pos = position + (normal * 0.1);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 uColor;
        void main() {
          gl_FragColor = vec4(uColor, 0.9);
        }
      `,
    });
  }, [activeTheme]);

  // 3. Material Interno (CYAN / COR FIXA)
  const innerMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      transparent: true,
      side: THREE.BackSide,
      depthWrite: true,
      depthTest: true,
      // PolygonOffset empurra a face interna para trás da externa
      polygonOffset: true,
      polygonOffsetFactor: 1,
      polygonOffsetUnits: 1,
      uniforms: { uColor: { value: new THREE.Color("#00ffff") } }, 
      vertexShader: `
        varying vec3 vNormal;
        void main() {
          vNormal = normalize(normalMatrix * normal);
          // Recolhe o vértice 0.1 unidades (para dentro)
          vec3 pos = position - (normal * 0.1);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 uColor;
        void main() {
          gl_FragColor = vec4(uColor, 0.4); // Mais suave para não ofuscar
        }
      `,
    });
  }, []);

  // Cleanup
  useEffect(() => {
    return () => {
      stateMeshes.forEach(m => m.geometry.dispose());
      outerMaterial.dispose();
      innerMaterial.dispose();
    };
  }, [stateMeshes, outerMaterial, innerMaterial]);

  if (stateMeshes.length === 0) return null;

  return (
    <group rotation={[Math.PI, 0, 0]} scale={0.5} position={[-250, 250, 0]}>
      {stateMeshes.map((state) => (
        <group key={state.id}>
          <mesh geometry={state.geometry} material={outerMaterial} />
          <mesh geometry={state.geometry} material={innerMaterial} />
        </group>
      ))}
    </group>
  );
}