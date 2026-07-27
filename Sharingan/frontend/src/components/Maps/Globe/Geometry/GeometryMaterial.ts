import * as THREE from 'three';
import vertexShader from './Shader/geometry.vert';
import fragmentShader from './Shader/geometry.frag';

export const GeometryShader = {
  uniforms: {
    uHeightMap: { value: null },
    uColor: { value: new THREE.Color('#ff4444') },
    uTime: { value: 0 },
  },
  vertexShader,
  fragmentShader
};