import { createContext } from 'react';
import type { Theme, ThemeMode } from '../constants/colors';

export interface ThemeContextValue {
  theme: Theme;
  viewMode: ThemeMode;
  setViewMode: (mode: ThemeMode) => void;
}

export const ThemeContext = createContext<ThemeContextValue | null>(null);
