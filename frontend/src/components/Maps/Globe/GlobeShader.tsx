import { useLoader, useFrame } from '@react-three/fiber';
import { useMemo, useRef, useEffect } from 'react';
import * as THREE from 'three';
import { GlobeShader } from './GlobeShaderMaterial';

const BRASIL_LAT = THREE.MathUtils.degToRad(-16);
const BRASIL_LON = THREE.MathUtils.degToRad(-38);

interface ShaderGlobeProps {
  url: string;
  activeTheme: any;
  isLocked: boolean;
  renderOrder?: number;
}

export function ShaderGlobe({ url, activeTheme, isLocked, renderOrder = 1}: ShaderGlobeProps) {
  const meshRef = useRef<THREE.Mesh>(null!);
  const texture = useLoader(THREE.TextureLoader, url);

  // Configuração da Textura 8K para nitidez máxima
  useEffect(() => {
    if (texture) {
      texture.minFilter = THREE.NearestFilter;
      texture.magFilter = THREE.NearestFilter;
      texture.generateMipmaps = false;
      texture.needsUpdate = true;
    }
  }, [texture]);

  // Inicialização dos Uniforms
  const uniforms = useMemo(() => ({
    uHeightMap: { value: texture },
    uColor: { value: new THREE.Color(activeTheme.primary) },
    uTime: { value: 0 },
  }), [texture]);

  // REATIVIDADE: Atualiza a cor do shader quando o tema muda
  useEffect(() => {
    if (meshRef.current) {
      const mat = meshRef.current.material as THREE.ShaderMaterial;
      mat.uniforms.uColor.value.set(activeTheme.primary);
    }
  }, [activeTheme.primary]); // Monitora especificamente a cor primária

  useFrame((state) => {
    if (meshRef.current) {
      const mat = meshRef.current.material as THREE.ShaderMaterial;
      mat.uniforms.uTime.value = state.clock.getElapsedTime();

      // Lógica de rotação (Locked/Auto)
      if (isLocked) {
        const targetY = -BRASIL_LON + Math.PI / 2;
        const targetX = BRASIL_LAT;
        const currentY = meshRef.current.rotation.y;
        const angleOffset = Math.round((currentY - targetY) / (Math.PI * 2)) * (Math.PI * 2);
        meshRef.current.rotation.y = THREE.MathUtils.lerp(currentY, targetY + angleOffset, 0.05);
        meshRef.current.rotation.x = THREE.MathUtils.lerp(meshRef.current.rotation.x, targetX, 0.05);
      } else {
        meshRef.current.rotation.x = THREE.MathUtils.lerp(meshRef.current.rotation.x, 0, 0.05);
        meshRef.current.rotation.y += 0.00012;
      }
    }
  });

  return (
    <mesh ref={meshRef} renderOrder={renderOrder}>
      <sphereGeometry args={[103, 1024, 1024]} /> 
      <shaderMaterial 
        uniforms={uniforms}
        vertexShader={GlobeShader.vertexShader}
        fragmentShader={GlobeShader.fragmentShader}
        transparent={true}
        blending={THREE.AdditiveBlending}

        depthWrite={false} // Impede que a esfera crie um "contorno" opaco
        depthTest={true}   // Mantém a esfera atrás dos cards do dashboard
      />
    </mesh>
  );
}