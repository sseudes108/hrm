import { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { useMapEvents } from '../../../../context/useMapEvents';
import { useTheme } from '../../../../context/useTheme';
import { useShaderTime } from '../Control/Controller';
import { createPillarMaterial } from './PillarMaterial';
import { eventHeight, eventSurfaceNormal, GLOBE_RADIUS, phaseFromId, WORLD_UP } from './eventPlacement';

const MAX_PILLARS = 100;

export function EventPillars() {
  const { theme } = useTheme();
  const { visibleEvents } = useMapEvents();
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  const geometry = useMemo(() => {
    const pillarGeometry = new THREE.CylinderGeometry(0.45, 1.25, 1, 6, 1, true);
    pillarGeometry.setAttribute('aPhase', new THREE.InstancedBufferAttribute(new Float32Array(MAX_PILLARS), 1));
    pillarGeometry.setAttribute('aIntensity', new THREE.InstancedBufferAttribute(new Float32Array(MAX_PILLARS), 1));
    return pillarGeometry;
  }, []);
  const material = useMemo(() => createPillarMaterial(theme.primary), [theme.primary]);

  useShaderTime(material);

  useEffect(() => {
    const mesh = meshRef.current;
    const phases = geometry.getAttribute('aPhase') as THREE.InstancedBufferAttribute;
    const intensities = geometry.getAttribute('aIntensity') as THREE.InstancedBufferAttribute;
    const matrix = new THREE.Matrix4();
    const quaternion = new THREE.Quaternion();
    const scale = new THREE.Vector3();

    visibleEvents.slice(0, MAX_PILLARS).forEach((event, index) => {
      const height = eventHeight(event.riskScore);
      const normal = eventSurfaceNormal(event.latitude, event.longitude);
      const position = normal.clone().multiplyScalar(GLOBE_RADIUS + height / 2);

      quaternion.setFromUnitVectors(WORLD_UP, normal);
      scale.set(1, height, 1);
      matrix.compose(position, quaternion, scale);

      mesh.setMatrixAt(index, matrix);
      phases.setX(index, phaseFromId(event.id));
      intensities.setX(index, 0.55 + event.riskScore / 180);
    });

    mesh.count = Math.min(visibleEvents.length, MAX_PILLARS);
    mesh.instanceMatrix.needsUpdate = true;
    phases.needsUpdate = true;
    intensities.needsUpdate = true;
  }, [geometry, visibleEvents]);

  return <instancedMesh ref={meshRef} args={[geometry, material, MAX_PILLARS]} renderOrder={15} />;
}
