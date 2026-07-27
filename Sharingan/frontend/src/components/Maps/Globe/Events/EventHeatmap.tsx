import { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { THEMES, type ThemeMode } from '../../../../constants/colors';
import { useMapEvents } from '../../../../context/useMapEvents';
import { useTheme } from '../../../../context/useTheme';
import { useShaderTime } from '../Control/Controller';
import { eventSurfaceNormal, GLOBE_RADIUS, phaseFromId, WORLD_UP } from './eventPlacement';
import { createHeatmapMaterial } from './HeatmapMaterial';
import { HEATMAP_CONTROLS } from './HeatmapMaterial';

const MAX_HEAT_SPOTS = 80;
type EventThemeMode = Exclude<ThemeMode, 'TODOS'>;

const HEATMAP_STYLES: Record<EventThemeMode, { mode: EventThemeMode; color: string }> = {
  NEGADA: { mode: 'NEGADA', color: THEMES.NEGADA.primary },
  FRAUDE: { mode: 'FRAUDE', color: THEMES.FRAUDE.primary },
  APROVADA: { mode: 'APROVADA', color: THEMES.APROVADA.primary },
  PENDENTE: { mode: 'PENDENTE', color: THEMES.PENDENTE.primary },
};

export function EventHeatmap() {
  const { viewMode } = useTheme();
  const { visibleEvents } = useMapEvents();
  const styles = viewMode === 'TODOS' ? Object.values(HEATMAP_STYLES) : [HEATMAP_STYLES[viewMode]];

  return (
    <group>
      {styles.map((style) => {
        const eventsForStyle = visibleEvents.filter((event) => event.visualMode === style.mode);

        return <HeatmapLayer key={style.mode} color={style.color} events={eventsForStyle} />;
      })}
    </group>
  );
}

function HeatmapLayer({
  color,
  events,
}: {
  color: string;
  events: ReturnType<typeof useMapEvents>['visibleEvents'];
}) {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  const geometry = useMemo(() => {
    const heatGeometry = new THREE.PlaneGeometry(1, 1);
    heatGeometry.rotateX(-Math.PI / 2);
    heatGeometry.setAttribute('aIntensity', new THREE.InstancedBufferAttribute(new Float32Array(MAX_HEAT_SPOTS), 1));
    heatGeometry.setAttribute('aPhase', new THREE.InstancedBufferAttribute(new Float32Array(MAX_HEAT_SPOTS), 1));
    return heatGeometry;
  }, []);
  const material = useMemo(() => createHeatmapMaterial(color), [color]);

  useShaderTime(material);

  useEffect(() => {
    const mesh = meshRef.current;
    const intensities = geometry.getAttribute('aIntensity') as THREE.InstancedBufferAttribute;
    const phases = geometry.getAttribute('aPhase') as THREE.InstancedBufferAttribute;
    const matrix = new THREE.Matrix4();
    const quaternion = new THREE.Quaternion();
    const scale = new THREE.Vector3();

    events.slice(0, MAX_HEAT_SPOTS).forEach((event, index) => {
      const normal = eventSurfaceNormal(event.latitude, event.longitude);
      // A rotação precisa receber a normal unitária. A posição é uma cópia
      // escalada para manter o plano tangente e horizontal sobre o globo.
      const position = normal.clone().multiplyScalar(GLOBE_RADIUS + HEATMAP_CONTROLS.surfaceOffset);
      const radius = HEATMAP_CONTROLS.minRadius + event.riskScore * HEATMAP_CONTROLS.riskRadiusFactor;

      quaternion.setFromUnitVectors(WORLD_UP, normal);
      scale.set(radius, radius, radius);
      matrix.compose(position, quaternion, scale);

      mesh.setMatrixAt(index, matrix);
      intensities.setX(index, event.riskScore / 100);
      phases.setX(index, phaseFromId(event.id));
    });

    mesh.count = Math.min(events.length, MAX_HEAT_SPOTS);
    mesh.instanceMatrix.needsUpdate = true;
    intensities.needsUpdate = true;
    phases.needsUpdate = true;
  }, [events, geometry]);

  return <instancedMesh ref={meshRef} args={[geometry, material, MAX_HEAT_SPOTS]} renderOrder={14} />;
}
