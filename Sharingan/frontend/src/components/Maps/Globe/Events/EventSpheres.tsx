import { useEffect, useMemo, useRef } from 'react';
import * as THREE from 'three';
import { THEMES, type ThemeMode } from '../../../../constants/colors';
import { useMapEvents } from '../../../../context/useMapEvents';
import { useTheme } from '../../../../context/useTheme';
import { eventSurfaceNormal, GLOBE_RADIUS } from './eventPlacement';

const MAX_SPHERES = 80;
type EventThemeMode = Exclude<ThemeMode, 'TODOS'>;

const SPHERE_STYLES: Record<EventThemeMode, { mode: EventThemeMode; color: string }> = {
  NEGADA: { mode: 'NEGADA', color: THEMES.NEGADA.primary },
  FRAUDE: { mode: 'FRAUDE', color: THEMES.FRAUDE.primary },
  APROVADA: { mode: 'APROVADA', color: THEMES.APROVADA.primary },
  PENDENTE: { mode: 'PENDENTE', color: THEMES.PENDENTE.primary },
};

export function EventSpheres() {
  const { viewMode } = useTheme();
  const { visibleEvents } = useMapEvents();
  const styles = viewMode === 'TODOS' ? Object.values(SPHERE_STYLES) : [SPHERE_STYLES[viewMode]];

  return <group>{styles.map((style) => <SphereLayer key={style.mode} style={style} events={visibleEvents.filter((event) => event.visualMode === style.mode)} />)}</group>;
}

function SphereLayer({ style, events }: { style: { mode: EventThemeMode; color: string }; events: ReturnType<typeof useMapEvents>['visibleEvents'] }) {
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  const geometry = useMemo(() => new THREE.SphereGeometry(1, 20, 20), []);
  const material = useMemo(() => new THREE.MeshPhysicalMaterial({
    color: style.color,
    emissive: style.color,
    emissiveIntensity: 1.15,
    metalness: 0.35,
    roughness: 0.16,
    clearcoat: 1,
    clearcoatRoughness: 0.08,
    transparent: true,
    opacity: 0.92,
  }), [style.color]);

  const aggregates = useMemo(() => {
    const groups = new Map<string, { latitude: number; longitude: number; count: number; risk: number }>();
    events.forEach((event) => {
      const key = `${event.visualMode}-${event.region}`;
      const current = groups.get(key) ?? { latitude: event.latitude, longitude: event.longitude, count: 0, risk: 0 };
      current.count += 1;
      current.risk += event.riskScore;
      groups.set(key, current);
    });
    return [...groups.values()].sort((left, right) => right.count - left.count).slice(0, MAX_SPHERES);
  }, [events]);

  useEffect(() => {
    const mesh = meshRef.current;
    const matrix = new THREE.Matrix4();
    const scale = new THREE.Vector3();
    aggregates.forEach((aggregate, index) => {
      const normal = eventSurfaceNormal(aggregate.latitude, aggregate.longitude);
      const averageRisk = aggregate.risk / aggregate.count;
      const radius = 0.8 + Math.sqrt(aggregate.count) * 0.65 + averageRisk * 0.022;
      const position = normal.multiplyScalar(GLOBE_RADIUS + radius + 1.0);
      scale.setScalar(radius);
      matrix.compose(position, new THREE.Quaternion(), scale);
      mesh.setMatrixAt(index, matrix);
    });
    mesh.count = aggregates.length;
    mesh.instanceMatrix.needsUpdate = true;
  }, [aggregates]);

  return <instancedMesh ref={meshRef} args={[geometry, material, MAX_SPHERES]} renderOrder={17} />;
}
