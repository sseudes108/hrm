import { createBrowserRouter } from 'react-router-dom';
import Lab from './pages/Lab';
import UnderConstruction from './pages/NotFound';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Lab />,
  },
  {
    path: '*',
    element: <UnderConstruction />,
  },
]);