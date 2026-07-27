import { useMemo, useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { GeometryShader } from './GeometryMaterial';
import { useShaderTime } from '../Control/Controller';
import { useTheme } from '../../../../context/useTheme';

interface GlobeGeometryProps {
  glbUrl: string;
}

export function Geometry({ glbUrl }: GlobeGeometryProps) {
  const { theme } = useTheme();
  const { scene } = useGLTF(glbUrl);

  const geoMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader: GeometryShader.vertexShader,
      fragmentShader: GeometryShader.fragmentShader,
      uniforms: {
        uColor: { value: new THREE.Color(theme.primary) },
        uTime: { value: 0 },
      },
      side: THREE.DoubleSide, 
      depthWrite: true,
      depthTest: true,
    });
  }, [theme.primary]);

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

  useShaderTime(geoMaterial);

  return (
    <group>
      <primitive object={scene} scale={[1, 1, 1]} />
    </group>
  );
}
