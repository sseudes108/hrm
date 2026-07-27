import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { ThemeProvider } from './context/ThemeContext.tsx'
import { MapEventsProvider } from './context/MapEventsProvider.tsx'
import { MapVisualizationProvider } from './context/MapVisualizationProvider.tsx'
import { DashboardDataProvider } from './context/DashboardDataProvider.tsx'
import { StateHoverProvider } from './context/StateHoverContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <MapEventsProvider>
        <MapVisualizationProvider>
          <DashboardDataProvider>
            <StateHoverProvider>
              <App />
            </StateHoverProvider>
          </DashboardDataProvider>
        </MapVisualizationProvider>
      </MapEventsProvider>
    </ThemeProvider>
  </StrictMode>,
)
