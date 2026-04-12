import * as THREE from 'three';
import vertexShader from './Shader/overlay.vert';
import fragmentShader from './Shader/overlay.frag';

export const OverlayShader = {
  uniforms: {
    uHeightMap: { value: null },
    uColor: { value: new THREE.Color('#ff4444') },
    uTime: { value: 0 },
  },
  vertexShader,
  fragmentShader
};