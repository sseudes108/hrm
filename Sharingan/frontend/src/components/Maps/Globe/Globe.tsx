import { Canvas } from '@react-three/fiber';
import { useRef } from 'react';
import * as THREE from 'three';
import { Ocean } from './Ocean/Ocean';
import { Overlay } from './Overlay/Overlay';
import { Geometry } from './Geometry/Geometry';
import { CameraController } from './Control/Camera';
import { EventBursts } from './Events/EventBursts';
import { EventSpheres } from './Events/EventSpheres';
import { EventHeatmap } from './Events/EventHeatmap';
import { EventSurfacePulses } from './Events/EventSurfacePulses';
import { EventRenderProvider } from './Events/EventRenderProvider';
import { useMapVisualization } from '../../../context/useMapVisualization';
import { useSharedGlobeRotation } from './Control/Controller';
// import { Effects } from '../../Layout/Effects';

export function Globe({ isLocked}: { isLocked: boolean; isFlat: boolean; }) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}>
      <Canvas 
        dpr={[1, 2]} 
        resize={{ debounce: { resize: 0, scroll: 0 } }}
        gl={{ 
          antialias: true, 
          powerPreference: "high-performance",
          stencil: false,
          depth: true
        }}
      >
        <ambientLight intensity={0.5} />
        <pointLight 
          position={[150, 150, 150]} 
          intensity={2} 
          color="#ffffff" 
        />
        <CameraController isLocked={isLocked}/>
        <GlobeScene isLocked={isLocked} />
      </Canvas>
    </div>
  );
}

function GlobeScene({ isLocked }: { isLocked: boolean }) {
  const { visualizationMode } = useMapVisualization();
  const globeRef = useRef<THREE.Group>(null!);
  useSharedGlobeRotation(globeRef, isLocked);

  return (
    <group ref={globeRef}>
      <EventRenderProvider>
      <Ocean />
    
        <Geometry
          glbUrl='/data/br_world.glb'
        />

        <Overlay 
          textureUrl="/data/br_mundo.png" 
        />

      {visualizationMode === 'BURSTS' && <><EventSurfacePulses /><EventBursts /></>}
      {visualizationMode === 'HEATMAP' && <EventHeatmap />}
      {visualizationMode === 'SPHERES' && <EventSpheres />}
      </EventRenderProvider>
    </group>
  );
}
