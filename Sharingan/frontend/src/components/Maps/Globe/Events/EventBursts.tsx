import { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { useShaderTime } from '../Control/Controller';
import { BURST_EMISSION, createBurstMaterial } from './BurstMaterial';
import { eventHeight, eventSurfaceNormal, GLOBE_RADIUS, phaseFromId, WORLD_UP } from './eventPlacement';
import { useEventRenderSource } from './useEventRenderSource';
import type { EventRenderStyle } from './eventRenderContext';

const MAX_EVENTS = BURST_EMISSION.testEventLimit;
const RINGS_PER_EVENT = BURST_EMISSION.ringsPerEvent;
const MAX_BURSTS = MAX_EVENTS * RINGS_PER_EVENT;

export function EventBursts() {
  const { layers } = useEventRenderSource();

  return (
    <group>
      {layers.map((layer) => <EventBurstLayer key={layer.style.mode} events={layer.events} style={layer.style} />)}
    </group>
  );
}

function EventBurstLayer({
  events,
  style,
}: {
  events: import('../../../../context/mapEventsContext').MapEvent[];
  style: EventRenderStyle;
}) {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  const geometry = useMemo(() => {
    const ringGeometry = new THREE.PlaneGeometry(1, 1);
    ringGeometry.rotateX(-Math.PI / 2);
    ringGeometry.setAttribute('aPhase', new THREE.InstancedBufferAttribute(new Float32Array(MAX_BURSTS), 1));
    ringGeometry.setAttribute('aIntensity', new THREE.InstancedBufferAttribute(new Float32Array(MAX_BURSTS), 1));
    ringGeometry.setAttribute('aHeight', new THREE.InstancedBufferAttribute(new Float32Array(MAX_BURSTS), 1));
    return ringGeometry;
  }, []);
  const material = useMemo(
    () => createBurstMaterial(style.color, style.shape),
    [style.color, style.shape],
  );

  useShaderTime(material);

  useEffect(() => {
    const mesh = meshRef.current;
    const phases = geometry.getAttribute('aPhase') as THREE.InstancedBufferAttribute;
    const intensities = geometry.getAttribute('aIntensity') as THREE.InstancedBufferAttribute;
    const heights = geometry.getAttribute('aHeight') as THREE.InstancedBufferAttribute;
    const matrix = new THREE.Matrix4();
    const quaternion = new THREE.Quaternion();
    const scale = new THREE.Vector3(1, 1, 1);
    let instanceIndex = 0;

    events.forEach((event) => {
      const normal = eventSurfaceNormal(event.latitude, event.longitude);
      const position = normal.clone().multiplyScalar(GLOBE_RADIUS + BURST_EMISSION.surfaceOffset);
      const height = eventHeight(event.riskScore);

      quaternion.setFromUnitVectors(WORLD_UP, normal);
      matrix.compose(position, quaternion, scale);

      for (let ringIndex = 0; ringIndex < RINGS_PER_EVENT; ringIndex += 1) {
        mesh.setMatrixAt(instanceIndex, matrix);
        phases.setX(
          instanceIndex,
          phaseFromId(event.id) + ringIndex * BURST_EMISSION.ringInterval,
        );
        intensities.setX(instanceIndex, 0.5 + event.riskScore / 350);
        heights.setX(instanceIndex, height);
        instanceIndex += 1;
      }
    });

    mesh.count = instanceIndex;
    mesh.instanceMatrix.needsUpdate = true;
    phases.needsUpdate = true;
    intensities.needsUpdate = true;
    heights.needsUpdate = true;
  }, [events, geometry]);

  return <instancedMesh ref={meshRef} args={[geometry, material, MAX_BURSTS]} renderOrder={16} />;
}
