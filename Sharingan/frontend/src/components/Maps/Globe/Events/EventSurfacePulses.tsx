import { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { useShaderTime } from '../Control/Controller';
import { BURST_EMISSION } from './BurstMaterial';
import { eventSurfaceNormal, GLOBE_RADIUS, phaseFromId, WORLD_UP } from './eventPlacement';
import { createSurfacePulseMaterial, SURFACE_PULSE_CONTROLS } from './SurfacePulseMaterial';
import { useEventRenderSource } from './useEventRenderSource';
import type { EventRenderStyle } from './eventRenderContext';

const MAX_EVENTS = BURST_EMISSION.testEventLimit; const PULSES_PER_EVENT = 3; const MAX_PULSES = MAX_EVENTS * PULSES_PER_EVENT;
export function EventSurfacePulses() { const { layers } = useEventRenderSource(); return <group>{layers.map((layer) => <PulseLayer key={layer.style.mode} style={layer.style} events={layer.events} />)}</group>; }
function PulseLayer({ style, events }: { style: EventRenderStyle; events: import('../../../../context/mapEventsContext').MapEvent[] }) {
  const meshRef = useRef<THREE.InstancedMesh>(null!); const geometry = useMemo(() => { const geometry = new THREE.PlaneGeometry(1, 1); geometry.rotateX(-Math.PI / 2); geometry.setAttribute('aPhase', new THREE.InstancedBufferAttribute(new Float32Array(MAX_PULSES), 1)); geometry.setAttribute('aIntensity', new THREE.InstancedBufferAttribute(new Float32Array(MAX_PULSES), 1)); return geometry; }, []); const material = useMemo(() => createSurfacePulseMaterial(style.color, style.shape), [style.color, style.shape]); useShaderTime(material);
  useEffect(() => { const mesh = meshRef.current; const phases = geometry.getAttribute('aPhase') as THREE.InstancedBufferAttribute; const intensities = geometry.getAttribute('aIntensity') as THREE.InstancedBufferAttribute; const matrix = new THREE.Matrix4(); const quaternion = new THREE.Quaternion(); let index = 0; events.forEach((event) => { const normal = eventSurfaceNormal(event.latitude, event.longitude); quaternion.setFromUnitVectors(WORLD_UP, normal); matrix.compose(normal.clone().multiplyScalar(GLOBE_RADIUS + SURFACE_PULSE_CONTROLS.surfaceOffset), quaternion, new THREE.Vector3(1, 1, 1)); for (let pulse = 0; pulse < PULSES_PER_EVENT; pulse += 1) { mesh.setMatrixAt(index, matrix); phases.setX(index, phaseFromId(event.id) + pulse * SURFACE_PULSE_CONTROLS.phaseSpacing); intensities.setX(index, 0.45 + event.riskScore / 200); index += 1; } }); mesh.count = index; mesh.instanceMatrix.needsUpdate = true; phases.needsUpdate = true; intensities.needsUpdate = true; }, [events, geometry]);
  return <instancedMesh ref={meshRef} args={[geometry, material, MAX_PULSES]} renderOrder={14} />;
}
