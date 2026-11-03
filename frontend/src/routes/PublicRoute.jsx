import { Navigate, Outlet } from 'react-router'
import { useSesion } from '../stores/useSesion'

export const PublicRoute = () => {
  const estado = useSesion((sesion) => sesion.estado)

  if (estado === 'autenticado') {
    return <Navigate to="/" replace />
  }
  return <Outlet />
}
