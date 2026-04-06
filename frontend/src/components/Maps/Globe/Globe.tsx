import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { Suspense, } from 'react';
import { ShaderGlobe } from './GlobeShader';
import { Effects } from '../../Effects';


export function Globe({ activeTheme, isLocked }: { activeTheme: any; isLocked: boolean }) {
  return (
    <div style={{ width: '100%', height: '100vh'}}>
      <Canvas 
        dpr={[1, 2]} 
        gl={{ 
          // Ative o antialias nativo
          antialias: true, 
          powerPreference: "high-performance",
          stencil: false,
          depth: true
        }}
      >
        <PerspectiveCamera makeDefault position={[100, 0, 400]} fov={45} />
        <OrbitControls enabled={!isLocked} enablePan={false} minDistance={300} maxDistance={600} />

        {/* Oceano (Esfera de fundo) */}
        <mesh>
          <sphereGeometry args={[100, 1024, 1024]} />
          <meshBasicMaterial color="#272727" />
        </mesh>

        <Suspense fallback={null}>s
          <ShaderGlobe
            url="/data/world_heightmap.png" 
            activeTheme={activeTheme} 
            isLocked={isLocked} 
          />

          <Effects 
            noise={false}
            vignette={true}
          />

        </Suspense>

      </Canvas>
    </div>
  );
}