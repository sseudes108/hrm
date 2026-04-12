import { OrbitControls } from '@react-three/drei';
import { useFrame, useThree } from '@react-three/fiber';
import { useRef, useEffect } from 'react';
import * as THREE from 'three';

interface CameraControllerProps {
  isLocked: boolean;
}

export function CameraController({ isLocked }: CameraControllerProps) {
  const { camera, gl } = useThree();
  const controlsRef = useRef<any>(null);
  
  const targetDistance = useRef(420); 
  const currentDistance = useRef(420);

  // --- SEU PAINEL DE CONTROLE DE ENQUADRAMENTO ---
  const OFFSET_X = -100; 
  const OFFSET_Y = -50;
  
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

  useFrame(() => {
    if (!controlsRef.current) return;

    const pCamera = camera as THREE.PerspectiveCamera;

    // APLICAR O ENQUADRAMENTO (LENS SHIFT)
    const currentX = pCamera.view ? pCamera.view.offsetX : 0;
    const currentY = pCamera.view ? pCamera.view.offsetY : 0;
    const nextX = THREE.MathUtils.lerp(currentX, OFFSET_X, 0.1);
    const nextY = THREE.MathUtils.lerp(currentY, OFFSET_Y, 0.1);

    pCamera.setViewOffset(
      gl.domElement.clientWidth, gl.domElement.clientHeight,
      nextX, nextY,
      gl.domElement.clientWidth, gl.domElement.clientHeight
    );
    pCamera.updateProjectionMatrix();

    // MANTER EIXO NO CENTRO
    controlsRef.current.target.set(0, 0, 0);

    if (isLocked) {
      // MODO TRAVADO: Vai suavemente para a posição do Brasil
      camera.position.lerp(new THREE.Vector3(66, -95, 140), 0.1);
    } else {
      // MODO LIVRE: Agora começa da posição onde o 'lerp' parou
      currentDistance.current = THREE.MathUtils.lerp(
        currentDistance.current, 
        targetDistance.current, 
        0.05
      );
      
      const lookAtDir = new THREE.Vector3()
        .subVectors(camera.position, controlsRef.current.target)
        .normalize();
      
      camera.position
        .copy(controlsRef.current.target)
        .addScaledVector(lookAtDir, currentDistance.current);
    }

    controlsRef.current.update();
  });

  return (
    <OrbitControls 
      ref={controlsRef}
      enabled={!isLocked} 
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