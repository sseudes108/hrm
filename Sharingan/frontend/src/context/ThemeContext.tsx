import { useState, type ReactNode } from 'react';
import { THEMES, type ThemeMode } from '../constants/colors';
import { ThemeContext } from './themeContext';

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [viewMode, setViewMode] = useState<ThemeMode>('FRAUDE');

  return (
    <ThemeContext.Provider value={{ theme: THEMES[viewMode], viewMode, setViewMode }}>
      {children}
    </ThemeContext.Provider>
  );
}
