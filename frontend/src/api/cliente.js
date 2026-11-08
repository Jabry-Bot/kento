import { useSesion } from '../stores/useSesion'

const API = import.meta.env.VITE_API_URL

const renovarTokens = async () => {
  const { refresh, actualizarTokens, logout } = useSesion.getState()

  if (!refresh) return false

  const resp = await fetch(`${API}/api/cuentas/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })

  if (!resp.ok) {
    logout()
    return false
  }

  actualizarTokens(await resp.json())
  return true
}

export const acceder = async (ruta, opciones = {}, reintentar = true) => {
  const { access } = useSesion.getState()

  const resp = await fetch(`${API}${ruta}`, {
    ...opciones,
    headers: {
      ...(!(opciones.body instanceof FormData) && { 'Content-Type': 'application/json' }),
      ...(access && { Authorization: `Bearer ${access}` }),
      ...opciones.headers,
    },
  })

  if (resp.status === 401 && reintentar && (await renovarTokens())) {
    return acceder(ruta, opciones, false)
  }

  return resp
}
export const primerError = (datos) =>
  datos.error ?? datos.detail ?? Object.values(datos)[0]?.[0] ?? 'Algo ha fallado'
