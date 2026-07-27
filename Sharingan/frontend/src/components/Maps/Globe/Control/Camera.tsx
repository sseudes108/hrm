import { OrbitControls } from '@react-three/drei';
import { useFrame, useThree } from '@react-three/fiber';
import { useRef, useEffect, useMemo } from 'react';
import * as THREE from 'three';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';

const LOCKED_CAMERA_POSITION = new THREE.Vector3(66, -95, 140);
const GLOBE_CENTER = new THREE.Vector3(0, 0, 0);
const FRAME_OFFSET = { x: 0, y: -40 };

interface CameraControllerProps {
  isLocked: boolean;
}

export function CameraController({ isLocked }: CameraControllerProps) {
  const { camera, gl } = useThree();
  const controlsRef = useRef<OrbitControlsImpl>(null);
  const targetDistance = useRef(420); 
  const currentDistance = useRef(420);
  const lookAtDirection = useMemo(() => new THREE.Vector3(), []);
  
  // 1. Sincronização de Distância ao Destravar
  useEffect(() => {
    if (!isLocked && controlsRef.current) {
      // Quando destravamos, calculamos a distância real que a câmera está do centro
      const actualDistance = camera.position.distanceTo(controlsRef.current.target);
      
      // Atualizamos os refs para que o modo livre comece exatamente de onde o modo travado parou
      currentDistance.current = actualDistance;
      targetDistance.current = actualDistance;
    }
  }, [isLocked, camera]);

  useEffect(() => {
    const handleWheel = (e: WheelEvent) => {
      if (isLocked) return;
      e.preventDefault();
      const direction = e.deltaY > 0 ? 1 : -1;
      targetDistance.current = THREE.MathUtils.clamp(
        targetDistance.current + (direction * 40),
        150, 600
      );
    };
    window.addEventListener('wheel', handleWheel, { passive: false });
    return () => window.removeEventListener('wheel', handleWheel);
  }, [isLocked]);

  useEffect(() => {
    const perspectiveCamera = camera as THREE.PerspectiveCamera;
    return () => perspectiveCamera.clearViewOffset();
  }, [camera]);

  useFrame(() => {
    if (!controlsRef.current) return;

    const pCamera = camera as THREE.PerspectiveCamera;

    const width = gl.domElement.clientWidth;
    const height = gl.domElement.clientHeight;
    if (width === 0 || height === 0) return;

    // Mantém o globo no centro horizontal do bloco e um pouco abaixo no eixo Y.
    pCamera.setViewOffset(width, height, FRAME_OFFSET.x, FRAME_OFFSET.y, width, height);
    pCamera.updateProjectionMatrix();

    controlsRef.current.target.copy(GLOBE_CENTER);

    if (isLocked) {
      camera.position.lerp(LOCKED_CAMERA_POSITION, 0.1);
    } else {
      currentDistance.current = THREE.MathUtils.lerp(
        currentDistance.current, 
        targetDistance.current, 
        0.05
      );
      
      lookAtDirection
        .subVectors(camera.position, controlsRef.current.target)
        .normalize();
      
      camera.position
        .copy(controlsRef.current.target)
        .addScaledVector(lookAtDirection, currentDistance.current);
    }

    controlsRef.current.update();
  });

  return (
    <OrbitControls 
      ref={controlsRef}
      enabled={!isLocked} 
      enableRotate={!isLocked}
      enablePan={false}
      enableZoom={false} 
      enableDamping={true}
      dampingFactor={0.05}
      rotateSpeed={0.8}
      minPolarAngle={Math.PI / 4} 
      maxPolarAngle={Math.PI / 1.4}
    />
  );
}
