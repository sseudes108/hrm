import { useFrame } from '@react-three/fiber';

export function useGlobalRotation(meshRef: any, material: any, isLocked: boolean) {
  useFrame((state, delta) => {
    if (meshRef.current && material) {
      const speed = isLocked ? 0 : 0.01;
      
      // Aplica a rotação
      meshRef.current.rotation.y += speed * delta;
      
      // Atualiza o shader (uTime)
      if (material.uniforms?.uTime) {
        material.uniforms.uTime.value = state.clock.getElapsedTime();
      }
    }
  });
}