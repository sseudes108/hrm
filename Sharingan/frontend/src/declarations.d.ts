// No arquivo src/declarations.d.ts (ou similar)
declare module 'three/examples/jsm/loaders/SVGLoader' {
  import { Loader, LoadingManager, ShapePath } from 'three';
  export class SVGLoader extends Loader {
    constructor(manager?: LoadingManager);
    load(url: string, onLoad: (data: SVGData) => void, onProgress?: (event: ProgressEvent) => void, onError?: (event: ErrorEvent) => void): void;
    static parse(text: string): SVGData;
    static pointsToStroke(points: number[], style: SVGStrokeStyle, arcDivisions?: number, minDistance?: number): THREE.BufferGeometry;
    static createShapes(shapePath: ShapePath): THREE.Shape[];
  }
  export interface SVGData {
    paths: ShapePath[];
    xml: XMLDocument;
  }
}