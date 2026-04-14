import { useRef, useMemo, useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { GeometryShader } from './GeometryMaterial';
import { useGlobalRotation } from '../Control/Controller';

interface GlobeGeometryProps {
  glbUrl: string;
  activeTheme: any;
  isLocked: boolean;
}

export function Geometry({ glbUrl, activeTheme, isLocked }: GlobeGeometryProps) {
  const { scene } = useGLTF(glbUrl);

  const geoMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader: GeometryShader.vertexShader,
      fragmentShader: GeometryShader.fragmentShader,
      uniforms: {
        uColor: { value: new THREE.Color(activeTheme.primary) },
        uTime: { value: 0 },
      },
      side: THREE.DoubleSide, 
      depthWrite: true,
      depthTest: true,
    });
  }, [activeTheme.primary]);

  useEffect(() => {
    if (scene) {
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh;
          mesh.material = geoMaterial;
          mesh.frustumCulled = false;
          mesh.renderOrder = 5;
        }
      });
    }
  }, [scene, geoMaterial]);

  const meshRef = useRef<THREE.Group>(null!);
  useGlobalRotation(meshRef, geoMaterial, isLocked)

  return (
    <group ref={meshRef}>
      <primitive object={scene} scale={[1, 1, 1]} />
    </group>
  );
}