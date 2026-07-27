import { useContext } from 'react';
import { StateHoverContext } from './stateHoverContext';
export function useStateHover() { const context = useContext(StateHoverContext); if (!context) throw new Error('useStateHover must be used within StateHoverProvider'); return context; }
