import { Navigate, Outlet, useSearchParams } from 'react-router'
import { useSesion } from '../stores/useSesion'

export const PublicRoute = () => {
  const estado = useSesion((sesion) => sesion.estado)
  const [parametros] = useSearchParams()
  const siguiente = parametros.get('siguiente')
  if (estado === 'autenticado') {
    // evitamos que se accedan a urls externas
    const valida = siguiente?.startsWith('/') && !siguiente.startsWith('//')

    return <Navigate to={valida ? siguiente : '/'} replace />
  }
  return <Outlet />
}
