import { Canvas } from '@react-three/fiber';
import { Ocean } from './Ocean/Ocean';
import { Overlay } from './Overlay/Overlay';
import { Geometry } from './Geometry/Geometry';
import { CameraController } from './Control/Camera';

export function Globe({ activeTheme, isLocked, isFlat }: { activeTheme: any; isLocked: boolean; isFlat: boolean; }) {
  return (
    <div style={{ width: '100%', height: '100vh'}}>
      <Canvas 
        dpr={[1, 2]} 
        gl={{ 
          antialias: true, 
          powerPreference: "high-performance",
          stencil: false,
          depth: true
        }}
      >
        <CameraController isLocked={isLocked}/>

        <Ocean />
    
        <Geometry
          glbUrl='/data/br_world.glb'
          activeTheme={activeTheme}
          isLocked={isLocked}
        />

        <Overlay 
          textureUrl="/data/br_mundo.png" 
          activeTheme={activeTheme}
          isLocked={isLocked}
        />
        
      </Canvas>
    </div>
  );
}