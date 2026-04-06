import * as THREE from 'three';
import vertexShader from './shaders/globe.vert';
import fragmentShader from './shaders/globe.frag';

export const GlobeShader = {
  uniforms: {
    uHeightMap: { value: null },
    uColor: { value: new THREE.Color('#ff4444') },
    uTime: { value: 0 },
  },
  vertexShader,
  fragmentShader
};