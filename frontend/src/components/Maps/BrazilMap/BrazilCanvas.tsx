import { Suspense, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { BrazilMap } from './BrazilMap';
import { Effects } from '../../Effects';

export function BrazilCanvas({ activeTheme, isLocked }: { activeTheme: any; isLocked: boolean }) {
  const [svgText, setSvgText] = useState<string | null>(null);

  useEffect(() => {
    fetch('data/br.svg')
      .then((res) => res.text())
      .then((data) => setSvgText(data))
      .catch((err) => console.error("Erro ao carregar SVG:", err));
  }, []);

  return (
    <div style={{ width: '100%', height: '100vh'}}>
      <Canvas dpr={[1, 2]} gl={{ antialias: true, alpha: true }}>
        <PerspectiveCamera 
          makeDefault 
          position={[0, 0, 500]} // Câmera de frente, distância moderada
          fov={45} 
        />
        <OrbitControls />

        <Suspense fallback={null}>
          {svgText && (
            <BrazilMap 
              svgData={svgText} 
              activeTheme={activeTheme} 
            />
          )}
          <Effects bloom={true} noise={true} />
        </Suspense>

        <ambientLight intensity={0.5} />
      </Canvas>
    </div>
  );
}