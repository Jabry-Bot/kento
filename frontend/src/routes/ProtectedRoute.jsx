import { Navigate, Outlet } from 'react-router'
import { useSesion } from '../stores/useSesion'

export const ProtectedRoute = () => {
  const estado = useSesion((sesion) => sesion.estado)

  if (estado !== 'autenticado') {
    return <Navigate to="/login" replace />
  }
  return <Outlet />
}
